#!/usr/bin/env python3
"""Mint (inject/refresh) registration receipts into Systema Concept Entry graphs.

Reads each positive example graph, computes a deterministic content-hash receipt
for every entry that carries provenance governance fields, and writes the receipt
back onto the entry. Idempotent: re-running on an unchanged graph is a no-op.

Negative fixtures under examples/systema/invalid/ are intentionally left alone
(they exist to fail the gate). Run:

    python scripts/mint_concept_receipts.py            # write receipts
    python scripts/mint_concept_receipts.py --check    # verify only (CI-safe)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept_receipt import RECEIPT_FIELD, compute_receipt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
POSITIVE_GRAPHS = [
    ROOT / "examples" / "systema" / "finance-arc-concepts.example.jsonld",
    ROOT / "examples" / "systema" / "gaia-value-flow-vocabulary.example.jsonld",
]


def entries(doc: dict) -> list[dict]:
    if "@graph" in doc:
        return [e for e in doc["@graph"] if isinstance(e, dict)]
    return [doc]


def is_registered_entry(entry: dict) -> bool:
    # Only mint for governed concept entries (those carrying provenance fields).
    return "provenanceClass" in entry and "conceptVersion" in entry


def main() -> int:
    check_only = "--check" in sys.argv
    drift = 0
    for path in POSITIVE_GRAPHS:
        doc = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for entry in entries(doc):
            if not is_registered_entry(entry):
                continue
            want = compute_receipt(entry)
            have = entry.get(RECEIPT_FIELD)
            if have != want:
                if check_only:
                    print(f"[DRIFT] {path.name} :: {entry.get('conceptId')} "
                          f"have={have} want={want}")
                    drift += 1
                else:
                    entry[RECEIPT_FIELD] = want
                    changed = True
        if changed and not check_only:
            path.write_text(
                json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"[MINT] receipts refreshed: {path.relative_to(ROOT)}")
    if check_only:
        if drift:
            print(f"\n{drift} receipt drift(s).")
            return 1
        print("All receipts current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
