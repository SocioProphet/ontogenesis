from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
DIRS = ["Upper","Middle","Lower","Domains","Platform","prophet","epi","catalog","shapes"]

def test_all_ttl_parse():
    ttl_files = []
    for d in DIRS:
        p = ROOT / d
        if p.exists():
            ttl_files.extend(p.rglob("*.ttl"))
    assert ttl_files, "No Turtle files found"
    for f in ttl_files:
        g = Graph()
        g.parse(f, format="turtle")
