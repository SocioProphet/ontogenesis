#!/usr/bin/env python3
"""Validate privacy non-linkability JSON-LD examples.

This validator keeps the privacy lane self-contained:
- positive examples under examples/privacy-nonlinkability/*.jsonld must conform;
- invalid examples under examples/privacy-nonlinkability/invalid/*.invalid.jsonld must fail.

The validator intentionally checks the structural SHACL gates only. It does not
attempt identity-reconstruction analysis, graph reachability analysis, latent
space leakage proofs, or legal compliance verification.
"""
from __future__ import annotations

from pathlib import Path
import sys

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples" / "privacy-nonlinkability"
INVALID_DIR = EXAMPLES_DIR / "invalid"
SHAPES = [
    ROOT / "shapes" / "governed_intelligence.shacl.ttl",
    ROOT / "shapes" / "privacy_nonlinkability.shacl.ttl",
]
ONTOLOGIES = [
    ROOT / "Upper" / "upper-core.ttl",
    ROOT / "Platform" / "GovernedIntelligence" / "governed-intelligence.ttl",
    ROOT / "Platform" / "GovernedIntelligence" / "privacy-nonlinkability.ttl",
]


def load_graph(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.suffix == ".ttl":
            graph.parse(path, format="turtle")
        elif path.suffix == ".jsonld":
            graph.parse(path, format="json-ld")
        else:
            raise ValueError(f"Unsupported graph input: {path}")
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
    positives = sorted(EXAMPLES_DIR.glob("*.jsonld"))
    negatives = sorted(INVALID_DIR.glob("*.invalid.jsonld")) if INVALID_DIR.exists() else []

    if not positives:
        print(f"[FAIL] no positive privacy examples found in {EXAMPLES_DIR}")
        return 1
    if not negatives:
        print(f"[FAIL] no invalid privacy examples found in {INVALID_DIR}")
        return 1

    failures = 0

    for path in positives:
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
        else:
            print(f"[OK] invalid example rejected: {path.relative_to(ROOT)}")
            if "privacyBasis" not in report and "Less than 1 values" not in report:
                print("[WARN] invalid fixture failed, but report did not mention expected missing privacyBasis signal")

    if failures:
        print(f"\n{failures} privacy non-linkability example validation failures.")
        return 1

    print("\nPrivacy non-linkability examples validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
