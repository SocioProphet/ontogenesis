# Corpus Event Semantics

Status: v0.1 semantic/validation tranche. Cross-referenced against the Kautz/NSR
method-family taxonomy per `SocioProphet/ontogenesis#126` (see "Neuro-symbolic
method-family cross-reference" below).

This module defines the first Ontogenesis carrier vocabulary for the Watson/Cyc/Semantic-Web/CHRONOS corpus substrate merged in `SocioProphet/sociosphere#334` and coordinated through `SocioProphet/sociosphere#335`.

## Purpose

The module provides semantic carriers for the first deployable cybernetic-loop path:

```text
EvidenceBundle -> EventInstance -> ActionProposal -> PolicyDecision -> AuditEvent
```

Ontogenesis owns only the semantic/schema side of this path. It does not own Sherlock evidence assembly, Policy Fabric decisions, Agentplane execution, or Model Governance Ledger audit storage.

## Added surfaces

```text
Platform/corpus-event-semantics.ttl
shapes/corpus-event-semantics.shacl.ttl
examples/corpus-event-semantics/valid/corpus-event-semantics.valid.ttl
tests/fixtures/corpus-event-semantics/invalid/*.ttl
scripts/validate_corpus_event_semantics.py
catalog/corpus-event-semantics-registry.ttl
vocab/method-family/method-family.ttl  (shared; see "Neuro-symbolic method-family cross-reference" below)
```

## Core classes

- `ces:CorpusEvidenceBundle`
- `ces:SourceProvenance`
- `ces:EventSchema`
- `ces:EventInstance`
- `ces:EventPrediction`
- `ces:CausalRelationCandidate`
- `ces:SemanticTableAnnotationTask`
- `ces:ColumnOntologyLink`
- `ces:DiagnosticFinding`
- `ces:ConceptHierarchyProbe`
- `ces:KGSubgraphFinding`

## Required validation behavior

The focused validator proves:

- a valid corpus-event example passes SHACL;
- an event instance without provenance fails;
- a causal candidate without confidence fails;
- a diagnostic finding without evidence fails.

Run:

```bash
make validate-corpus-event-semantics
```

The target is also included in:

```bash
make validate
```

## Neuro-symbolic method-family cross-reference

`SocioProphet/ontogenesis#126` asked whether this module's carrier classes should adopt or cross-reference the ASU/Kautz neuro-symbolic method-family taxonomy from `sociosphere/docs/integration/neurosymbolic-chronos-alignment.md`. Rather than adopt it wholesale (that alignment doc's own text frames this as "a request to evaluate the connection, not a mandate ... to adopt any specific field set"), this module adopts it where it maps onto a real existing gap: `ces:CausalRelationCandidate` (a natural NeurASP/dILP-style output) and `ces:KGSubgraphFinding` (a natural Deep-Ontological-Network/RRN-style output) may now carry `mf:hasMethodFamily` and the alignment doctrine's carrier-boundary fields (`mf:groundingStatus`, `mf:validationStatus`, `mf:methodOutputType`, `mf:explanationTraceRef`, `mf:owningAuthorityPlane`) from the shared `vocab/method-family/method-family.ttl` module.

Both fields are optional and additive: an existing causal candidate or KG subgraph finding that declares no method family is unaffected. Once `mf:hasMethodFamily` is declared, SHACL requires the remaining carrier-boundary fields alongside it, mirroring the same conditional pattern used in `docs/symbolic-regression-vocabulary.md`'s `SRAssertionProposal` extension.

This module does not redefine CHRONOS's canonical carrier model; it only lets its own carrier classes declare which neuro-symbolic method family (if any) produced a given candidate or finding.

## Boundary

This module does not implement:

- Sherlock evidence retrieval;
- external bibliography harvesting;
- KGQA runtime;
- Agentplane action execution;
- Policy Fabric authorization;
- Model Governance Ledger audit storage;
- graph database deployment.

It provides vocabulary, examples, SHACL constraints, and validation fixtures only.
