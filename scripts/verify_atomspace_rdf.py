#!/usr/bin/env python3
"""Verify the AtomSpace <-> RDF StorageNode connector round-trips with fidelity.

The Symbolic-AI/KG doc promotes an AtomSpace hypergraph to RDF. This makes ONE verifiable
slice of that promotion checkable end to end:

    AtomSpace (fixture JSON)  --atomspace_to_rdf-->  RDF  --rdf_to_atomspace-->  AtomSpace

The mapping (small and faithful):
  * ConceptNode / PredicateNode  -> RDF resources (IRIs), each typed as:ConceptNode / as:PredicateNode.
  * NumberNode                   -> an xsd:decimal typed literal.
  * InheritanceLink(A, B)        -> the triple  A as:inherits B .
  * EvaluationLink(P, ListLink(a,b)) -> the triple  a <P> b  (the PredicateNode IRI is the predicate).
  * TruthValue(strength, confidence) -> an RDF reified annotation (as:TruthValueStatement) on that
    statement -- the RDF-standard reification an RDF-star quoted-triple annotation desugars to,
    mirroring the #136 n-ary intermediate-node idiom. (rdflib 7.x ships no RDF-star turtle parser,
    so reification is the faithful, pinned-version-safe carrier.)

Proven here (fail-closed, self-testing):
  1. POSITIVE round-trip: fixture -> RDF -> fixture recovers a graph ISOMORPHIC to the original,
     TruthValues included; and the emitted RDF is isomorphic to the checked-in Domains TTL.
  2. NEGATIVE (SHACL teeth): a TruthValue that drops its confidence is REFUSED by the shape.
  3. NEGATIVE (fidelity teeth): a lossy promotion that drops a TruthValue does NOT round-trip
     back isomorphic -- the connector detects the loss for the right reason.
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

import rdflib
from rdflib import Graph, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import RDF, XSD
import pyshacl

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "atomspace-rdf" / "atomspace-graph.json"
CANON_TTL = ROOT / "Domains" / "atomspace-rdf.ttl"
SHAPE = ROOT / "shapes" / "atomspace-rdf.shacl.ttl"

AS = rdflib.Namespace("https://socioprophet.github.io/ontogenesis/domains/atomspace-rdf#")
AS_INHERITS = AS["inherits"]


def _dec(x) -> str:
    """Canonical xsd:decimal string, so 1.0 == 1.0 both directions."""
    return str(Decimal(str(x)))


# --------------------------------------------------------------------------- #
# Canonical AtomSpace representation: a frozenset of fully-embedded link atoms.
# Node type + name are embedded in every link, so ConceptNode vs PredicateNode
# vs NumberNode distinctions and TruthValues are all part of the identity.
# --------------------------------------------------------------------------- #
def _node_key(atom: dict) -> tuple:
    t = atom["type"]
    if t == "NumberNode":
        return ("NumberNode", _dec(atom["value"]))
    return (t, atom["name"])


def _tv_key(tv) -> tuple | None:
    if tv is None:
        return None
    return (_dec(tv["strength"]), _dec(tv["confidence"]))


def atomspace_canonical(atoms: list[dict]) -> frozenset:
    links = set()
    for a in atoms:
        t = a["type"]
        if t == "InheritanceLink":
            s, o = a["outgoing"]
            links.add(("InheritanceLink", _node_key(s), _node_key(o), _tv_key(a.get("tv"))))
        elif t == "EvaluationLink":
            pred, lst = a["outgoing"]
            s, o = lst["outgoing"]
            links.add(("EvaluationLink", _node_key(pred),
                       ("ListLink", _node_key(s), _node_key(o)), _tv_key(a.get("tv"))))
        # Bare nodes are recovered from the links they participate in; no standalone entry needed.
    return frozenset(links)


# --------------------------------------------------------------------------- #
# Connector: AtomSpace -> RDF
# --------------------------------------------------------------------------- #
def _term(atom: dict):
    """A node atom -> its RDF term (IRI for Concept/Predicate, typed literal for NumberNode)."""
    t = atom["type"]
    if t == "ConceptNode":
        return AS[f"concept-{atom['name']}"]
    if t == "PredicateNode":
        return AS[f"predicate-{atom['name']}"]
    if t == "NumberNode":
        return Literal(_dec(atom["value"]), datatype=XSD.decimal)
    raise ValueError(f"unpromotable node atom: {atom!r}")


def _reify(g: Graph, s, p, o, tv, drop_confidence: bool = False) -> None:
    if tv is None:
        return
    st = rdflib.BNode()
    g.add((st, RDF.type, AS.TruthValueStatement))
    g.add((st, RDF.subject, s))
    g.add((st, RDF.predicate, p))
    g.add((st, RDF.object, o))
    g.add((st, AS.strength, Literal(_dec(tv["strength"]), datatype=XSD.decimal)))
    if not drop_confidence:
        g.add((st, AS.confidence, Literal(_dec(tv["confidence"]), datatype=XSD.decimal)))


def atomspace_to_rdf(atoms: list[dict], *, drop_all_tv: bool = False,
                     drop_confidence: bool = False) -> Graph:
    g = Graph()
    g.bind("as", AS)
    for a in atoms:
        t = a["type"]
        if t in ("ConceptNode", "PredicateNode"):
            g.add((_term(a), RDF.type, AS.ConceptNode if t == "ConceptNode" else AS.PredicateNode))
        elif t == "InheritanceLink":
            s_atom, o_atom = a["outgoing"]
            s, o = _term(s_atom), _term(o_atom)
            g.add((s, AS_INHERITS, o))
            if not drop_all_tv:
                _reify(g, s, AS_INHERITS, o, a.get("tv"), drop_confidence)
        elif t == "EvaluationLink":
            pred_atom, lst = a["outgoing"]
            p = _term(pred_atom)
            s_atom, o_atom = lst["outgoing"]
            s, o = _term(s_atom), _term(o_atom)
            g.add((s, p, o))
            if not drop_all_tv:
                _reify(g, s, p, o, a.get("tv"), drop_confidence)
    return g


# --------------------------------------------------------------------------- #
# Connector: RDF -> AtomSpace
# --------------------------------------------------------------------------- #
def _iri_to_node(term) -> dict:
    if isinstance(term, Literal):
        return {"type": "NumberNode", "value": str(term)}
    local = str(term).rsplit("#", 1)[-1]
    if local.startswith("concept-"):
        return {"type": "ConceptNode", "name": local[len("concept-"):]}
    if local.startswith("predicate-"):
        return {"type": "PredicateNode", "name": local[len("predicate-"):]}
    raise ValueError(f"un-demotable resource: {term}")


def rdf_to_atomspace(g: Graph) -> list[dict]:
    predicate_nodes = {s for s in g.subjects(RDF.type, AS.PredicateNode)}

    # Recover TruthValues keyed by the (s, p, o) they reify.
    tv_by_spo: dict[tuple, dict] = {}
    for st in g.subjects(RDF.type, AS.TruthValueStatement):
        s = g.value(st, RDF.subject)
        p = g.value(st, RDF.predicate)
        o = g.value(st, RDF.object)
        strength = g.value(st, AS.strength)
        confidence = g.value(st, AS.confidence)
        # Fail-closed: a partial TruthValue is not a TruthValue.
        if None in (s, p, o, strength, confidence):
            continue
        tv_by_spo[(s, p, o)] = {"strength": str(strength), "confidence": str(confidence)}

    atoms: list[dict] = []
    for s, p, o in g:
        if p == AS_INHERITS:
            atoms.append({"type": "InheritanceLink",
                          "outgoing": [_iri_to_node(s), _iri_to_node(o)],
                          "tv": tv_by_spo.get((s, p, o))})
        elif p in predicate_nodes:
            atoms.append({"type": "EvaluationLink",
                          "outgoing": [_iri_to_node(p),
                                       {"type": "ListLink", "outgoing": [_iri_to_node(s), _iri_to_node(o)]}],
                          "tv": tv_by_spo.get((s, p, o))})
        # rdf:type / reification triples are structural, not link atoms.
    return atoms


# --------------------------------------------------------------------------- #
def main() -> int:
    fails: list[str] = []
    atoms = json.loads(FIXTURE.read_text())["atoms"]
    original = atomspace_canonical(atoms)

    # 1a. POSITIVE: fixture -> RDF -> fixture is isomorphic (TruthValues included).
    g = atomspace_to_rdf(atoms)
    recovered = atomspace_canonical(rdf_to_atomspace(g))
    if recovered != original:
        fails.append(f"round-trip lost fidelity: missing={original - recovered} extra={recovered - original}")

    # 1b. POSITIVE: the emitted RDF matches the checked-in canonical TTL (up to isomorphism).
    canon = Graph().parse(CANON_TTL, format="turtle")
    # Compare only the ABox the connector emits (drop the TBox/ontology header of the committed file).
    abox = Graph()
    for s, p, o in canon:
        if (p == RDF.type and o in (AS.ConceptNode, AS.PredicateNode, AS.TruthValueStatement)) \
           or p in (AS_INHERITS, RDF.subject, RDF.predicate, RDF.object, AS.strength, AS.confidence) \
           or p in {ps for ps in canon.subjects(RDF.type, AS.PredicateNode)}:
            abox.add((s, p, o))
    if not isomorphic(g, abox):
        fails.append("emitted RDF is not isomorphic to the checked-in Domains/atomspace-rdf.ttl ABox")

    # 1c. POSITIVE: the checked-in TTL itself demotes back to the original AtomSpace.
    if atomspace_canonical(rdf_to_atomspace(canon)) != original:
        fails.append("the checked-in Domains TTL does not demote back to the fixture AtomSpace")

    # 2. NEGATIVE (SHACL teeth): a TruthValue missing its confidence must be REFUSED.
    lossy_tv = atomspace_to_rdf(atoms, drop_confidence=True)
    shape = Graph().parse(SHAPE, format="turtle")
    conforms, _, _ = pyshacl.validate(lossy_tv, shacl_graph=shape, inference="none")
    if conforms:
        fails.append("a TruthValue with no confidence wrongly CONFORMED -- the SHACL shape has no teeth")

    # 2b. The faithful RDF must itself conform to the shape.
    ok, _, txt = pyshacl.validate(g, shacl_graph=shape, inference="none")
    if not ok:
        fails.append(f"the faithful promotion does not conform to its own shape:\n{txt}")

    # 3. NEGATIVE (fidelity teeth): a promotion that drops ALL TruthValues must NOT round-trip.
    lossy = atomspace_to_rdf(atoms, drop_all_tv=True)
    lossy_recovered = atomspace_canonical(rdf_to_atomspace(lossy))
    if lossy_recovered == original:
        fails.append("a TruthValue-stripped promotion wrongly round-tripped -- fidelity check has no teeth")
    else:
        # Confirm the ONLY difference is the missing TruthValues (right reason, not a coincidence).
        stripped_original = frozenset((*t[:3], None) for t in original)
        if lossy_recovered != stripped_original:
            fails.append("TruthValue-stripped round-trip differs by more than the TruthValues (wrong reason)")

    for m in fails:
        print(f"FAIL: {m}", file=sys.stderr)
    if fails:
        return 1
    print(f"OK: AtomSpace<->RDF round-trips ({len(original)} link atoms, TruthValues isomorphic); "
          "incomplete TruthValue refused by SHACL; TruthValue-stripped promotion refused by fidelity check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
