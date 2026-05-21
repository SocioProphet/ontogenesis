# Corpus Event Semantics

Status: v0.1 semantic/validation tranche.

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
