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
- terminal/revocation lockout proof for delegated authority closure and process completion closure
- initial SHIR projection and receipt mapping

It is intentionally narrower than a full ontology module family.

## Why it belongs in ontogenesis

`ontogenesis` is already the ontology genesis, mapping/binding, provenance, policy-aware validation, and JSON-LD boundary-surface substrate for the broader stack. The ValueFlows governed lane is not a detached product repo; it is a governed binding surface that belongs inside this ontology-and-validation substrate.

## Current implementation surfaces

Current repo surfaces for this lane include:

- `docs/specs/valueflows-governed-canonical-v0.4.md`
- `docs/specs/valueflows-governed-canonical-v0.4-landing-plan.md`
- `docs/valueflows-to-shir-projection.md`
- `bindings/valueflows_governed/README.md`
- `bindings/valueflows_governed/Makefile`
- `bindings/valueflows_governed/compact-bundle.v1.json`
- `bindings/valueflows_governed/valueflows-governed.context.jsonld`
- `bindings/valueflows_governed/valueflows-to-shir.projection.v0.1.json`
- `bindings/valueflows_governed/tools/*.py`
- `bindings/valueflows_governed/policies/rego/*.rego`
- `bindings/valueflows_governed/fixtures/terminal_lockout.events.ndjson`
- `bindings/valueflows_governed/fixtures/terminal_lockout.expected.json`
- `shapes/valueflows-governed.shacl.ttl`
- `examples/valueflows-governed-task-flow-demo.jsonld`
- `examples/valueflows-shir-receipt.example.json`
- `.github/workflows/valueflows-governed-ci.yml`

## What it currently proves

This lane currently proves a compact runtime slice for:

- delegated task offer
- delegated task completion override
- delegated task assignment override
- denial of unauthorized assignment override
- deterministic replay against expected outputs

It also defines ontology-native semantics for:

- completed process runs requiring `completedAt`
- canceled process runs requiring `canceledAt` and `canceledBy`
- revoked delegations requiring `revokedAt` and `revokedBy`
- revoked capability grants requiring `revokedAt` and `revokedBy`
- completed and canceled tasks carrying terminal-state timestamps and authorities

The terminal lockout fixture proves:

- revoked capability grants block delegated task offers
- revoked delegations close delegated authority
- completed process runs block later task offers, even from the coordinator

The SHIR projection manifest now defines how the lane projects into:

- `shir:Context`
- `shir:Node`
- `shir:Assertion`
- `shir:PolicyScope`
- `shir:TemporalScope`
- `shir:Link`
- `shir:RoleBinding`
- `shir:Receipt`
- `shir:ProjectionLossReport`

## What it does not yet prove

Missing or partial surfaces still include:

- machine-validated SHIR schema/fixture checks in `semantic-serdes`
- full compact-bundle replay absorption for terminal/revocation events
- module catalog / registry alignment beyond documentation references
- Memory Mesh persistence/reconstruction for ValueFlows event logs and checkpoints
- AgentPlane / Policy Fabric consumption of ValueFlows process/task authority as a governed execution subject

## Correct next lift

The right next lift is cross-repo validation and consumption:

1. move the SHIR projection manifest and receipt example into `semantic-serdes` validation
2. absorb terminal/revocation events into the main compact bundle materializer when the connector/file-write path can safely carry the larger runtime artifact
3. wire ValueFlows event/checkpoint artifacts into Memory Mesh or AgentPlane consumers

## Design rule

This lane should remain a narrow, executable, governed binding. It should not become a dumping ground for every business or workflow concept in the repo.
