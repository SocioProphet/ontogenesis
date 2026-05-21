#!/usr/bin/env python3
"""Validate the corpus event semantics module and fixtures.

This focused validator supplements the repo-wide SHACL gate by proving that the
valid corpus-event example conforms and that the negative fixtures fail.
"""
from __future__ import annotations

from pathlib import Path
from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "Platform" / "corpus-event-semantics.ttl"
SHAPES = ROOT / "shapes" / "corpus-event-semantics.shacl.ttl"
VALID = ROOT / "examples" / "corpus-event-semantics" / "valid" / "corpus-event-semantics.valid.ttl"
INVALID_DIR = ROOT / "tests" / "fixtures" / "corpus-event-semantics" / "invalid"


def graph_from(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        if not path.exists():
            raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
        graph.parse(path, format="turtle")
    return graph


def conforms(data_graph: Graph) -> bool:
    shapes_graph = graph_from([SHAPES])
    result, _, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        debug=False,
    )
    if not isinstance(result, bool):
        raise SystemExit(f"unexpected pyshacl result: {result!r}\n{report_text}")
    return result


def main() -> int:
    valid_graph = graph_from([ONTOLOGY, VALID])
    if not conforms(valid_graph):
        raise SystemExit("valid corpus-event-semantics fixture failed SHACL validation")

    invalid_fixtures = sorted(INVALID_DIR.glob("*.ttl"))
    if not invalid_fixtures:
        raise SystemExit("missing invalid corpus-event-semantics fixtures")

    failures = []
    for fixture in invalid_fixtures:
        data_graph = graph_from([ONTOLOGY, fixture])
        if conforms(data_graph):
            failures.append(str(fixture.relative_to(ROOT)))

    if failures:
        raise SystemExit("invalid fixtures unexpectedly passed: " + ", ".join(failures))

    print("OK: corpus event semantics valid fixture passed and invalid fixtures failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
