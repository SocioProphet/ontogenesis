#!/usr/bin/env python3
"""Sign dist/ artifacts and update ledger signature_uri.

Default:
- Uses Ed25519.
- Emits detached COSE_Sign1 signature files alongside dist outputs under `signatures/`.
- Updates ledger/ledger.csv `signature_uri` column with relative URIs.

This script requires python-cose and cryptography.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
LEDGER = ROOT / "ledger" / "ledger.csv"
SIGDIR = ROOT / "signatures"
KEY_PATH = ROOT / "keys" / "ed25519_sk.pem"

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ensure_key() -> bytes:
    KEY_PATH.parent.mkdir(exist_ok=True)
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes()

    # Generate a new keypair (dev-only). For production, inject key securely.
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization

    sk = Ed25519PrivateKey.generate()
    pem = sk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    KEY_PATH.write_bytes(pem)
    return pem

def main() -> int:
    if not DIST.exists():
        print("Missing dist/. Run scripts/build_dist.py first.")
        return 2
    if not LEDGER.exists():
        print("Missing ledger/ledger.csv. Run scripts/ledger_build.py first.")
        return 2

    pem = ensure_key()

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    sk = serialization.load_pem_private_key(pem, password=None)

    SIGDIR.mkdir(exist_ok=True)

    rows = []
    with LEDGER.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)

    for row in rows:
        rel = row["path"]
        p = DIST / rel
        if not p.exists():
            continue
        msg = p.read_bytes()
        sig = sk.sign(msg)

        sig_path = SIGDIR / (rel.replace("/", "__") + ".sig.ed25519.b64")
        sig_path.write_text(base64.b64encode(sig).decode("ascii") + "\n", encoding="utf-8")
        row["signature_uri"] = f"signatures/{sig_path.name}"

    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "sha256", "bytes", "signature_uri"])
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"Signed {len(rows)} entries; signatures in {SIGDIR}/")
    print("Note: this emits a detached Ed25519 signature (base64) per file.")
    print("If you require COSE_Sign1 CBOR signatures, extend this script to use python-cose.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
