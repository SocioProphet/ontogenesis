#!/usr/bin/env python3
import argparse, yaml
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF

EPI = Namespace("https://socioprophet.github.io/ontogenesis/epi#")
NL  = Namespace("https://socioprophet.github.io/ontogenesis/noether#")

def to_uri(base, name): return URIRef(base + name)

def main():
    ap = argparse.ArgumentParser(description="Convert TritFabric quantum: block YAML → EPI TTL")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default="urn:epi:quantum:")
    args = ap.parse_args()

    data = yaml.safe_load(open(args.inp, "r", encoding="utf-8"))
    q = data.get("quantum", {})

    g = Graph(); g.bind("epi", EPI); g.bind("nl", NL)

    cfg = to_uri(args.base, "config")
    g.add((cfg, RDF.type, EPI.TritQuantumConfig))
    g.add((cfg, EPI.provider, Literal(q.get("provider","aer"))))
    prefer = q.get("backend_policy", {}).get("prefer", [])
    if prefer:
        g.add((cfg, EPI.preferBackends, Literal(",".join(prefer))))
    budget = int(q.get("backend_policy", {}).get("qubit_budget", 64))

    for t in q.get("tasks", []) or []:
        name = t.get("name","task")
        s = to_uri(args.base, name)
        if "observable" in t:
            g.add((s, RDF.type, EPI.ChargeEstimationTask))
            g.add((s, EPI.observable, Literal(t.get("observable",""))))
        else:
            g.add((s, RDF.type, EPI.QAOATask))
            if "p_layers" in t: g.add((s, EPI.qaoaLayers, Literal(int(t["p_layers"]))))
            if "graph" in t: g.add((s, EPI.graphSpec, Literal(t["graph"])))
        g.add((s, EPI.qubitBudget, Literal(budget)))

        # link to a Noether layer hint if algebra/group given
        if "algebra" in t or "group" in t:
            layer = to_uri(args.base, f"{name}:layer")
            g.add((layer, RDF.type, NL.Layer))
            if "algebra" in t: g.add((layer, NL.algebra, Literal(t["algebra"])))
            if "group" in t:   g.add((layer, NL.group, Literal(t["group"])))
            g.add((s, EPI.supportsLayer, layer))

        # backend entity
        be = to_uri(args.base, "backend")
        if q.get("provider","aer") == "ibm":
            g.add((be, RDF.type, EPI.IBMBackend))
        else:
            g.add((be, RDF.type, EPI.AerBackend))
        g.add((s, EPI.usesBackend, be))

        # mitigation
        for m in q.get("estimator",{}).get("mitigation",[]) or []:
            mm = to_uri(args.base, f"mitigation:{m}")
            g.add((mm, RDF.type, EPI.Mitigation))
            g.add((mm, EPI.mitigationName, Literal(m)))
            g.add((s, EPI.usesMitigation, mm))

        g.add((cfg, EPI.hasTask, s))

    g.serialize(destination=args.out, format="turtle")
    print(f"[epi] wrote {args.out}")

if __name__ == "__main__":
    main()
