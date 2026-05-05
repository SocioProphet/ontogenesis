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
- `Platform/lattice-ontology-query.ttl`
  - governed ontology-query adapter contract for Lattice FederatedQueryPlane; distinct from SPARQL routing
- `Platform/Parsing/`
  - `core.ttl` — utterances, tokens, spans, links, candidates, evidence, and promotion decisions
  - `link-grammar.ttl` — Link Grammar connectors, disjuncts, linkages, lexicon entries, and parse-failure terms
  - `acset-parse.ttl` — canonical ACSET parse-state scaffold
  - `hypergraph-promotion.ttl` — promotion decisions, gates, and parse-backreference preservation
  - SHACL: `shapes/parsing-gates.ttl`
  - Validator: `tools/validate_parsing.py`; CI: `.github/workflows/validate-parsing.yml`
- `Platform/Epistemics/`
  - `michael-core.ttl` — Michael epistemic core primitives
  - `michael-belief.ttl` — belief-state surface
  - `michael-discovery.ttl` — candidate-law / discovery surface
  - SHACL: `shapes/michael-belief.shacl.ttl`
- `Platform/Twins/`
  - `human-digital-twin.ttl` — bounded human digital twin starter surface
  - SHACL: `shapes/human-digital-twin.shacl.ttl`

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
- `Domains/business_core.ttl` — company, offering, customer, contract, revenue, geography, scenario modeling
- `Domains/cybernetic-self.ttl` — cybernetic self, embodiments, chambers, objective functions
- `Domains/party-identity.ttl` — party, identity, accounts, entitlements, role assignments
- `Domains/org-legal.ttl` — legal entities, jurisdictions, ownership, repository allocation
- `Domains/product-service.ttl` — product/service offerings, plans, SKUs, capabilities, entitlements, and service instances

## Bindings / governed profiles
- `bindings/valueflows_governed/`
  - compact governed binding lane for process-scoped task flow, delegated authority, deterministic replay, and policy runtime checks
  - execution surface remains compact and CI-oriented (`compact-bundle.v1.json`, runtime tools, Rego policy, GitHub Actions workflow)
  - ontology-native semantic lift is present via `bindings/valueflows_governed/valueflows-governed.context.jsonld`, `shapes/valueflows-governed.shacl.ttl`, and `examples/valueflows-governed-task-flow-demo.jsonld`
  - terminal and revocation semantics are represented for completed/canceled processes and tasks, plus revoked/expired delegations and capability grants
  - SHIR projection surface is present via `bindings/valueflows_governed/valueflows-to-shir.projection.v0.1.json`, `docs/valueflows-to-shir-projection.md`, and `examples/valueflows-shir-receipt.example.json`

## Specifications and profiles
- `docs/specs/shir-v0.1.md`
  - Semantic Hyperknowledge Intermediate Representation draft: preserves n-ary relations, role bindings, context, evidence, temporal scope, policy scope, induction traces, projection loss reports, and receipts before downstream lowering
- `docs/specs/ontology-query-adapter.md`
  - governed ontology-query adapter contract for OWL/SHACL/schema-alignment/reasoning queries in the Lattice FederatedQueryPlane
- `docs/specs/valueflows-governed-canonical-v0.4.md`
  - governed ValueFlows profile spec

## Gates and audits
- SHACL bundles: `shapes/core.shacl.ttl`, `shapes/ontogenesis.shacl.ttl`, `shapes/cybernetic-self.shacl.ttl`, `shapes/product-service.shacl.ttl`, `shapes/parsing-gates.ttl`, `shapes/ontology-query.shacl.ttl`, `shapes/valueflows-governed.shacl.ttl`, `shapes/michael-belief.shacl.ttl`, `shapes/human-digital-twin.shacl.ttl`
- Scripts:
  - parse validation, SHACL gates, JSON-LD roundtrip
  - dist build, ledger build/verify, detached signatures, SPDX SBOM
