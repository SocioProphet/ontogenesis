# SVF Semantic Validation Plan

Status: contract declaration for downstream workspace discovery  
Plane: Ontogenesis / ontology governance  
Upstream authority: SocioProphet/ProCybernetica SVF policy primitive  
Workspace registry: SocioProphet/sociosphere SVF workspace registry

## Purpose

This document defines Ontogenesis' first Sovereign Validation Fabric (SVF) semantic-validation plan contract. It wraps the existing ontology verification pipeline as declared SVF Actions and one advisory Plan.

SVF does not replace Ontogenesis' existing validation discipline. Ontogenesis already provides RDF parse validation, SHACL gates, JSON-LD roundtrip checks, deterministic dist builds, ledger build and verification, and SPDX SBOM generation. SVF registers those lanes as governed validation capabilities that Sociosphere can discover and select.

## Current basis

The repository exposes its local verification pipeline through `make all`:

1. `make validate`
2. `make shacl`
3. `make jsonld`
4. `make build`
5. `make ledger`
6. `make verify`
7. `make sbom`

The first SVF contract maps those commands into a typed semantic-validation plan.

## SVF ids

The first Ontogenesis SVF contract uses these ids:

- `svf:policy:ontogenesis.semantic-readonly`
- `svf:action:ontogenesis.validate-rdf`
- `svf:action:ontogenesis.shacl`
- `svf:action:ontogenesis.jsonld-roundtrip`
- `svf:action:ontogenesis.build-dist`
- `svf:action:ontogenesis.ledger-build`
- `svf:action:ontogenesis.ledger-verify`
- `svf:action:ontogenesis.sbom`
- `svf:plan:ontogenesis.semantic-validation-basic`

## Claim scope

The first plan may only support these bounded claims:

- `schema_conformant`
- `semantic_roundtrip_preserved`
- `artifact_integrity_verified`

It does not certify domain truth beyond declared ontology modules and SHACL shapes. It does not certify full semantic adequacy of modeled concepts. It does not certify downstream consumer correctness, live platform behavior, or production release readiness beyond the executed local validation pipeline.

## Capability policy

`svf:policy:ontogenesis.semantic-readonly` is advisory and local. It admits CI or workspace invocation of existing Ontogenesis verification commands only.

The policy permits generated ontology outputs where existing Ontogenesis Make targets already generate dist, ledger, audit, or SBOM artifacts. Future release publication or signing flows require a separate policy profile and separate review.

## Plan composition

`svf:plan:ontogenesis.semantic-validation-basic` composes the existing local ontology verification lanes:

1. `make validate`
2. `make shacl`
3. `make jsonld`
4. `make build`
5. `make ledger`
6. `make verify`
7. `make sbom`

The first contract is advisory in the Sociosphere registry. It becomes a blocking candidate only after the repo-local SVF validator is observed green and Sociosphere updates the registry posture.

## Non-claims

This document is a plan contract. It does not prove that the plan has run.

This document does not issue a ValidationReceipt.

This document does not replace Ontogenesis release governance.

This document does not grant Ontogenesis authority over upstream policy-fabric schemas or workspace routing.
