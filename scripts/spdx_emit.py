#!/usr/bin/env python3
"""Emit a minimal SPDX 2.3 SBOM (JSON) with checksums.

This is intentionally minimal and self-contained (no external SBOM tools required).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "sbom"
OUT = OUTDIR / "spdx.json"

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    OUTDIR.mkdir(exist_ok=True)

    files = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        # Exclude generated outputs by policy
        if rel.startswith("dist/") or rel.startswith("audit/"):
            continue
        files.append({
            "SPDXID": f"SPDXRef-File-{len(files)+1}",
            "FileName": rel,
            "Checksums": [{"Algorithm": "SHA256", "ChecksumValue": sha256_file(p)}],
        })

    doc = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "ontogenesis",
        "documentNamespace": "https://socioprophet.github.io/ontogenesis/spdx/" + sha256_file(ROOT / "README.md"),
        "creationInfo": {
            "created": datetime.utcnow().isoformat() + "Z",
            "creators": ["Tool: scripts/spdx_emit.py"],
        },
        "files": files,
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(files)} files).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
