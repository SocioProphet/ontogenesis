# ValueFlows governed lane → SHIR projection v0.1

Status: draft mapping note  
Owner: Ontogenesis  
Source lane: `bindings/valueflows_governed/`  
Target contract: `docs/specs/shir-v0.1.md`

## Purpose

This note defines the first projection mapping from the ValueFlows governed binding lane into SHIR.

The goal is not to replace ValueFlows runtime replay. The goal is to make the governed process/task/authority lane projectable into the Semantic Hyperknowledge Intermediate Representation so downstream SerDes, graph, memory, policy, and receipt surfaces can consume the lane without flattening away authority, temporal scope, evidence, or checkpoint semantics.

## Source objects

The source ValueFlows governed lane currently includes:

- `ProcessRun`
- `Task`
- `Delegation`
- `CapabilityGrant`
- `Commitment`
- `CairnCheckpoint`

It also has runtime proof for delegated authority closure and terminal lockout behavior.

## SHIR target objects

The first target SHIR object families are:

- `shir:Node`
- `shir:Context`
- `shir:Connector`
- `shir:RoleBinding`
- `shir:Link`
- `shir:Assertion`
- `shir:Evidence`
- `shir:TemporalScope`
- `shir:PolicyScope`
- `shir:Projection`
- `shir:ProjectionLossReport`
- `shir:Receipt`

## Mapping table

| ValueFlows object | SHIR target | Projection rule |
| --- | --- | --- |
| `ProcessRun` | `shir:Context` + `shir:Node` | A process run is both an execution context and an addressable semantic node. |
| `Task` | `shir:Node` | A task is an operational work node scoped to its process run context. |
| `Delegation` | `shir:Assertion` + `shir:PolicyScope` | Delegation is an authority assertion with temporal and policy scope. |
| `CapabilityGrant` | `shir:Assertion` + `shir:PolicyScope` | A capability grant is a narrower authority assertion derived from delegation. |
| `Commitment` | `shir:Link` | A commitment is a connector-backed relation linking debtor actor, task, process context, and status. |
| `CairnCheckpoint` | `shir:Receipt` | A checkpoint is a reproducibility and governance receipt over the materialized state projection. |
| Runtime divergence | `shir:ProjectionLossReport` or `shir:CurationDecision` | Divergence records become explicit projection/evaluation artifacts rather than silent failures. |

## Connector profiles

### `vfg:delegatesAuthority(grantor, grantee, process_run, scope)`

Role bindings:

- `grantor` → actor node
- `grantee` → actor node
- `process_run` → process context
- `scope` → policy scope node

### `vfg:grantsCapability(grantor, grantee, capability, delegation, process_run, task?)`

Role bindings:

- `grantor` → actor node
- `grantee` → actor node
- `capability` → capability literal/value node
- `delegation` → delegation assertion
- `process_run` → process context
- `task` → optional task node

### `vfg:commitsToTask(debtor, task, process_run, status)`

Role bindings:

- `debtor` → actor node
- `task` → task node
- `process_run` → process context
- `status` → commitment-state literal/value node

## Temporal rules

ValueFlows valid-time fields project into `shir:TemporalScope`.

- `startedAt`, `plannedEndAt`, `completedAt`, and `canceledAt` define process validity and terminal state scope.
- `validFrom`, `validUntil`, and `revokedAt` define authority validity for delegation and capability grants.
- `dueAt` and task terminal times define task execution scope.

Observation or transaction time should be taken from the replay event envelope when available.

## Policy rules

Delegations and capability grants always project into `shir:PolicyScope`.

The policy scope must preserve:

- delegated actor
- grantor actor
- allowed capability
- process scope
- optional task scope
- active/revoked/expired status
- revocation reason when present

## Receipt rules

Each `CairnCheckpoint` projects into a `shir:Receipt` with:

- source lane: `valueflows-governed`
- source projection: `authoritative_projection_v2`
- source materialized state hash
- ontology profile reference
- SHIR projection profile
- policy decision references where available
- projection loss report reference

## Loss profile

The initial projection is intentionally partial.

Preserved:

- object identity
- process/task scoping
- delegated authority shape
- terminal-state timestamps
- checkpoint hash
- policy-relevant capability and delegation scope

Not fully preserved yet:

- full runtime event log order
- all Rego decision internals
- all compact-bundle validation reports
- full actor graph beyond referenced actor IDs
- direct Memory Mesh persistence/reconstruction receipts

These losses must be declared in the projection manifest and receipt example.

## Next lift

The next implementation step should move this manifest shape into `semantic-serdes` so SHIR schema validation and projection receipts can be tested alongside the existing SHIR SerDes fixtures.
