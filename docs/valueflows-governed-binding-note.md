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
- `bindings/valueflows_governed/tools/*.py`
- `bindings/valueflows_governed/policies/rego/*.rego`
- `.github/workflows/valueflows-governed-ci.yml`

## What it currently proves

This lane currently proves a compact runtime slice for:

- delegated task offer
- delegated task completion override
- delegated task assignment override
- denial of unauthorized assignment override
- deterministic replay against expected outputs

## What it does not yet prove

This lane is not yet fully ontology-native.

Missing or partial surfaces still include:

- SHACL shapes dedicated to the ValueFlows governed lane
- JSON-LD context / context-fragment integration
- ontology-native example alignment beyond the compact runtime bundle
- module catalog / registry alignment beyond documentation references
- revocation and terminal lifecycle semantics for delegations, capability grants, and process runs

## Correct next lift

The right next lift is semantic, not wider runtime sprawl:

1. bind the governed lane to native ontology surfaces such as SHACL and JSON-LD context fragments
2. preserve the compact bundle as the deterministic CI/runtime proof surface
3. add revocation and terminal lifecycle semantics only after the ontology-native surfaces exist

## Design rule

This lane should remain a narrow, executable, governed binding. It should not become a dumping ground for every business or workflow concept in the repo.
