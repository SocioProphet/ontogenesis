#!/usr/bin/env python3
"""Validate the estate-catalog P3 query surface + KKO alignment.

The estate-catalog is "reason over the estate, don't read every repo" — but a query
surface that is never executed against a known graph is a claim, not a capability.
This lane runs the versioned queries in ``examples/queries/estate-catalog/*.rq``
against the estate-catalog TBox + a tiny, SHACL-conform ABox fixture and asserts the
EXACT rows each must return. Exact-set assertions give teeth both ways: a query that
drops a real dependent, or sweeps in one that should not be there, both fail. Two
checks are deliberately negative — a leaf has an empty blast radius, and the
Apache-licensed model is absent from the licence-compliance result — so the queries
are shown discriminating, not just returning "everything".

It also checks the governed KKO alignment (``Alignments/kko.ttl``) resolves: every
cat: class that grounds into KKO via skos:closeMatch has a matching governed
smap:MappingAssertion (and vice versa — no orphan assertions), every mapsFrom
resolves to a declared class in the TBox, and every mapsTo is a KKO IRI.

Dependencies: rdflib + owlrl (owlrl ships with pyshacl, already required).
"""

from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDFS, SKOS
from owlrl import DeductiveClosure, RDFS_Semantics

ROOT = Path(__file__).resolve().parents[1]

CAT = Namespace("https://socioprophet.github.io/ontogenesis/domains/estate-catalog#")
EX = Namespace("https://socioprophet.github.io/ontogenesis/domains/estate-catalog/examples#")
KKO = Namespace("http://kbpedia.org/ontologies/kko#")

UPPER = ROOT / "Upper" / "upper-core.ttl"
TBOX = ROOT / "Domains" / "estate-catalog" / "estate-catalog.ttl"
KKO_ALIGN = ROOT / "Alignments" / "kko.ttl"
SEMMAP = ROOT / "Middle" / "semantic-mapping.ttl"
FIXTURE = ROOT / "tests" / "estate-catalog" / "mini-estate.ttl"
QDIR = ROOT / "examples" / "queries" / "estate-catalog"
SHAPES = ROOT / "shapes" / "estate-catalog" / "estate-catalog.shacl.ttl"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def _load(*files: Path) -> Graph:
    g = Graph()
    for f in files:
        g.parse(f, format="turtle")
    return g


def _query_graph() -> Graph:
    """TBox subclass/subproperty axioms + fixture, rdfs-materialised so that
    bound-fragment instances are their catalog family and cat:dependsOn+ traverses
    its subproperties (runsOn/usesModel/consumesData/storedIn/deployedTo)."""
    g = _load(UPPER, TBOX, FIXTURE)
    DeductiveClosure(RDFS_Semantics).expand(g)
    return g


def _run(g: Graph, name: str, **bindings) -> set[tuple]:
    q = (QDIR / name).read_text(encoding="utf-8")
    init = {k: (v if isinstance(v, (URIRef, Literal)) else Literal(v)) for k, v in bindings.items()}
    rows = g.query(q, initBindings=init) if init else g.query(q)
    return {tuple(str(t) for t in row) for row in rows}


def _one_col(rows: set[tuple]) -> set[str]:
    return {r[0] for r in rows}


def check_fixture_conforms() -> None:
    """The fixture must be a VALID estate before we reason over it — otherwise the
    query rows are answers about malformed data. Scoped to the estate-catalog shapes
    only (the fixture lives outside the estate-wide gate on purpose)."""
    from pyshacl import validate

    data = _load(UPPER, TBOX, FIXTURE)
    conforms, _report, text = validate(
        data_graph=data, shacl_graph=str(SHAPES), shacl_graph_format="turtle",
        inference="rdfs", abort_on_first=False, advanced=True,
    )
    if not conforms:
        fail(f"query fixture is NOT estate-catalog-conform:\n{text}")
    print("OK: query fixture conforms to the estate-catalog SHACL shapes")


def check_queries() -> None:
    g = _query_graph()

    # 1. resolve-resource — one governed record resolved by its catalog id.
    got = _run(g, "resolve-resource.rq", catalogId="inf.cluster.core")
    want = {(str(EX.entryCluster), str(EX.clusterCore), "SocioProphet/platform", "active")}
    if got != want:
        fail(f"resolve-resource: expected {want}, got {got}")

    # 2. by-catalog-family — the new Model catalog and a bound fragment (Infra).
    got = _one_col(_run(g, "by-catalog-family.rq", family=CAT.Model))
    want = {str(EX.modelGood), str(EX.modelBad)}
    if got != want:
        fail(f"by-catalog-family(cat:Model): expected {want}, got {got}")
    got = _one_col(_run(g, "by-catalog-family.rq", family=CAT.Infrastructure))
    want = {str(EX.clusterCore), str(EX.bucketArtifacts)}
    if got != want:
        fail(f"by-catalog-family(cat:Infrastructure): expected {want}, got {got}")

    # 3. cross-catalog-lineage — service -> model -> provider(+posture) -> infra.
    rows = _run(g, "cross-catalog-lineage.rq")
    lineage = {(r[0], r[1], r[2], r[3], r[6]) for r in rows}  # service, model, provider, residency, license
    want = {
        (str(EX.svcGateway), str(EX.modelGood), str(EX.providerSov), "sovereign_cluster", "Apache-2.0"),
        (str(EX.svcAnalytics), str(EX.modelBad), str(EX.providerCloud), "off_device", "GPL-3.0-only"),
    }
    if lineage != want:
        fail(f"cross-catalog-lineage: expected {want}, got {lineage}")

    # 4. blast-radius — transitive dependents (positive), a leaf (negative teeth),
    #    and a transitive-through-service case.
    got = _one_col(_run(g, "blast-radius.rq", root=EX.clusterCore))
    want = {str(EX.modelGood), str(EX.modelBad), str(EX.svcGateway), str(EX.svcAnalytics), str(EX.appPortal)}
    if got != want:
        fail(f"blast-radius(clusterCore): expected {want}, got {got}")
    got = _one_col(_run(g, "blast-radius.rq", root=EX.appPortal))
    if got:
        fail(f"blast-radius(appPortal) must be empty (leaf), got {got}")
    got = _one_col(_run(g, "blast-radius.rq", root=EX.datasetCorpus))
    want = {str(EX.svcGateway), str(EX.appPortal)}
    if got != want:
        fail(f"blast-radius(datasetCorpus): expected transitive {want}, got {got}")

    # 5. license-compliance — non-allowlisted models only; the Apache model is absent.
    rows = _run(g, "license-compliance.rq")
    flagged = {(r[0], r[1]) for r in rows}
    want = {(str(EX.modelBad), "GPL-3.0-only")}
    if flagged != want:
        fail(f"license-compliance: expected {want}, got {flagged}")
    if any(r[0] == str(EX.modelGood) for r in rows):
        fail("license-compliance: Apache-2.0 model must NOT be flagged (filter has no teeth)")

    print("OK: estate-catalog query surface — 5 queries, exact rows (incl. 2 negative-teeth checks)")


def check_kko_alignment() -> None:
    tbox = _load(TBOX)
    align = _load(KKO_ALIGN, SEMMAP)
    smap = Namespace("https://socioprophet.github.io/ontogenesis/middle/semantic-mapping#")

    # Inline grounding carried by the TBox (skos:closeMatch into the KKO namespace).
    inline = {
        (str(s), str(o))
        for s, o in tbox.subject_objects(SKOS.closeMatch)
        if str(o).startswith(str(KKO))
    }
    # Governed grounding: smap:MappingAssertion mapsFrom -> mapsTo(KKO).
    governed = set()
    mapsfrom_all = set()
    for a in align.subjects(smap.mapsFrom, None):
        src = align.value(a, smap.mapsFrom)
        tgt = align.value(a, smap.mapsTo)
        if src is None or tgt is None:
            fail(f"KKO alignment {a}: MappingAssertion missing mapsFrom/mapsTo")
        mapsfrom_all.add(str(src))
        if str(tgt).startswith(str(KKO)):
            governed.add((str(src), str(tgt)))

    if inline != governed:
        fail(
            "KKO alignment mismatch (inline TBox grounding vs governed Alignments/kko.ttl):\n"
            f"  only inline:   {sorted(inline - governed)}\n"
            f"  only governed: {sorted(governed - inline)}"
        )

    expected = {
        (str(CAT.EstateResource), str(KKO.Particulars)),
        (str(CAT.CatalogEntry), str(KKO.Methodeutic)),
        (str(CAT.Model), str(KKO.Forms)),
        (str(CAT.Infrastructure), str(KKO.Systems)),
    }
    if governed != expected:
        fail(f"KKO alignment set changed: expected {expected}, got {governed}")

    # Resolvability: every mapsFrom is a declared class in the TBox; every mapsTo is a KKO IRI.
    declared = set(str(c) for c in tbox.subjects(RDFS.subClassOf, None)) | {
        str(s) for s, _, o in tbox.triples((None, None, OWL.Class))
    }
    for src, tgt in governed:
        if src not in declared:
            fail(f"KKO alignment: mapsFrom {src} does not resolve to a declared class in the TBox")
        if not tgt.startswith(str(KKO)):
            fail(f"KKO alignment: mapsTo {tgt} is not a KKO IRI")

    print(f"OK: KKO alignment — {len(governed)} governed assertions resolve; inline grounding matches exactly")


def main() -> int:
    check_fixture_conforms()
    check_queries()
    check_kko_alignment()
    print("OK: estate-catalog P3 (query surface + KKO alignment) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
