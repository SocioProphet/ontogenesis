# Semantic Enterprise Query and Import v0.1

This tranche adds query and import surfaces for the semantic-enterprise scenarios.

## Added query examples

- `examples/queries/finance_aml_kyc.rq`
- `examples/queries/threat_intel_lifecycle.rq`
- `examples/queries/investigation_custody_timeline.rq`
- `examples/queries/supply_chain_resilience.rq`
- `examples/queries/defense_c2_cop.rq`

The queries are read-only SPARQL examples over the synthetic scenario fixtures.

## Added governance fixture

- `examples/named-graphs/semantic_sector_named_graphs.ttl`

This fixture binds sector scenario files to named graph URI, source system, access class, trust profile, lifecycle phase, effective date, and perspective label metadata.

## Added import bridge contract

- `docs/semantic-enterprise/downstream-import-bridge-v0.1.md`

The import bridge defines the surfaces downstream systems should ingest and what provenance they must preserve.

## Registry

- `catalog/semantic_query_import_registry.ttl`

This registry supplement indexes the query files, named graph governance fixture, and import bridge note.

## Follow-up

Next work should add lightweight importer tests that ensure registered paths exist and each scenario has a query plus a named graph governance record.
