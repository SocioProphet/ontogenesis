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
    ROOT / "contexts/prophet-artifact.context.jsonld",
    ROOT / "prophet/contexts/prophet.context.jsonld",
    ROOT / "epi/contexts/epi.context.jsonld",
]

EXAMPLE_DOCS = [
    ROOT / "examples/prophet-artifact-gaia-bounded-osm-ingest.example.jsonld",
    ROOT / "examples/prophet-artifact-notebook-promotion.example.jsonld",
    ROOT / "examples/prophet-artifact-sourceos-image-reproducibility.example.jsonld",
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

    for ep in EXAMPLE_DOCS:
        if not ep.exists():
            print(f"[SKIP] missing {ep}")
            continue
        doc = json.loads(ep.read_text(encoding="utf-8"))
        if isinstance(doc.get("@context"), str) and not doc["@context"].startswith(("http://", "https://")):
            ctx_path = (ep.parent / doc["@context"]).resolve()
            ctx_doc = json.loads(ctx_path.read_text(encoding="utf-8"))
            doc["@context"] = ctx_doc["@context"] if "@context" in ctx_doc else ctx_doc
        expanded = jsonld.expand(doc)
        compacted = jsonld.compact(expanded, doc["@context"])
        if "apiVersion" not in compacted or "spec" not in compacted:
            print(f"[FAIL] {ep}: compacted doc missing expected artifact keys")
            return 1
        print(f"[OK] {ep}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
