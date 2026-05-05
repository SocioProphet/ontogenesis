# Downstream Import Bridge v0.1

## Purpose

This note defines how downstream platform consumers should import semantic-enterprise scenario assets from Ontogenesis without replacing Ontogenesis as the canonical authored source.

Ontogenesis owns canonical ontology modules, mapping assertions, SHACL gates, examples, registry entries, and governance metadata. Downstream systems may compile, index, materialize, query, or display the assets, but compiled artifacts must retain traceability to Ontogenesis source paths, canonical IRIs, module versions, and validation gates.

## Required import surfaces

A downstream importer should read:

- `catalog/registry.ttl`
- `catalog/semantic_enterprise_registry.ttl`
- `catalog/semantic_sector_registry.ttl`
- `catalog/semantic_sector_scenarios_registry.ttl`
- `Middle/kg-lifecycle.ttl`
- `Middle/semantic-mapping.ttl`
- `Middle/named-graph-governance.ttl`
- `Domains/finance.ttl`
- `Domains/threat-intel.ttl`
- `Domains/investigation.ttl`
- `Domains/supply-chain.ttl`
- `Domains/defense-c2.ttl`
- `Alignments/sector-domains.ttl`
- `examples/scenarios/*.ttl`
- `examples/named-graphs/*.ttl`
- `examples/queries/*.rq`
- `shapes/sector_modules.shacl.ttl`
- `shapes/kg_lifecycle.shacl.ttl`
- `shapes/named_graph_governance.shacl.ttl`
- `shapes/semantic_mapping.shacl.ttl`

## Preservation requirements

Every compiled downstream artifact should preserve:

- source file path
- source commit or release tag
- canonical subject IRI
- RDF type set
- module or registry entry when available
- applicable SHACL gate path
- named graph URI when available
- access class and trust profile when available
- mapping assertion provenance for external-standard bridges

## Platform consumer contracts

### Prophet Platform

Prophet Platform should treat Ontogenesis assets as canonical semantic inputs for API contracts, runtime capability descriptors, and domain-aware service surfaces. It should not mutate Ontogenesis semantics at runtime. Runtime-derived forms should reference their source ontology module and scenario fixture.

### Sherlock Search

Sherlock Search should index labels, classes, properties, examples, mapping assertions, named graph metadata, and SPARQL examples as searchable evidence. Search results should expose provenance back to Ontogenesis paths and commit/release identifiers.

### AgentPlane

AgentPlane should use the semantic modules as admission and context boundaries for agent tasks. It should preserve the distinction between authored ontology terms, example facts, named graph metadata, and runtime observations.

### PolicyFabric

PolicyFabric should consume SHACL gates and named graph governance metadata as policy inputs. It should not translate SHACL failures into silent warnings; gate failures should remain explicit promotion blockers.

### SourceOS

SourceOS should use the supply-chain, named-graph, provenance, identity, and governance surfaces to describe software artifact lineage, local-first state context, release provenance, rollback evidence, and system trust surfaces.

### DeliveryExcellence

DeliveryExcellence should consume scenario registries and validation outcomes as measurable artifacts: module coverage, scenario coverage, query coverage, gate coverage, validation pass/fail, release evidence, and adoption status.

## Non-goals

This import bridge does not define production storage, production access control, operational playbooks, incident response procedures, or live collection logic. Those belong in downstream systems and must remain governed by their own safety, security, and deployment controls.

## Next hardening step

The next tranche should add a lightweight importer test contract that enumerates registered semantic-enterprise files, checks that all referenced source paths exist, and verifies that each scenario has at least one query and one named graph governance record.
