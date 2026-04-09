# Module map (what exists now)

This repo defines a layered ontology stack plus gates/tools.

## Upper
- `Upper/upper-core.ttl`
  - Entity, Process, Agent, System
  - InformationArtifact, Policy, Evidence
  - Ledger, LedgerEntry, Signature, Signer
  - alignment helpers for PROV

## Middle
- `Middle/system-architecture.ttl`
  - Space: SYSTEM / USER / INCEPTION / REGION / MACRO
  - Gate and UpdateFlow (outside→inside adjudication)
- `Middle/registries.ttl`
  - Backend, SyncSpec, Route, IOClaim records

## Lower
- `Lower/bindings-core.ttl`
  - File/Directory, Process/Service
  - Port/Device/Interface
  - Container + minimal K8sResource
  - BoundaryInterface surface

## Platform
- `Platform/platform.ttl`
  - Component taxonomy: SourceOS, Genesis, Inception, Twin, Mesh
- `Platform/SourceOS.ttl`
  - ostree deployments, Nix flake generations, rollback semantics
- `Platform/Genesis.ttl`
  - keys/manifests/signatures/cosign
- `Platform/Inception.ttl`
  - local inception kit services: MinIO, SAPIEN, ROCKZDB, GIB, Bus
- `Platform/Twin.ttl`
  - snapshots, handshake, replication
- `Platform/Mesh.ttl`
  - wireguard tunnels and peers

## Prophet
- `prophet/prophet_cli.ttl`
  - planes, commands, profiles
  - 3×3 build recipes, steps
  - dynamic registration: ServiceDescriptor, CapabilityDescriptor (CapD)
  - provenance carriers: schemaRef + leafRef
- `prophet/capd.ttl`
  - CapD refinement: Requirements, image/chart artifacts, privacy policy hooks
- `prophet/prophet_diagrams.ttl` (+ `prophet/diagrams/*.mmd`)
  - pointers to Mermaid sources for architecture diagrams
- SHACL: `prophet/shapes/prophet_cli.shacl.ttl`

## EPI (Epi‑Onto‑Learning)
- `epi/noether.ttl`
  - Noetherian layer contract: algebra, group, invariant form, integrator, charges, coercions
- `epi/epi.ttl`
  - learning runs, diagnostics, publishing pipeline artifacts (signed PDFs), quantum lane model
- `epi/tools/` and `epi/notebooks/`
  - reference implementations (Aer-first) for reporting and quantum adapter skeletons
- SHACL: `epi/shapes/epi.shacl.ttl`

## Domains
- `Domains/human.ttl` — persons, sex/gender, phenotype traits (coded observations)
- `Domains/math.ttl` — pragmatic math core (structures, manifolds, proofs)
- `Domains/kubernetes.ttl` — minimal K8s abstractions
- `Domains/cyber.ttl` — security event/control/finding stubs
- `Domains/metadata.ttl` — catalogs/datasets/services
- `Domains/web.ttl` — socioprophet.* domain endpoints

## Gates and audits
- SHACL bundle: `shapes/core.shacl.ttl`
- Scripts:
  - parse validation, SHACL gates, JSON-LD roundtrip
  - dist build, ledger build/verify, detached signatures, SPDX SBOM

