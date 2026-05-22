#!/usr/bin/env python3
"""Validate Ontogenesis registry discovery posture.

The repository currently uses a hybrid discovery model:

- `catalog/registry.ttl` remains the primary registry.
- supplemental registry files under `catalog/` are first-class discovery inputs
  while the registry posture is being normalized.

This validator makes that hybrid posture explicit and fail-closed enough for CI:

- registry-like Turtle files must parse;
- at least one registry file and at least one `og:Module` must be discoverable;
- every discovered `og:Module` must declare at least one `og:path`;
- registry files that contain `og:Module` are listed in deterministic order.
"""
from __future__ import annotations

from pathlib import Path
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
OG = Namespace("https://socioprophet.github.io/ontogenesis/og#")


def registry_candidates() -> list[Path]:
    if not CATALOG.exists():
        raise SystemExit("missing catalog/ directory")

    candidates: set[Path] = set()
    for pattern in ("registry.ttl", "*registry*.ttl", "*.registry.ttl"):
        candidates.update(CATALOG.glob(pattern))

    return sorted(path for path in candidates if path.is_file())


def main() -> int:
    candidates = registry_candidates()
    if not candidates:
        raise SystemExit("no registry Turtle files discovered under catalog/")

    discovered_registry_files: list[Path] = []
    module_count = 0
    missing_path: list[str] = []

    for path in candidates:
        graph = Graph()
        graph.parse(path, format="turtle")
        modules = sorted(str(module) for module in graph.subjects(RDF.type, OG.Module))
        if not modules:
            continue

        discovered_registry_files.append(path)
        for module_iri in modules:
            module = next(graph.subjects(RDF.type, OG.Module)) if False else None
        for module in graph.subjects(RDF.type, OG.Module):
            module_count += 1
            paths = list(graph.objects(module, OG.path))
            if not paths:
                missing_path.append(f"{path.relative_to(ROOT)} :: {module}")

    if not discovered_registry_files:
        raise SystemExit("no registry files with og:Module entries discovered")

    if module_count == 0:
        raise SystemExit("no og:Module records discovered")

    if missing_path:
        details = "\n".join(f"- {entry}" for entry in missing_path)
        raise SystemExit("registry module records missing og:path:\n" + details)

    print("OK: registry discovery posture")
    print(f"registry files with modules: {len(discovered_registry_files)}")
    print(f"module records discovered: {module_count}")
    for path in discovered_registry_files:
        print(f"- {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
