#!/usr/bin/env python3
"""Validate the model-plane SHACL gate examples (T7-8).

Keeps the model-plane lane self-contained and gives the residency gate
failure-output visibility:
- the positive example must conform to the residency constraints;
- each invalid fixture under examples/model-plane/invalid/*.invalid.ttl must be
  rejected, tripping the specific residency / receipt / biometric invariant it
  violates.

A control never observed refusing is indistinguishable from no control, so the
negatives are asserted here rather than merely documented.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGIES = [
    ROOT / "Upper" / "upper-core.ttl",
    ROOT / "Domains" / "model-plane" / "inference-provider.ttl",
]
SHAPES = ROOT / "shapes" / "model-plane" / "residency-constraints.shacl.ttl"
POSITIVE = ROOT / "examples" / "model-plane" / "model-plane-providers.ttl"
INVALID_DIR = ROOT / "examples" / "model-plane" / "invalid"

# Each invalid fixture must trip a recognisable model-plane safety signal.
EXPECTED_SIGNALS = {
    "ondevice-with-network": "networkCapability",
    "escalation-on-device": "escalationPermitted",
    "biometric-offdevice": "biometric",
    "no-receipt": "receipt",
    "missing-network-declaration": "networkCapability",
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
        data_graph=data,
        shacl_graph=_shapes(),
        inference="rdfs",
        abort_on_first=False,
        advanced=True,
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
    if len(stems) < 3:
        fail(f"expected >=3 invalid fixtures, found {len(stems)}")

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
        f"OK: model-plane SHACL gate — positive conforms; "
        f"{len(stems)} invalid fixtures each rejected on the expected invariant"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
