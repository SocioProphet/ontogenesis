#!/usr/bin/env python3
"""Run SHACL gates over the merged data graph.

Default behavior:
- merges all *.ttl under Upper/Middle/Lower/Domains/Platform/prophet/epi/catalog
- merges all shapes under shapes/ plus module-local shapes
- runs pyshacl validate
"""
from __future__ import annotations

import sys
from pathlib import Path
from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

DATA_DIRS = ["Upper", "Middle", "Lower", "Domains", "Platform", "prophet", "epi", "catalog", "examples"]
SHAPES_DIRS = ["shapes", "prophet/shapes", "epi/shapes"]

def load_all_ttl(dirs: list[str]) -> Graph:
    g = Graph()
    for d in dirs:
        p = ROOT / d
        if not p.exists():
            continue
        for f in sorted(p.rglob("*.ttl")):
            g.parse(f, format="turtle")
    return g

def main() -> int:
    data_graph = load_all_ttl(DATA_DIRS)
    shapes_graph = load_all_ttl(SHAPES_DIRS)

    conforms, report_graph, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        debug=False,
    )

    print(report_text)
    if not conforms:
        # Write report to audit/
        outdir = ROOT / "audit"
        outdir.mkdir(exist_ok=True)
        (outdir / "shacl_report.ttl").write_text(report_graph.serialize(format="turtle"))
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
