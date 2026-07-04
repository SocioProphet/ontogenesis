#!/usr/bin/env python3
"""Validate adversarial-scenario SHACL gate examples.

This keeps the adversarial-scenario lane self-contained and gives the gate
failure-output visibility:
- the positive SCOPE-D example must conform to the gate;
- invalid examples under examples/adversarial-scenario/invalid/*.invalid.ttl must
  be rejected, each tripping the specific SCOPE-D safety invariant it violates.

The validator checks the structural SHACL gates only. It does not execute,
simulate, or authorize any adversarial procedure; the examples are governed
non-claims by construction.
"""
from __future__ import annotations

from pathlib import Path
import sys

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
INVALID_DIR = ROOT / "examples" / "adversarial-scenario" / "invalid"
POSITIVES = [ROOT / "examples" / "adversarial-scenario-scope-d-workspace-transduction.ttl"]
SHAPES = [ROOT / "shapes" / "adversarial-scenario.shacl.ttl"]
ONTOLOGIES = [
    ROOT / "Upper" / "upper-core.ttl",
    ROOT / "Domains" / "agentic-purple-team.ttl",
    ROOT / "Domains" / "adversarial-scenario.ttl",
]

# Each invalid fixture must trip a recognisable SCOPE-D safety signal.
EXPECTED_SIGNALS = {
    "runtime-authority-claimed": "runtime authority",
    "memory-writeback-allowed": "durable writeback",
    "claim-promotion-finding": "promotion",
}


def load_graph(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        graph.parse(path, format="turtle")
    return graph


def validate_doc(path: Path) -> tuple[bool, str]:
    data_graph = load_graph(ONTOLOGIES + [path])
    shapes_graph = load_graph(SHAPES)
    conforms, _report_graph, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        debug=False,
    )
    return bool(conforms), str(report_text)


def main() -> int:
    negatives = sorted(INVALID_DIR.glob("*.invalid.ttl")) if INVALID_DIR.exists() else []
    if not all(p.exists() for p in POSITIVES):
        print(f"[FAIL] positive adversarial-scenario example(s) missing: {POSITIVES}")
        return 1
    if not negatives:
        print(f"[FAIL] no invalid adversarial-scenario examples found in {INVALID_DIR}")
        return 1

    failures = 0

    for path in POSITIVES:
        conforms, report = validate_doc(path)
        if conforms:
            print(f"[OK] positive example conforms: {path.relative_to(ROOT)}")
        else:
            failures += 1
            print(f"[FAIL] positive example did not conform: {path.relative_to(ROOT)}")
            print(report)

    for path in negatives:
        conforms, report = validate_doc(path)
        if conforms:
            failures += 1
            print(f"[FAIL] invalid example unexpectedly conformed: {path.relative_to(ROOT)}")
            continue
        print(f"[OK] invalid example rejected: {path.relative_to(ROOT)}")
        signal = next((v for k, v in EXPECTED_SIGNALS.items() if path.name.startswith(k)), None)
        if signal and signal.lower() not in report.lower():
            print(f"[WARN] {path.name} failed, but report did not mention expected signal '{signal}'")

    if failures:
        print(f"\n{failures} adversarial-scenario example validation failures.")
        return 1

    print("\nAdversarial-scenario examples validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
