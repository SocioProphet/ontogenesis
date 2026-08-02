#!/usr/bin/env python3
"""Validate the symbolic-regression vocabulary module and fixtures.

This focused validator supplements the repo-wide SHACL gate by proving that the
valid symbolic-regression examples conform and that the negative fixtures fail.
It mirrors scripts/validate_corpus_event_semantics.py's structure.

Prior to SocioProphet/ontogenesis#126, this vocabulary (docs/symbolic-regression-
vocabulary.md, vocab/symbolic-regression/sr-assertion.ttl,
shapes/symbolic-regression/sr-assertion.shacl.ttl) had no dedicated validator,
no example fixtures, and no invalid fixtures at all -- unlike the corpus-event-
semantics module, its SHACL shapes were never exercised by any test in this
repo. This script fills that gap and additionally proves the new
mf:hasMethodFamily / carrier-boundary field extension.
"""
from __future__ import annotations

from pathlib import Path
from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocab" / "symbolic-regression" / "sr-assertion.ttl"
METHOD_FAMILY = ROOT / "vocab" / "method-family" / "method-family.ttl"
SHAPES = ROOT / "shapes" / "symbolic-regression" / "sr-assertion.shacl.ttl"
VALID = ROOT / "examples" / "symbolic-regression" / "valid" / "symbolic-regression.valid.ttl"
INVALID_DIR = ROOT / "tests" / "fixtures" / "symbolic-regression" / "invalid"


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
    valid_graph = graph_from([VOCAB, METHOD_FAMILY, VALID])
    if not conforms(valid_graph):
        raise SystemExit("valid symbolic-regression fixture failed SHACL validation")

    invalid_fixtures = sorted(INVALID_DIR.glob("*.ttl"))
    if not invalid_fixtures:
        raise SystemExit("missing invalid symbolic-regression fixtures")

    failures = []
    for fixture in invalid_fixtures:
        data_graph = graph_from([VOCAB, METHOD_FAMILY, fixture])
        if conforms(data_graph):
            failures.append(str(fixture.relative_to(ROOT)))

    if failures:
        raise SystemExit("invalid fixtures unexpectedly passed: " + ", ".join(failures))

    print("OK: symbolic regression valid fixture passed and invalid fixtures failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
