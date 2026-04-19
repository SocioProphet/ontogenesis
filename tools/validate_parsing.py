#!/usr/bin/env python3
"""Validate the parsing ontology family.

Runs a focused validation pass over the parsing module family and the parsing SHACL bundle.
This is intentionally narrower than `tools/validate.py`, which validates the broader repo.

Default behavior on this branch prefers the aligned ACSET variant when present so the parsing
cleanup work can be validated independently of the canonical replacement step.

Dependencies: rdflib + pyshacl
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
PARSING_DIR = ROOT / "Platform" / "Parsing"
SHAPES_PATH = ROOT / "shapes" / "parsing-gates.ttl"


def parsing_ttls(use_aligned_acset: bool) -> list[Path]:
    files = [
        PARSING_DIR / "core.ttl",
        PARSING_DIR / "link-grammar.ttl",
        PARSING_DIR / "hypergraph-promotion.ttl",
    ]
    acset = PARSING_DIR / ("acset-parse-aligned.ttl" if use_aligned_acset else "acset-parse.ttl")
    files.insert(2, acset)
    return files


def load_graph(use_aligned_acset: bool) -> Graph:
    g = Graph()
    loaded = 0
    for p in parsing_ttls(use_aligned_acset):
        if not p.exists():
            raise FileNotFoundError(f"Missing parsing ontology module: {p}")
        g.parse(p, format="turtle")
        loaded += 1
    if loaded == 0:
        raise RuntimeError("No parsing ontology files loaded.")
    return g


def run_shacl(g: Graph) -> None:
    try:
        from pyshacl import validate
    except Exception as e:
        raise RuntimeError("pyshacl import failed; install requirements.txt") from e

    if not SHAPES_PATH.exists():
        raise FileNotFoundError(f"Missing parsing SHACL bundle: {SHAPES_PATH}")

    conforms, _report_graph, report_text = validate(
        data_graph=g,
        shacl_graph=str(SHAPES_PATH),
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        debug=False,
    )

    if not conforms:
        sys.stderr.write("ERR: parsing SHACL validation failed.\n")
        sys.stderr.write(report_text + "\n")
        raise SystemExit(2)

    print("OK: parsing SHACL conforms.")


def run_basic_invariants(g: Graph) -> None:
    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?cls WHERE {
      ?cls a owl:Class .
      FILTER(STRSTARTS(STR(?cls), "https://socioprophet.github.io/ontogenesis/Platform/Parsing/"))
    }
    """
    rows = list(g.query(q))
    if not rows:
        raise SystemExit("ERR: no parsing classes discovered in loaded graph.")
    print(f"OK: discovered {len(rows)} parsing class declaration(s).")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--canonical-acset",
        action="store_true",
        help="validate the canonical acset-parse.ttl instead of the aligned variant",
    )
    args = ap.parse_args()

    g = load_graph(use_aligned_acset=not args.canonical_acset)
    run_basic_invariants(g)
    run_shacl(g)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
