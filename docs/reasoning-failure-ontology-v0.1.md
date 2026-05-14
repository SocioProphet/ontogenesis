# Reasoning Failure Ontology v0.1

Parent: SocioProphet/sociosphere#271 and SocioProphet/ontogenesis#38.

This tranche makes reasoning failure a first-class semantic surface in Ontogenesis. It is intentionally compact: Ontogenesis owns vocabulary, relation semantics, SHACL gates, examples, and registry-local metadata. Runtime systems own execution, trace capture, storage, routing, guardrail actions, metrics, and user-visible search.

## Design posture

A reasoning failure is not a prompt defect by default. It is an evidence-bearing case that ties together a task, failure mode, perturbation or invariant, verifier, trace, evidence receipt, mitigation, residual risk, and regression status.

This gives downstream systems a stable contract:

- AgentPlane records typed traces and termination/verifier decisions.
- Prophet Platform runs perturbation suites and emits receipts.
- Guardrail Fabric maps receipts to runtime actions.
- Policy Fabric gates memory, tools, export, and termination.
- Model Governance Ledger records receipts for promotion, waiver, rollback, and revocation.
- Agent Registry changes authority based on risk posture.
- Sherlock indexes cases and evidence.
- DeliveryExcellence measures recurrence and correction.
- GAIA validates spatial, embodied, multimodal, temporal, and scientific claims.
- SourceOS contracts local exactness, stale-state, and repair evidence.

## Covered failure families

The initial ontology covers cognitive-state failures, bias and framing failures, formal reasoning failures, exactness/tokenization failures, task-specification failures, social reasoning failures, code reasoning failures, causal/temporal failures, multimodal and embodied failures, scientific reasoning failures, and multi-agent failures.

The first concrete examples cover exact-string mutation and directed-relation reversal. Those are deliberately selected because they can be validated with deterministic or schema-backed checks without relying on LLM-as-judge.

## Relation semantics

Relation-bearing tasks must declare directionality, inverse relation where applicable, symmetry profile, and transitivity profile. This is the Ontogenesis hook for preventing reversal curse and two-hop shortcut failures from becoming ambiguous graph semantics.

## SHACL gate

`shapes/reasoning_failure.shacl.ttl` fails closed when a case omits failure mode, task, invariant, verifier, evidence receipt, residual risk, severity, or runtime action. It also requires relation-semantics records to declare direction, symmetry, and transitivity.

## Non-goals

This tranche does not implement the perturbation runner, runtime trace capture, ledger storage, authority revocation, routing, UI, or metrics. Those are owned by downstream issues under the Sociosphere epic.
