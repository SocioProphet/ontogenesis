# View Governance v0.1

Status: draft ontology-governance tranche

## Purpose

This note defines the Ontogenesis-side meaning layer for authority-bound graph and analysis views.

Semantic SerDes owns the portable `ViewContract` schema shape. Ontogenesis owns the governed meaning of the terms used by that schema, including:

- `ViewContract`
- `ViewSignature`
- `DisclosureMode`
- `TypedAbsence`
- `PolicyBarrier`
- `RedactionBoundary`
- `MaterializationBoundary`
- `RevocationEpoch`
- `ViewSensitiveAnalysis`

## Why this exists

A graph view is not valid merely because a traversal returned rows. A governed view must compose:

- principal identity/session authority;
- agent authority when the principal is an agent;
- policy bundle / decision / obligation authority;
- workspace and environment fingerprint authority;
- ontology and schema authority;
- runtime evidence authority;
- traversal/materialization evidence authority;
- transport binding authority.

Ontogenesis provides the semantic vocabulary and SHACL promotion gates for these concepts.

## New module

Ontology module:

- `Platform/view-governance.ttl`

SHACL gate:

- `shapes/view-governance.shacl.ttl`

## Ownership boundary

Ontogenesis does not own the wire schema, Policy Fabric decision objects, Agent Registry session/grant objects, AgentPlane run artifacts, Sociosphere fingerprint registries, or CairnPath step traces.

It owns the semantic terms and gates that allow those objects to be composed safely in a governed ViewContract.

## First-gate semantics

The first SHACL tranche requires that a `view:ViewContract` bind:

- principal authority;
- policy authority;
- workspace authority;
- disclosure mode;
- revocation epoch;
- view signature;
- a sha256 contract hash.

The gate also defines minimal authority-ref requirements for principal, agent, policy, workspace, runtime evidence, and traversal evidence authority nodes.

## Deferred work

- Add example JSON-LD instance graph that conforms to the SHACL gate.
- Add module entry to `catalog/registry.ttl` and `catalog/registry.jsonld` when promoting beyond draft.
- Add `contexts/view-governance.context.jsonld` for downstream JSON-LD use.
- Wire the new shape into the full `make shacl` pipeline if required by the next promotion tranche.
