# Semantic Enterprise Sector Modules v0.1

## Purpose

This tranche adds first-class sector ontology modules to the semantic-enterprise architecture.

The goal is to move from architecture scaffolding to concrete domain surfaces for:

- finance
- cyber threat intelligence
- cyber-physical investigation
- supply-chain resilience
- defensive command-and-control

Each module is intentionally compact. The modules define governed semantic anchors, not full external-standard copies.

## Added sector modules

### `Domains/finance.ttl`

Covers accounts, transactions, counterparties, financial instruments, beneficial ownership, KYC profiles, AML alerts, sanctions screening, risk scores, and transaction-network patterns.

Primary standards alignment: FIBO.

### `Domains/threat-intel.ttl`

Covers CTI sources, observables, indicators, threat actors, campaigns, malware, vulnerabilities, TTPs, defensive techniques, countermeasures, and attribution assessments.

Primary standards alignment: UCO, D3FEND, and later STIX/TAXII bridge work.

### `Domains/investigation.ttl`

Covers investigations, cases, evidence, digital evidence, physical evidence, traces, investigative actions, custody events, persons of interest, witnesses, location artifacts, hypotheses, and source reports.

Primary standards alignment: CASE and UCO.

### `Domains/supply-chain.ttl`

Covers supply-chain systems, agents, suppliers, manufacturers, distributors, retailers, facilities, components, shipments, purchase orders, bills of lading, disruption risks, mitigations, and alternate sources.

Primary standards alignment: IOF Supply Chain Ontology.

### `Domains/defense-c2.ttl`

Covers missions, capabilities, units, assets, sensors, operational areas, courses of action, operating constraints/rules of engagement, threat assessment, cyber state, logistics state, readiness, and common operational picture artifacts.

Primary standards alignment: DoDAF and CCO-style architecture semantics.

## Added validation and examples

- `shapes/sector_modules.shacl.ttl` — consolidated sector promotion gates.
- `examples/semantic_sector_demo.ttl` — cross-sector fixture exercising finance, CTI, investigation, supply-chain, and C2 classes.
- `contexts/semantic-sectors.context.jsonld` — compact JSON-LD context for sector surfaces.
- `catalog/semantic_sector_registry.ttl` — registry supplement for this tranche.
- `Alignments/sector-domains.ttl` — mapping assertions from the sector modules to external standards.

## Governance posture

These modules are not operational playbooks. They define semantic structures for evidence, provenance, validation, analysis, integration, and defensive governance.

External standards are bridged by explicit `smap:MappingAssertion` records. This keeps Ontogenesis canonical while preserving traceability to external ontology ecosystems.

## Next tranche

The next tranche should add deeper examples and downstream bridge contracts:

1. Finance AML/KYC scenario fixture with beneficial ownership and sanctions-screening provenance.
2. Threat-intel fixture with STIX/TAXII exchange notes and D3FEND mitigation mapping.
3. Investigation fixture with cyber/physical evidence fusion and chain-of-custody timeline.
4. Supply-chain fixture with multi-tier dependency and alternate-source propagation.
5. Defense/C2 fixture with common operational picture, readiness, logistics, and cyber-state overlays.
