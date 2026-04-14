# Value Flows Governed Canonical v0.4 — Landing Plan for Ontogenesis

## Decision
Land this work in `SocioProphet/ontogenesis` rather than a generic standards repo.

## Why this repository is the correct home
`ontogenesis` already describes itself as the framework for ontology genesis, linking, mapping and binding, provenance, policy-aware validation, JSON-LD boundary surfaces, and iterative refinement under uncertainty. The governed Value Flows slice is exactly that sort of binding and validation surface: a machine-checkable canonical object lane with replay, delegated authority, and policy/runtime checks.

## What has already been anchored on this branch
- `docs/specs/valueflows-governed-canonical-v0.4.md`
- this landing-plan document

## Next coherent file tranche to add on this same branch
### Canonical schemas
- `bindings/valueflows_governed/schemas/json/canonical/v1/actor.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/group.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/role.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/membership.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/process-run.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/task.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/commitment.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/delegation.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/capability-grant.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/policy-decision.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/evidence-pack.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/canonical/v1/cairn-checkpoint.v1.schema.json`

### Event schemas
- `bindings/valueflows_governed/schemas/json/events/v1/event-envelope.v1.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/processrun.created.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/delegation.issued.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/capabilitygrant.issued.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/task.offered.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/commitment.accepted.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/task.progress_updated.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/task.assignment_overridden.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/task.completed.v1.payload.schema.json`
- `bindings/valueflows_governed/schemas/json/events/v1/checkpoint.created.v1.payload.schema.json`

### Replay fixtures and expected outputs
- `bindings/valueflows_governed/fixtures/replay/task-flow-linear/...`
- `bindings/valueflows_governed/fixtures/replay/task-flow-assignment-override/...`
- `bindings/valueflows_governed/fixtures/replay/task-flow-divergence/...`

### Policy runtime
- `bindings/valueflows_governed/policies/rego/task_flow_policy_v0_3.rego`
- `bindings/valueflows_governed/policies/rego/testdata/...`
- `bindings/valueflows_governed/ci/check_policy_runtime.sh`

### Deterministic tooling
- `bindings/valueflows_governed/tools/validate_bundle.py`
- `bindings/valueflows_governed/tools/materialize_task_flow.py`
- `bindings/valueflows_governed/tools/check_expected_reports.py`

### CI
- `.github/workflows/valueflows-governed-ci.yml`

## Why use a dedicated subtree
A dedicated `bindings/valueflows_governed/` subtree keeps this slice self-contained while still living inside the ontology/mapping substrate where it belongs. That avoids polluting root-level repo surfaces prematurely, while making it obvious that this is a governed binding and validation surface rather than a detached project.

## Immediate merge criteria for the full tranche
- schema validation passes
- linear replay passes with checkpoint-hash consistency
- delegated assignment override passes
- unauthorized assignment override produces exactly one `policy_denied` divergence
- OPA delegated allow/deny tests pass in CI

## Explicit non-goals for this tranche
Do not broaden into additional ontology families until the delegated task/process slice is fully landed and passing.

## After the full tranche lands
1. add `delegation.revoked.v1`
2. add `capabilitygrant.revoked.v1`
3. add `processrun.completed.v1`
4. add `processrun.canceled.v1`
5. add one brownfield adapter fixture mapping external task/admin semantics into this canonical lane
