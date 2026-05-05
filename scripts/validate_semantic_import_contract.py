#!/usr/bin/env python3
"""Validate semantic-enterprise import contract coverage.

This script is intentionally lightweight and stdlib-only. It checks that the
semantic-enterprise scenario, query, named-graph, registry, and downstream
import-bridge surfaces remain connected by path and by expected coverage.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCENARIOS = {
    "finance": {
        "scenario": "examples/scenarios/finance_aml_kyc_demo.ttl",
        "query": "examples/queries/finance_aml_kyc.rq",
        "graph_uri_fragment": "graphs/scenarios/finance-aml-kyc",
    },
    "threat-intel": {
        "scenario": "examples/scenarios/threat_intel_lifecycle_demo.ttl",
        "query": "examples/queries/threat_intel_lifecycle.rq",
        "graph_uri_fragment": "graphs/scenarios/threat-intel-lifecycle",
    },
    "investigation": {
        "scenario": "examples/scenarios/investigation_custody_timeline_demo.ttl",
        "query": "examples/queries/investigation_custody_timeline.rq",
        "graph_uri_fragment": "graphs/scenarios/investigation-custody",
    },
    "supply-chain": {
        "scenario": "examples/scenarios/supply_chain_resilience_demo.ttl",
        "query": "examples/queries/supply_chain_resilience.rq",
        "graph_uri_fragment": "graphs/scenarios/supply-chain-resilience",
    },
    "defense-c2": {
        "scenario": "examples/scenarios/defense_c2_cop_demo.ttl",
        "query": "examples/queries/defense_c2_cop.rq",
        "graph_uri_fragment": "graphs/scenarios/defense-c2-cop",
    },
}

REQUIRED_IMPORT_BRIDGE_CONSUMERS = [
    "Prophet Platform",
    "Sherlock Search",
    "AgentPlane",
    "PolicyFabric",
    "SourceOS",
    "DeliveryExcellence",
]


def require_file(errors: list[str], path: str) -> None:
    if not (ROOT / path).is_file():
        errors.append(f"missing required file: {path}")


def require_contains(errors: list[str], path: str, needle: str, context: str) -> None:
    file_path = ROOT / path
    if not file_path.is_file():
        errors.append(f"cannot check {context}; missing file: {path}")
        return
    text = file_path.read_text(encoding="utf-8")
    if needle not in text:
        errors.append(f"{context}: expected {path} to contain {needle!r}")


def main() -> int:
    errors: list[str] = []

    scenario_registry = "catalog/semantic_sector_scenarios_registry.ttl"
    query_registry = "catalog/semantic_query_import_registry.ttl"
    named_graphs = "examples/named-graphs/semantic_sector_named_graphs.ttl"
    import_bridge = "docs/semantic-enterprise/downstream-import-bridge-v0.1.md"

    for path in [scenario_registry, query_registry, named_graphs, import_bridge]:
        require_file(errors, path)

    for sector, spec in SCENARIOS.items():
        scenario_path = spec["scenario"]
        query_path = spec["query"]
        graph_uri_fragment = spec["graph_uri_fragment"]

        require_file(errors, scenario_path)
        require_file(errors, query_path)

        require_contains(errors, scenario_registry, scenario_path, f"{sector} scenario registry coverage")
        require_contains(errors, query_registry, query_path, f"{sector} query registry coverage")
        require_contains(errors, named_graphs, scenario_path, f"{sector} named graph sourceSystem coverage")
        require_contains(errors, named_graphs, graph_uri_fragment, f"{sector} named graph URI coverage")

    for consumer in REQUIRED_IMPORT_BRIDGE_CONSUMERS:
        require_contains(errors, import_bridge, consumer, f"downstream consumer {consumer} coverage")

    if errors:
        print("Semantic import contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Semantic import contract validation passed.")
    print(f"Validated {len(SCENARIOS)} scenarios, queries, named graph records, and import bridge coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
