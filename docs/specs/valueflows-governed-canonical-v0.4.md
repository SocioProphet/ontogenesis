# Value Flows → Governed Canonical Object Substrate
Version: v0.4 delegated-authority slice
Status: machine-enforced delegated-authority slice

## Source grounding
The source deck argues for a shared data language, multiple optimal interfaces, shared semantics for people, groups, participation, and roles, and a conversational task flow where offers, commitments, and follow-up occur over shared data rather than a single interface. This slice extends that premise with explicit delegated authority and repo-ready CI. It does **not** claim those governance layers were present in the source deck itself. fileciteturn0file0

## What changed from v0.3
- added canonical `Delegation` and `CapabilityGrant`
- added delegated authority event types:
  - `delegation.issued.v1`
  - `capabilitygrant.issued.v1`
  - `task.assignment_overridden.v1`
- extended the authoritative hash surface to `authoritative_projection_v2`
- added delegated offer, delegated completion override, and delegated assignment override fixtures
- added expected-report checker and repo-ready CI workflow
- added Rego runtime test inputs for delegated allow/deny scenarios

## Scope of this slice
1. process run created
2. delegation issued
3. capability grant issued
4. task offered
5. commitment accepted
6. task progressed
7. task completed or assignment overridden
8. checkpoint created

The slice is intentionally narrow. It proves governed task-flow state, authority, replay, divergence, and checkpoint-hash consistency before broadening into more ontology families.

## Canonical object set
- `Actor`
- `Group`
- `Role`
- `Membership`
- `ProcessRun`
- `Task`
- `Commitment`
- `Delegation`
- `CapabilityGrant`
- `PolicyDecision`
- `EvidencePack`
- `CairnCheckpoint`

## Event set
- `processrun.created.v1`
- `delegation.issued.v1`
- `capabilitygrant.issued.v1`
- `task.offered.v1`
- `commitment.accepted.v1`
- `task.progress_updated.v1`
- `task.assignment_overridden.v1`
- `task.completed.v1`
- `checkpoint.created.v1`

## Authority model
Membership does not imply authority.

Authority may come from:
- ordinary role-bound execution, such as the accepted assignee progressing or completing a task normally
- explicit delegated capability, such as `task.offer`, `task.complete.override`, or `task.assignment.override`

Delegation and capability are separate objects because social participation and authority must not collapse into one field.

## Authoritative hash surface
Projection name: `authoritative_projection_v2`

The authoritative replay surface includes:
- `process_run`
- `task`
- `commitments`
- `delegations`
- `capability_grants`
- `divergences`

It intentionally excludes checkpoint objects themselves to avoid self-reference loops in the state hash.

## Proven machine-checked behaviors
The delegated linear replay proves:
- delegated offer by a non-coordinator when a valid delegation plus `task.offer` capability exists
- delegated completion override when a valid `task.complete.override` capability exists
- checkpoint hash consistency against the same authoritative projection

The assignment-override replay proves:
- delegated reassignment from one worker to another when `task.assignment.override` exists

The negative-control divergence replay proves:
- unauthorized assignment override is denied and recorded as a `policy_denied` divergence

## CI posture
This slice is designed for CI execution with:
- schema validation
- deterministic replay for linear, assignment-override, and divergence fixtures
- expected-report comparison
- OPA runtime checks against delegated allow/deny inputs

## Remaining gaps after v0.4
- `delegation.revoked.v1`
- `capabilitygrant.revoked.v1`
- `processrun.completed.v1`
- `processrun.canceled.v1`
- richer cryptographic provenance for delegation and grant issuance
- upstream execution of the authored OPA checks and capture of the first real CI run artifact

## Recommended landing inside ontogenesis
This material fits `ontogenesis` because the repository already positions itself as the ontology genesis, mapping, boundary, provenance, policy, and validation substrate. The governed Value Flows slice should be treated as a binding/mapping and validation surface within that broader ontology framework, not as a separate orphan specification.
