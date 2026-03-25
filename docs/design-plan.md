# Design plan

## Goals
1. **One source of truth** for SocioProphet ontologies: auditable, signed, policy-gated.
2. **Layering** to separate foundational semantics from platform bindings.
3. **Explicit module boundaries** with SemVer, compatibility notes, and OWL imports.
4. **Reasoning + SHACL gating** to enable safe evolution (outside→inside adjudication).

## Layering

### Upper
- Cross-domain primitives (Entity, Process, Agent, System, Policy, Evidence, Artifact).
- Align to standard vocabularies (RDF/OWL, SKOS, PROV-O, DCTERMS) by reference.

### Middle
- System architecture abstractions:
  - spaces (SYSTEM/USER/INCEPTION/REGION/MACRO)
  - capability descriptors (CapD)
  - provenance carriers (schemaRef/leafRef)
  - registries (backends, sync specs, routes, IO claims)
  - governance, validation and promotion flows

### Lower
- Atomic bindings to on-device data/services/IO:
  - files, processes, ports, network, packages
  - container runtimes, k8s resources
  - observability signals
- These provide the handle surface for system admin + boundary interfaces.

## Platform modules
- SourceOS: ostree/Nix three-space model, update/rollback semantics
- Genesis: keys, PKI, manifest, signatures
- Inception: local kind cluster + MinIO + SAPIEN + ROCKZDB + GIB registry
- Twin: snapshots, bridge, federation, replication policy
- Mesh: WireGuard + routes + boundary interfaces

## Prophet CLI ontology
- Models planes/commands, profiles, build recipes, dynamic registration, CapD lifecycle.
- SHACL gates enforce required fields + invariants (e.g., capability must declare plane/verbs/requires/rollout).

## Epi‑Onto‑Learning
- Models Noetherian layer contracts + publishing/provenance + optional quantum offload.
- SHACL gates enforce that hardware usage is opt-in and fully logged (backend, mitigation settings).

