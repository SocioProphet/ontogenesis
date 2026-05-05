# Semantic Enterprise Sector Scenarios v0.1

This tranche adds scenario fixtures for the merged sector modules.

## Fixtures

- `examples/scenarios/finance_aml_kyc_demo.ttl`
- `examples/scenarios/threat_intel_lifecycle_demo.ttl`
- `examples/scenarios/investigation_custody_timeline_demo.ttl`
- `examples/scenarios/supply_chain_resilience_demo.ttl`
- `examples/scenarios/defense_c2_cop_demo.ttl`

Each fixture is written as RDF/Turtle and is intended to run through the existing Ontogenesis parse, SHACL, JSON-LD, dist, ledger, and SBOM validation flow.

The scenario fixtures are deliberately synthetic and non-operational. They exercise evidence, provenance, role, risk, logistics, readiness, and governance surfaces without encoding procedural instructions.

## Follow-up

Next work should add SPARQL query examples, named-graph governance examples, and downstream import-bridge notes for platform consumers.
