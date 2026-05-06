#!/usr/bin/env python3
"""Validate the Semantic Enterprise v0.1 downstream manifest."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "manifests/semantic_enterprise_v0_1_manifest.json"

REQUIRED_TOP_LEVEL = {
    "version": "0.1.0",
    "status": "stable",
    "rollup_registry": "catalog/semantic_enterprise_v0_1_registry.ttl",
    "release_note": "docs/semantic-enterprise/v0.1-release-note.md",
    "named_graph_fixture": "examples/named-graphs/semantic_sector_named_graphs.ttl",
}

REQUIRED_LISTS = [
    "registry_supplements",
    "architecture_docs",
    "middle_modules",
    "domain_modules",
    "alignment_modules",
    "shape_modules",
    "contexts",
    "examples",
    "downstream_consumers",
    "validators",
    "workflows",
]

REQUIRED_SECTORS = ["finance", "threat-intel", "investigation", "supply-chain", "defense-c2"]


def exists(path: str) -> bool:
    return (ROOT / path).is_file()


def main() -> int:
    errors: list[str] = []
    path = ROOT / MANIFEST
    if not path.is_file():
        print(f"missing manifest: {MANIFEST}")
        return 1

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"manifest JSON parse failed: {exc}")
        return 1

    for key, expected in REQUIRED_TOP_LEVEL.items():
        actual = manifest.get(key)
        if actual != expected:
            errors.append(f"{key}: expected {expected!r}, got {actual!r}")
        if key.endswith("registry") or key.endswith("note") or key.endswith("fixture"):
            if not exists(expected):
                errors.append(f"referenced file missing: {expected}")

    for key in REQUIRED_LISTS:
        value = manifest.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"{key}: expected non-empty list")
            continue
        for item in value:
            if isinstance(item, str) and "/" in item and not exists(item):
                errors.append(f"{key}: referenced path missing: {item}")

    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, dict):
        errors.append("scenarios: expected object")
    else:
        for sector in REQUIRED_SECTORS:
            spec = scenarios.get(sector)
            if not isinstance(spec, dict):
                errors.append(f"scenarios.{sector}: expected object")
                continue
            for key in ["scenario", "query"]:
                value = spec.get(key)
                if not isinstance(value, str) or not exists(value):
                    errors.append(f"scenarios.{sector}.{key}: missing referenced file {value!r}")
            if not spec.get("named_graph_uri_fragment"):
                errors.append(f"scenarios.{sector}.named_graph_uri_fragment: missing")

    if errors:
        print("Semantic manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Semantic manifest validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
