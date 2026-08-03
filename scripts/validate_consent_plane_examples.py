"""Consent-plane conformance: the ontology self-validates, a conformant instance passes,
and a violating instance fails on exactly the intended fail-closed teeth. Offline."""
import sys, glob
from rdflib import Graph
from pyshacl import validate

def load(paths):
    g = Graph()
    for pat in paths:
        for f in sorted(glob.glob(pat)):
            g.parse(f, format="turtle")
    return g

ONTO = load(["Domains/consent-plane/*.ttl", "shapes/consent_plane.shacl.ttl",
             "Upper/*.ttl", "Domains/agent-system/*.ttl"])
SHAPES = load(["shapes/consent_plane.shacl.ttl"])

def check(name, example, expect):
    dg = load([example])
    conforms, _, txt = validate(dg, shacl_graph=SHAPES, ont_graph=ONTO, inference="rdfs", advanced=True)
    ok = conforms == expect
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: conforms={conforms} (expected {expect})")
    if not conforms:
        for l in txt.splitlines():
            if "Message:" in l: print("   -", l.strip())
    return ok

r = [
  check("conformant-invocation", "examples/consent-plane/conformant-invocation.ttl", True),
  check("violating-invocation",  "examples/consent-plane/invalid/violating-invocation.ttl", False),
]
sys.exit(0 if all(r) else 1)
