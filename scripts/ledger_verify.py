#!/usr/bin/env python3
"""Verify ledger/ledger.csv against dist/ content."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
LEDGER = ROOT / "ledger" / "ledger.csv"

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    if not DIST.exists():
        print("Missing dist/. Run scripts/build_dist.py first.")
        return 2
    if not LEDGER.exists():
        print("Missing ledger/ledger.csv. Run scripts/ledger_build.py first.")
        return 2

    errors = 0
    with LEDGER.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rel = row["path"]
            p = DIST / rel
            if not p.exists():
                print(f"[FAIL] missing dist file: {rel}")
                errors += 1
                continue
            h = sha256_file(p)
            if h != row["sha256"]:
                print(f"[FAIL] sha256 mismatch: {rel}\n  ledger={row['sha256']}\n  dist  ={h}")
                errors += 1
            else:
                print(f"[OK] {rel}")

    if errors:
        print(f"\nLedger verification failed: {errors} problems.")
        return 1
    print("\nLedger verification OK.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
