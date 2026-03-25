from pathlib import Path
from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

def load_all(dirs):
    g = Graph()
    for d in dirs:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.ttl")):
                g.parse(f, format="turtle")
    return g

def test_shacl_conforms():
    data = load_all(["Upper","Middle","Lower","Domains","Platform","prophet","epi","catalog"])
    shapes = load_all(["shapes","prophet/shapes","epi/shapes"])
    conforms, _, _ = validate(data_graph=data, shacl_graph=shapes, inference="rdfs", advanced=True)
    assert conforms
