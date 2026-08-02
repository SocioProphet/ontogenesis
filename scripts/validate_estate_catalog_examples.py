#!/usr/bin/env python3
"""Validate the estate-catalog SHACL gate examples.

The estate-catalog binding layer must actually refuse malformed catalog data, or
it is a control never observed refusing. Asserts:
  * the positive mini-estate conforms;
  * each invalid fixture under examples/estate-catalog/invalid/*.invalid.ttl is
    rejected on the specific binding invariant it violates (unowned entry,
    unlicensed model, status outside the closed lifecycle set).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGIES = [
    ROOT / "Upper" / "upper-core.ttl",
    ROOT / "Domains" / "metadata.ttl",
    ROOT / "Domains" / "data-reference.ttl",
    ROOT / "Domains" / "service-reference.ttl",
    ROOT / "Domains" / "environment-reference.ttl",
    ROOT / "Domains" / "org-legal.ttl",
    ROOT / "Domains" / "model-plane" / "inference-provider.ttl",
    ROOT / "Domains" / "estate-catalog" / "estate-catalog.ttl",
]
SHAPES = ROOT / "shapes" / "estate-catalog" / "estate-catalog.shacl.ttl"
POSITIVE = ROOT / "examples" / "estate-catalog" / "estate-catalog-ok.ttl"
INVALID_DIR = ROOT / "examples" / "estate-catalog" / "invalid"

EXPECTED_SIGNALS = {
    "catalog-entry-no-owner": "owner",
    "model-no-license": "license",
    "catalog-entry-bad-status": "status",
}


def _base() -> Graph:
    g = Graph()
    for f in ONTOLOGIES:
        g.parse(f, format="turtle")
    return g


def _shapes() -> Graph:
    g = Graph()
    g.parse(SHAPES, format="turtle")
    return g


def _validate(data_file: Path) -> tuple[bool, str]:
    data = _base()
    data.parse(data_file, format="turtle")
    conforms, _report, text = validate(
        data_graph=data, shacl_graph=_shapes(), inference="rdfs", abort_on_first=False, advanced=True
    )
    return conforms, text


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> int:
    conforms, text = _validate(POSITIVE)
    if not conforms:
        fail(f"positive example must conform but did not:\n{text}")

    stems = sorted(p for p in INVALID_DIR.glob("*.invalid.ttl"))
    found = {p.name.replace(".invalid.ttl", "") for p in stems}
    missing = set(EXPECTED_SIGNALS) - found
    if missing:
        fail(f"expected invalid fixtures missing: {sorted(missing)}")

    for path in stems:
        key = path.name.replace(".invalid.ttl", "")
        conforms, text = _validate(path)
        if conforms:
            fail(f"invalid fixture was ACCEPTED but must be rejected: {path.name}")
        signal = EXPECTED_SIGNALS.get(key)
        if signal is None:
            fail(f"no expected signal registered for fixture {key}")
        if signal not in text:
            fail(f"{path.name}: rejected but did not trip expected signal {signal!r}")

    print(
        f"OK: estate-catalog SHACL gate — positive conforms; "
        f"{len(stems)} invalid fixtures each rejected on the expected invariant"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
