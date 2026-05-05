#!/usr/bin/env python3
"""Validate that all Turtle files in this repo parse cleanly.

This is intentionally strict: a parse failure is a promotion gate failure.
"""
from __future__ import annotations

import sys
from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]

SEARCH_DIRS = ["Upper", "Middle", "Lower", "Domains", "Alignments", "Platform", "prophet", "epi", "catalog", "shapes", "examples"]

def main() -> int:
    ttl_files = []
    for d in SEARCH_DIRS:
        p = ROOT / d
        if not p.exists():
            continue
        ttl_files += sorted(p.rglob("*.ttl"))

    if not ttl_files:
        print("No .ttl files found.")
        return 2

    errors = 0
    for f in ttl_files:
        g = Graph()
        try:
            g.parse(f, format="turtle")
        except Exception as e:
            errors += 1
            print(f"[FAIL] {f}: {e}")
        else:
            print(f"[OK]   {f}  ({len(g)} triples)")

    if errors:
        print(f"\n{errors} Turtle files failed to parse.")
        return 1
    print("\nAll Turtle files parsed successfully.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
