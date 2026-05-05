# Semantic Enterprise Integration

This directory indexes the first semantic-enterprise tranche.

The purpose of this tranche is to turn sector ontology architecture into governed Ontogenesis source files. It adds cross-domain lifecycle, semantic mapping, named graph governance, external-standard alignment scaffolds, SHACL promotion gates, and an executable example graph.

## Specification

- `../specs/semantic_enterprise_architecture.md` — architecture, ownership split, lifecycle contract, alignment discipline, named graph governance, SHACL posture, and implementation sequence.

## Middle-layer modules

- `../../Middle/kg-lifecycle.ttl` — knowledge creation, hosting, curation, deployment, validation, reasoning, SPARQL endpoint, and feedback-loop vocabulary.
- `../../Middle/semantic-mapping.ttl` — external ontology, mapping assertion, mapping predicate, confidence, status, and review vocabulary.
- `../../Middle/named-graph-governance.ttl` — named graph URI, source system, trust profile, access policy, lifecycle phase, binding epoch, and retention vocabulary.

## Alignment modules

- `../../Alignments/gist.ttl`
- `../../Alignments/fibo.ttl`
- `../../Alignments/uco-case.ttl`
- `../../Alignments/d3fend.ttl`
- `../../Alignments/iof-sco.ttl`
- `../../Alignments/dodaf-cco.ttl`

These modules intentionally map to external standards instead of vendoring full external ontology trees.

## SHACL gates

- `../../shapes/kg_lifecycle.shacl.ttl`
- `../../shapes/semantic_mapping.shacl.ttl`
- `../../shapes/named_graph_governance.shacl.ttl`

## Example fixture

- `../../examples/semantic_enterprise_pipeline.ttl` — minimal pipeline fixture showing lifecycle phases, governed graph output, named graph metadata, trust/access surfaces, SPARQL exposure, and one mapping assertion.

## Registry supplement

- `../../catalog/semantic_enterprise_registry.ttl`
- `../../catalog/semantic_enterprise_registry.jsonld`

These supplement files index this tranche without rewriting the primary registry while this branch is behind current `main`. A follow-up rebase-safe PR should merge the supplement entries into `catalog/registry.ttl` and `catalog/registry.jsonld`.

## Next functional tranche

The next tranche should add sector modules and gates:

- `Domains/finance.ttl` + `shapes/finance.shacl.ttl`
- `Domains/threat-intel.ttl` + `shapes/threat_intel.shacl.ttl`
- `Domains/investigation.ttl` + `shapes/investigation.shacl.ttl`
- `Domains/supply-chain.ttl` + `shapes/supply_chain.shacl.ttl`
- `Domains/defense-c2.ttl` + `shapes/defense_c2.shacl.ttl`

Each sector module should include at least one example graph and at least one explicit alignment path through the semantic mapping vocabulary.
