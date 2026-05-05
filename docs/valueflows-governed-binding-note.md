# ValueFlows governed binding note

This note records the current position of the `bindings/valueflows_governed/` lane inside `ontogenesis`.

## What this lane is

The ValueFlows governed lane is a compact governed binding and runtime proof surface for:

- process-scoped task coordination
- delegated authority
- capability-grant–based overrides
- deterministic replay and checkpoint hashing
- policy runtime checks
- compact-bundle execution for CI and local validation
- ontology-native terminal-state semantics for completed, canceled, revoked, and expired states

It is intentionally narrower than a full ontology module family.

## Why it belongs in ontogenesis

`ontogenesis` is already the ontology genesis, mapping/binding, provenance, policy-aware validation, and JSON-LD boundary-surface substrate for the broader stack. The ValueFlows governed lane is not a detached product repo; it is a governed binding surface that belongs inside this ontology-and-validation substrate.

## Current implementation surfaces

Current repo surfaces for this lane include:

- `docs/specs/valueflows-governed-canonical-v0.4.md`
- `docs/specs/valueflows-governed-canonical-v0.4-landing-plan.md`
- `bindings/valueflows_governed/README.md`
- `bindings/valueflows_governed/Makefile`
- `bindings/valueflows_governed/compact-bundle.v1.json`
- `bindings/valueflows_governed/valueflows-governed.context.jsonld`
- `bindings/valueflows_governed/tools/*.py`
- `bindings/valueflows_governed/policies/rego/*.rego`
- `shapes/valueflows-governed.shacl.ttl`
- `examples/valueflows-governed-task-flow-demo.jsonld`
- `.github/workflows/valueflows-governed-ci.yml`

## What it currently proves

This lane currently proves a compact runtime slice for:

- delegated task offer
- delegated task completion override
- delegated task assignment override
- denial of unauthorized assignment override
- deterministic replay against expected outputs

It also now defines ontology-native semantics for:

- completed process runs requiring `completedAt`
- canceled process runs requiring `canceledAt` and `canceledBy`
- revoked delegations requiring `revokedAt` and `revokedBy`
- revoked capability grants requiring `revokedAt` and `revokedBy`
- completed and canceled tasks carrying terminal-state timestamps and authorities

## What it does not yet prove

Missing or partial surfaces still include:

- runtime replay fixtures for revocation and terminal-state lockout behavior
- SHIR projection and receipt mapping
- module catalog / registry alignment beyond documentation references
- Memory Mesh persistence/reconstruction for ValueFlows event logs and checkpoints
- AgentPlane / Policy Fabric consumption of ValueFlows process/task authority as a governed execution subject

## Correct next lift

The right next lift is runtime and projection evidence, not wider ontology sprawl:

1. update the compact runtime bundle and replay fixtures to prove terminal-state lockouts
2. add a ValueFlows-to-SHIR projection manifest and receipt example
3. then wire ValueFlows event/checkpoint artifacts into Memory Mesh or AgentPlane consumers

## Design rule

This lane should remain a narrow, executable, governed binding. It should not become a dumping ground for every business or workflow concept in the repo.
