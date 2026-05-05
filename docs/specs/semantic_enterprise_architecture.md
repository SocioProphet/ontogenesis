# Semantic enterprise architecture

## Purpose

This specification integrates the sector ontology architecture into Ontogenesis as governed source, not as an informal research note.

Ontogenesis is the canonical authored ontology and governance repository. Downstream graph stores, ingestion jobs, runtime reasoners, dashboards, SOAR systems, C2 systems, and business applications consume compiled or materialized artifacts from Ontogenesis, but they do not replace Ontogenesis as the source of semantic truth.

The target architecture is:

`Ontogenesis authored modules -> registry + SHACL + JSON-LD examples -> dist/audit/ledger -> downstream graph/runtime/query systems`

## Architectural stance

The architecture is hybrid.

1. Ontogenesis upper and middle modules provide the stable enterprise semantic substrate.
2. Domain modules provide local canonical semantics for finance, threat intelligence, investigation, supply chain, defense/C2, business, identity, product/service, and platform work.
3. Alignment modules map Ontogenesis concepts to external standards such as gist, FIBO, UCO/CASE, D3FEND, IOF SCO, DoDAF, and CCO.
4. SHACL bundles define promotion gates and quality constraints.
5. Examples and JSON-LD contexts make the model executable in CI and usable by downstream import bridges.

The repo should generally map to external ontologies rather than blindly vendoring large external trees. Vendoring is acceptable only when licensing, size, stability, and operational need justify it. The default is governed alignment by explicit mapping assertions.

## What Ontogenesis owns

Ontogenesis owns:

- canonical classes and properties
- module boundaries and SemVer
- namespace discipline
- import graph discipline
- alignment assertions and mapping metadata
- SHACL promotion gates
- JSON-LD contexts and examples
- registry entries
- deterministic dist/audit/ledger/signature/SBOM posture

## What downstream systems own

Runtime and application systems own:

- RDF store or graph database deployment
- named graph storage and access-control enforcement
- ingestion, extraction, and entity-resolution jobs
- materialized inference graphs
- SPARQL endpoint hosting
- BI, SOAR, C2, search, and application integration
- runtime scoring, ranking, workflow execution, and report generation

No downstream compiled artifact should lose traceability back to the Ontogenesis module path, SemVer, canonical IRI, registry record, and applicable SHACL gate.

## Core module families

### Middle lifecycle modules

- `Middle/kg-lifecycle.ttl` — knowledge creation, hosting, curation, deployment, ingestion, validation, reasoning, and feedback-loop vocabulary.
- `Middle/semantic-mapping.ttl` — external ontology, alignment, mapping assertion, mapping status, confidence, and approval vocabulary.
- `Middle/named-graph-governance.ttl` — named graph context, trust, source, owner, access class, lifecycle, and retention vocabulary.

### Alignment modules

- `Alignments/gist.ttl` — bridge from Ontogenesis primitives and business concepts to gist-style enterprise primitives.
- `Alignments/fibo.ttl` — bridge from business/legal/financial concepts to FIBO financial-sector semantics.
- `Alignments/uco-case.ttl` — bridge from cyber and investigation semantics to UCO/CASE-style cyber and forensic concepts.
- `Alignments/d3fend.ttl` — bridge from defensive controls to D3FEND-style defensive techniques.
- `Alignments/iof-sco.ttl` — bridge from business/product/platform/supply-chain concepts to IOF SCO-style supply-chain structure.
- `Alignments/dodaf-cco.ttl` — bridge from system, process, capability, and operational concepts to DoDAF/CCO-style defense architecture concepts.

### Sector domain modules

Future sector modules should land as first-class domain modules, not prose-only notes:

- `Domains/finance.ttl`
- `Domains/threat-intel.ttl`
- `Domains/investigation.ttl`
- `Domains/supply-chain.ttl`
- `Domains/defense-c2.ttl`

Each sector module must have a registry entry, SHACL bundle, example graph, and at least one alignment path to relevant external standards.

## Knowledge graph lifecycle contract

The minimum lifecycle vocabulary covers:

1. Knowledge creation: extraction, mapping, enrichment, provenance creation, and source-to-RDF transformation.
2. Knowledge hosting: graph storage, named graph partitioning, access class, trust context, and SPARQL exposure.
3. Knowledge curation: SHACL validation, entity resolution, inconsistency handling, enrichment, and feedback to upstream mapping/extraction rules.
4. Knowledge deployment and consumption: queries, reasoning, visualization, runtime application consumption, and generated reports.

Every production pipeline should be expressible as an instance of this lifecycle, with source systems, mapping rules, graph partitions, validation runs, and deployment surfaces captured as first-class semantic records.

## Mapping and alignment discipline

Mappings are first-class governed resources.

Every mapping assertion should declare:

- source concept
- target concept or external standard concept
- mapping predicate such as `rdfs:subClassOf`, `owl:equivalentClass`, `skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`, or `skos:narrowMatch`
- confidence
- status
- source standard
- reviewer or approver where applicable
- provenance

Approximate external alignment should use SKOS matching terms. Strong equivalence should be rare and justified.

## Named graph governance

Named graphs model context, not just storage partitioning.

A named graph should record:

- graph URI
- source system
- graph owner
- trust level
- access class
- lifecycle phase
- effective date or epoch where relevant
- retention policy

This supports source isolation, trust modeling, provenance, versioning, access control, and conflicting-perspective handling.

## SHACL posture

Semantic enterprise modules must be gated.

Minimum gates:

- mapping assertions must declare source, target, predicate, confidence, and status
- named graphs must declare graph URI, source system, trust level, access class, and owner
- lifecycle pipelines must declare at least one phase and at least one governed artifact or graph output
- sector modules must define domain-specific required fields before promotion

## Release posture

This architecture is not considered integrated until the repo can validate, build, and audit it through the existing Ontogenesis workflow:

1. RDF parse validation
2. SHACL gates
3. JSON-LD roundtrip checks
4. dist build
5. ledger build and verification
6. SBOM generation
7. release signing where applicable

## Implementation sequence

1. Land middle lifecycle, mapping, and named-graph modules.
2. Land alignment scaffolds to gist, FIBO, UCO/CASE, D3FEND, IOF SCO, and DoDAF/CCO.
3. Register the modules in `catalog/registry.ttl` and `catalog/registry.jsonld`.
4. Add SHACL gates for mapping and graph governance.
5. Add a minimal example graph for a semantic enterprise pipeline.
6. Add sector domain modules in focused tranches.
7. Extend downstream compiler/runtime import bridges to preserve canonical IRI, module path, SemVer, registry, and SHACL provenance.
