#!/usr/bin/env python3
"""JSON-LD context sanity tests.

We do NOT require full JSON-LD rendering for every ontology file, but we
require that our contexts load and can compact/expand a minimal document.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from pyld import jsonld

ROOT = Path(__file__).resolve().parents[1]
CONTEXTS = [
    ROOT / "contexts/main.context.jsonld",
    ROOT / "prophet/contexts/prophet.context.jsonld",
    ROOT / "epi/contexts/epi.context.jsonld",
]

def main() -> int:
    for cpath in CONTEXTS:
        if not cpath.exists():
            print(f"[SKIP] missing {cpath}")
            continue
        ctx = json.loads(cpath.read_text(encoding="utf-8"))
        doc = {
            "@context": ctx["@context"] if "@context" in ctx else ctx,
            "id": "https://example.invalid/item/1",
            "type": "upper:InformationArtifact",
            "label": "roundtrip-test",
        }
        expanded = jsonld.expand(doc)
        compacted = jsonld.compact(expanded, doc["@context"])
        if "label" not in compacted:
            print(f"[FAIL] {cpath}: compacted doc missing 'label'")
            return 1
        print(f"[OK] {cpath}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
