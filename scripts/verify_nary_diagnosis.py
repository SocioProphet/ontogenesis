#!/usr/bin/env python3
"""Verify the n-ary Diagnosis promotion round-trips (Symbolic-AI/KG doc test vector).

The AtomSpace-hyperedge -> RDF promotion is made checkable: the Patient x Disease x Doctor x Date
relation, reified as one intermediate node, must be SPARQL-queryable back into the complete 4-tuple
(round-trip), and an INCOMPLETE diagnosis (missing a role) must be refused by the SHACL shape.
"""
from __future__ import annotations

import sys
from pathlib import Path

import rdflib
import pyshacl

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Domains" / "nary-diagnosis.ttl"
SHAPE = ROOT / "shapes" / "nary-diagnosis.shacl.ttl"
N = "https://socioprophet.github.io/ontogenesis/domains/nary-diagnosis#"

Q = f"""
PREFIX nary: <{N}>
SELECT ?patient ?disease ?doctor ?date WHERE {{
  ?dx a nary:Diagnosis ;
      nary:patient ?patient ; nary:disease ?disease ;
      nary:doctor ?doctor ;  nary:diagnosedOn ?date .
}}"""


def main() -> int:
    fails = []
    g = rdflib.Graph().parse(DATA, format="turtle")

    # 1. Round-trip: the n-ary atom is SPARQL-queryable back into one complete 4-tuple.
    rows = list(g.query(Q))
    if len(rows) != 1 or any(v is None for v in rows[0]):
        fails.append(f"the n-ary Diagnosis did not reconstruct one complete 4-tuple (rows={len(rows)})")
    else:
        p, d, doc, date = rows[0]
        if not (str(p).endswith("patient-alice") and str(d).endswith("disease-influenza")
                and str(doc).endswith("doctor-bob") and str(date) == "2026-08-03"):
            fails.append(f"round-tripped 4-tuple has the wrong roles: {rows[0]}")

    # 2. Teeth: an INCOMPLETE diagnosis (drop the doctor role) must fail the SHACL shape.
    incomplete = rdflib.Graph().parse(data=f"""
        @prefix nary: <{N}> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        nary:diagnosis-bad a nary:Diagnosis ;
          nary:patient nary:patient-alice ; nary:disease nary:disease-influenza ;
          nary:diagnosedOn "2026-08-03"^^xsd:date .
    """, format="turtle")
    shape = rdflib.Graph().parse(SHAPE, format="turtle")
    conforms, _, _ = pyshacl.validate(incomplete, shacl_graph=shape, inference="none")
    if conforms:
        fails.append("an incomplete Diagnosis (missing doctor) wrongly CONFORMED — the n-ary shape has no teeth")

    # 3. The complete example must itself conform.
    ok, _, _ = pyshacl.validate(g, shacl_graph=shape, inference="none")
    if not ok:
        fails.append("the complete Diagnosis example does not conform to its own shape")

    for m in fails:
        print(f"FAIL: {m}", file=sys.stderr)
    if fails:
        return 1
    print("OK: n-ary Diagnosis round-trips (SPARQL-queryable 4-tuple) + incomplete refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
