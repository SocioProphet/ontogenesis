#!/usr/bin/env python3
"""Build ledger/ledger.csv from dist/ manifests.

Ledger fields:
- path
- sha256
- bytes
- signature_uri (optional, filled by sign_dist.py)
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
LEDGER_DIR = ROOT / "ledger"
LEDGER = LEDGER_DIR / "ledger.csv"

def main() -> int:
    manifest_path = AUDIT / "dist_manifest.json"
    if not manifest_path.exists():
        print("Missing audit/dist_manifest.json. Run scripts/build_dist.py first.")
        return 2

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = data.get("files", [])
    LEDGER_DIR.mkdir(exist_ok=True)

    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "sha256", "bytes", "signature_uri"])
        w.writeheader()
        for item in files:
            w.writerow({
                "path": item["path"],
                "sha256": item["sha256"],
                "bytes": item["bytes"],
                "signature_uri": "",
            })

    print(f"Wrote {LEDGER} with {len(files)} entries.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
