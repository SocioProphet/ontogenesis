# Ontogenesis upstream capture — 2026-04-12

## Purpose

This document captures the **actual** upstream state of `SocioProphet/ontogenesis` as the canonical ontology/governance repository that should anchor downstream semantic, runtime, and policy work.

This is not a greenfield design note. It is a capture of what already exists upstream, what it already solves, and what gaps remain for business ontology, value-driver, benchmark, binding, and runtime-critic work.

---

## Executive position

`ontogenesis` is already the canonical upstream semantic and release-governance plane for the SocioProphet stack.

It already provides:

- layered RDF/OWL/JSON-LD ontology modules
- machine-readable module registry and namespace discipline
- SHACL promotion gates
- deterministic `dist/` build and `audit/` manifest generation
- ledger generation and signature posture
- JSON-LD contexts and examples
- CI-oriented validation and SBOM support

Therefore:

1. downstream runtime/compiler work should **rebase on Ontogenesis**, not create a rival namespace
2. new business/value-driver/runtime semantic surfaces should be proposed as **Ontogenesis modules** or tightly governed overlays
3. promotion, audit, and release discipline for new semantic modules should inherit Ontogenesis build/gate/ledger/signature policy

---

## Canonical repo purpose and release posture

The repo is positioned as an auditable, policy-gated, supply-chain-traceable repository for ontology and semantic-web assets used across the SocioProphet stack.

Core declared properties of the repo include:

- repeatable ontology distribution builds into `dist/`
- deterministic hashing
- append-only ledger generation in `ledger/`
- artifact signing
- SHACL gates for promotion and policy checks
- machine-readable module catalog/registry
- layered ontology architecture

The generated surfaces are intentionally separated from authored source:

- `dist/` — generated distribution surface
- `audit/` — generated manifests / validation artifacts
- `ledger/` — checksums + signature pointers
- `signatures/` — detached signatures
- `sbom/` — SPDX outputs

This repo is meant to be boring in the strong sense: deterministic, auditable, and resistant to silent semantic drift.

---

## Current upstream layer model

### Upper

Purpose: cross-domain primitives and standards alignment.

Currently represented by:

- `Upper/upper-core.ttl`
- `Upper/upper-alignments.ttl`

Observed role:

- foundational categories (`Entity`, `Process`, `Agent`, `System`, `InformationArtifact`, `Policy`, `Evidence`, `Assertion`)
- ledger/signature/signer primitives
- alignment helpers for PROV / SKOS / DCTERMS

### Middle

Purpose: architecture, governance, action/state/trace semantics, registries, and learning/assessment surfaces.

Currently represented by:

- `Middle/system-architecture.ttl`
- `Middle/registries.ttl`
- `Middle/action-ontology.ttl`
- `Middle/learning-ontogenesis.ttl`

Observed role:

- canonical spaces: `SYSTEM`, `USER`, `INCEPTION`, `REGION`, `MACRO`
- outside→inside adjudication gates and update flows
- registries for backend/sync/route/IO claims
- action/state/trace model for governed coordination
- curriculum / competency / assessment / optimization loop linkage to EPI and Noetherian evidence

### Lower

Purpose: atomic operational bindings to system surfaces.

Currently represented by:

- `Lower/bindings-core.ttl`

Observed role:

- files, directories, processes, services
- ports, devices, interfaces
- containers, minimal k8s resources
- boundary-interface surfaces

### Platform

Purpose: platform-specific semantic modules.

Currently represented by:

- `Platform/platform.ttl`
- `Platform/SourceOS.ttl`
- `Platform/Genesis.ttl`
- `Platform/Genesys.ttl`
- `Platform/Inception.ttl`
- `Platform/Twin.ttl`
- `Platform/Mesh.ttl`

Observed role:

- component taxonomy for SourceOS / Genesis / Inception / Twin / Mesh
- ostree + Nix + rollback semantics
- keys / manifests / signatures / cosign-adjacent posture
- inception kit services (MinIO, SAPIEN, ROCKZDB, GIB, Bus)
- snapshot / bridge / federation / replication semantics
- WireGuard peers / tunnels / routes

### Prophet

Purpose: control-plane and CLI semantics.

Currently represented by:

- `prophet/prophet_cli.ttl`
- `prophet/capd.ttl`
- `prophet/prophet_diagrams.ttl`
- `prophet/shapes/prophet_cli.shacl.ttl`
- `prophet/contexts/prophet.context.jsonld`
- `prophet/diagrams/*.mmd`

Observed role:

- planes / commands / profiles
- 3×3 build recipes and steps
- dynamic registration via `ServiceDescriptor`, `CapabilityDescriptor`, `PluginDescriptor`
- CapD refinement and requirement surfaces
- provenance carriers such as `schemaRef` and `leafRef`

### EPI

Purpose: Noetherian learning, report/publishing provenance, optional quantum lane.

Currently represented by:

- `epi/noether.ttl`
- `epi/epi.ttl`
- `epi/shapes/epi.shacl.ttl`
- `epi/contexts/epi.context.jsonld`
- `epi/tools/*`
- `epi/notebooks/*`
- `epi/tritfabric/*`

Observed role:

- layer contracts, algebras, groups, invariant forms, integrators, charges, coercions
- learning runs and diagnostic reports
- publishing pipeline and signed-PDF artifact semantics
- optional quantum provider/backend/task model with hardware opt-in

### Domains

Purpose: domain-specific vocabularies.

Currently represented by:

- `Domains/human.ttl`
- `Domains/math.ttl`
- `Domains/kubernetes.ttl`
- `Domains/cyber.ttl`
- `Domains/metadata.ttl`
- `Domains/web.ttl`
- `Domains/cc_runners.ttl`

Observed role:

- human/person/phenotype observations
- practical math structures/manifolds/proofs
- minimal Kubernetes abstractions
- cyber event/control/finding stubs
- metadata/catalog/dataset/service vocabulary
- web endpoints for socioprophet.*
- CC runner surfaces

---

## Machine-readable governance surfaces

### Module registry

`catalog/registry.ttl` and `catalog/registry.jsonld` are the authoritative machine-readable module inventory.

The registry currently records, at minimum:

- module path
- layer
- base IRI
- semver
- status
- label

This registry is more authoritative than any informal directory summary and already exposes additional modules beyond the simpler module map.

### Namespace discipline

Current canonical base IRI:

`https://socioprophet.github.io/ontogenesis/`

Current canonical prefixes include:

- `upper:`
- `middle:`
- `lower:`
- `plat:`
- `prop:`
- `capd:`
- `nl:`
- `epi:`
- `og:`

The repo already recommends:

- stable lowercase filenames
- `owl:versionInfo` as the semantic version surface
- creating new modules rather than silently overloading old ones

### SHACL gates

Current SHACL policy surfaces already enforce more than shape hygiene.

Examples already modeled upstream include:

- required CapD fields
- minimum Noetherian layer-contract constraints
- octonion-specific coercion witness requirement
- explicit hardware opt-in constraints for quantum lane usage

This means Ontogenesis already encodes promotion rules, not just ontology structure.

---

## Build / audit / release control surfaces

Current toolchain components include:

- RDF parse validation
- SHACL gate execution
- JSON-LD roundtrip tests
- deterministic `dist/` copy + manifest generation
- ledger generation and verification
- detached-signature flow
- SPDX SBOM emission

Current local workflow is intentionally simple:

- create venv
- install `requirements-dev.txt`
- run validation / SHACL / JSON-LD tests
- run build / ledger / verify / SBOM

The repo already contains:

- `Makefile`
- Python 3.11+ project metadata
- test suite
- GitHub workflows for validation and release

This is the canonical release-governance plane that downstream semantic work should inherit.

---

## Recent upstream promotion state

Recent history matters because this repo is live.

As of 2026-04-12, the baseline promoted state is the result of the merged PR:

- **PR #1** — `Promote 2026-03-25 ontogenesis winner`

Observed properties of that merge:

- merged into `main`
- merged on 2026-04-09
- 86 changed files
- 3292 additions
- 58 deletions

Therefore, all downstream design work should treat the current `main` branch as a promoted baseline rather than as an untouched prototype.

---

## What Ontogenesis already solves for us

Ontogenesis already solves the following classes of problems:

### 1. Canonical namespace and module discipline

We do not need to invent a rival semantic root. The repo already has base IRI, prefixes, module registry, and SemVer posture.

### 2. Promotion and anti-drift policy

We do not need to invent ontology-gating from scratch. SHACL bundles already function as promotion checks.

### 3. Supply-chain traceability for semantic artifacts

The repo already treats ontology artifacts as build outputs with manifest, ledger, signature, and SBOM surfaces.

### 4. Prophet / platform / EPI semantic backbone

We do not need to separately invent spaces, gates, capability descriptors, build recipes, action/state/trace patterns, or Noether/EPI publishing vocabulary at the ontology level.

### 5. Module onboarding workflow

The repo already defines how new modules should be added, registered, validated, and released.

---

## What Ontogenesis does **not** yet solve

The current upstream repo does **not yet** appear to provide a dedicated business ontology lane for:

- business archetypes
- company / BU / product / contract / segment / channel modeling at the business-analysis level
- unit-economics metric family (ARR, MRR, NRR, GRR, CAC, CAC payback, etc.)
- causal value-driver and lever graph semantics
- benchmark priors / selector profiles / benchmark quality records
- source observation / canonical observation / resolved binding runtime semantics
- historical restatement / binding epochs / freshness / precedence / derivation class
- recommendation-critic and workflow-output gating tied to binding quality

This is the primary gap to fill upstream.

---

## Immediate architectural implication

The downstream runtime/compiler program should be reframed as follows:

- **Ontogenesis** = canonical authored ontology + namespace + gate + supply-chain repo
- **PackIR / runtime compiler** = normalized executable IR compiled from Ontogenesis modules and governed overlays
- **business/value-driver/runtime modules** = new Ontogenesis-authored semantic surfaces, not a parallel ontology stack

In other words:

- Ontogenesis remains the semantic source of truth
- runtime/compiler artifacts remain downstream generated forms
- new business semantics should be added upstream using the existing Ontogenesis discipline

---

## Hard invariants to preserve in follow-on work

The following constraints should be treated as mandatory:

1. No rival namespace for business/runtime semantics unless there is a compelling and explicit compatibility reason.
2. All new business modules must register in `catalog/registry.ttl` and `catalog/registry.jsonld`.
3. New business modules should add SHACL gates where promotion invariants matter.
4. New semantic surfaces should preserve `owl:versionInfo` / SemVer discipline.
5. Downstream compiler/runtime layers must preserve provenance back to Ontogenesis modules and versions.
6. Generated `dist/`, `audit/`, `ledger/`, and signature outputs remain generated surfaces, not hand-edited truth.
7. Promotion and release posture for new semantic modules should reuse the existing build/verify/sign/SBOM flow.

---

## Recommended next move

Create the first upstream business ontology family and the import bridge docs/specs that connect Ontogenesis modules into downstream executable IR.

That follow-on work is captured separately in:

- `docs/specs/business_ontology_bridge.md`

---

## Status of this capture

This document is a snapshot capture of current upstream state and should be updated when:

- registry entries materially change
- new business modules are added
- build/release policy changes
- new platform/Prophet/EPI modules materially alter the semantic baseline
