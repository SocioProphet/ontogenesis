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
- `Middle/kg-lifecycle.ttl`
  - governed knowledge graph lifecycle states, promotion, retirement, and lifecycle gates
- `Middle/semantic-mapping.ttl`
  - mapping assertions, mapping methods, confidence, evidence, and curation state
- `Middle/named-graph-governance.ttl`
  - named graph scopes, graph ownership, policy binding, and publication controls
- `Middle/banking-core.ttl`
  - seed banking twin core for banking firms, legal entities, portfolios, counterparties, capital/liquidity assertions, and filing packs

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
- `Platform/knowledge-context.ttl`
  - Knowledge Context v1 semantic governance: passages, mentions, entities, claims, provenance, embedding references, vector index references, and entity resolution records
- `Platform/view-governance.ttl`
  - ViewContract semantic governance for authority-bound graph/analysis views, disclosure modes, typed absence, policy barriers, materialization boundaries, revocation epochs, and view signatures
  - SHACL: `shapes/view-governance.shacl.ttl`
  - JSON-LD context: `contexts/view-governance.context.jsonld`
  - example: `examples/view-governance-demo.ttl`
  - spec: `docs/specs/view-governance.md`
- `Platform/ReasoningFailure/`
  - `reasoning-failure.ttl` — reasoning-failure ontology slice covering failure modes, perturbations, invariants, verifiers, traces, mitigation patterns, residual risk, regression cases, and evidence receipts
  - SHACL: `shapes/reasoning_failure.shacl.ttl`
  - JSON-LD context: `contexts/reasoning-failure.context.jsonld`
  - example: `examples/reasoning_failure_demo.ttl`
- `Platform/GovernedIntelligence/`
  - `governed-intelligence.ttl` — canonical SocioProphet governed-intelligence object model: Entity, Anchor, Evidence, Claim, ProofCertificate, ExplanationTrace, VectorCandidate, PolicyDecision, ActionProposal, ActionAdmission, RuntimeReceipt, LearningEvent, Revocation, SlashTopicProfile, and VectorEncodingManifest
  - SHACL: `shapes/governed_intelligence.shacl.ttl`
  - JSON-LD context: `contexts/governed-intelligence.context.jsonld`
  - JSON Schema: `schemas/governed-intelligence.v1.schema.json`
  - vector manifest: `manifests/governed-intelligence.vector-encoding.manifest.v1.json`
  - examples: `examples/governed-intelligence/`
  - spec: `docs/specs/governed-intelligence-object-model-v0.md`
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

## Alignments
- `Alignments/gist.ttl`
- `Alignments/fibo.ttl`
- `Alignments/uco-case.ttl`
- `Alignments/d3fend.ttl`
- `Alignments/iof-sco.ttl`
- `Alignments/dodaf-cco.ttl`
- `Alignments/mitre-attack.ttl`
  - governed MITRE ATT&CK / ATLAS alignment scaffold
  - seed ATT&CK tactic/technique hooks and SourceOS-local technique equivalents
  - map-not-vendor-by-default import policy for future STIX/TAXII-generated modules

These are governed alignment scaffolds. They are not full vendored external ontology trees.

## Prophet
- `prophet/prophet_cli.ttl`
  - planes, commands, profiles
  - 3×3 build recipes, steps
  - dynamic registration: ServiceDescriptor, CapabilityDescriptor (CapD)
  - provenance carriers: schemaRef + leafRef
- `prophet/capd.ttl`
  - CapD refinement: Requirements, image/chart artifacts, privacy policy hooks
- `prophet/prophet_artifact.ttl`
  - computational artifact contract for governed workflows, datasets, models, benchmarks, notebooks, runtimes, papers, agent skills, and scoreboards
  - SHACL: `prophet/shapes/prophet_artifact.shacl.ttl`
  - JSON-LD context: `contexts/prophet-artifact.context.jsonld`
  - examples: `examples/prophet_artifact_examples.ttl`, `examples/prophet-artifact-*.example.jsonld`
  - spec: `docs/specs/prophet_artifact_contract.md`
  - integrity query: `tests/prophet-artifact-integrity.rq`
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
- `Domains/agentic-purple-team.ttl` — governed agentic purple-team loops/actions, evidence envelopes, safety boundaries, gates, atomic tests, countermeasure rules, run receipts/summaries, AI/MCP/agent-skill risk, graph robustness, and MITRE-compatible local technique model
- `Domains/smart-home-privacy.ttl` — smart-home privacy governance for vendors, devices, capabilities, physical contexts, privacy claims, evidence, coverage findings, risk inferences, consent boundaries, GAIA bindings, and HDT impact bindings
- `Domains/balance-sheet.ttl` — banking balance-sheet seed module for assets, liabilities, cashflows, and funding sources
- `Domains/regulatory-reporting.ttl` — banking regulatory-reporting seed module for filing packs, line items, correction chains, and signoffs

## Bindings / governed profiles
- `bindings/valueflows_governed/`
  - compact governed binding lane for process-scoped task flow, delegated authority, deterministic replay, and policy runtime checks
  - execution surface remains compact and CI-oriented (`compact-bundle.v1.json`, runtime tools, Rego policy, GitHub Actions workflow)
  - ontology-native semantic lift is present via `bindings/valueflows_governed/valueflows-governed.context.jsonld`, `shapes/valueflows-governed.shacl.ttl`, and `examples/valueflows-governed-task-flow-demo.jsonld`
  - terminal and revocation semantics are represented for completed/canceled processes and tasks, plus revoked/expired delegations and capability grants
  - SHIR projection surface is present via `bindings/valueflows_governed/valueflows-to-shir.projection.v0.1.json`, `docs/valueflows-to-shir-projection.md`, and `examples/valueflows-shir-receipt.example.json`
- `bindings/governed_intelligence/`
  - portable contract notes for the canonical Platform-scoped governed-intelligence model
  - binds the ontology, SHACL, JSON-LD context, JSON Schema, and vector manifest without introducing a duplicate Middle-layer ontology

## Specifications and profiles
- `docs/specs/governed-intelligence-object-model-v0.md`
  - canonical governed-intelligence object model for claims, anchors, evidence, policy decisions, vector candidates, action proposals, runtime receipts, learning events, revocations, and slash-topic profiles
- `docs/specs/lc-vsm-query-chatops-object-model-v0.md`
  - LC-VSM query and ChatOps semantic profile binding Matrix/WordOps surface events, Sherlock search packets, resolver plans, evidence bundles, semantic bindings, lifecycle cells, and DevSecOps audit events
  - Example trace: `examples/lc-vsm-query-chatops-sample.json`
- `docs/specs/view-governance.md`
  - ViewContract governance profile for authority-bound graph/analysis views, typed absence, disclosure modes, revocation epochs, and cross-repo ownership boundaries
- `docs/specs/prophet_artifact_contract.md`
  - Prophet computational artifact contract for governed artifact kinds, actions, runtime substrates, provenance, policy, evidence, metrics, and registrations
- `docs/specs/shir-v0.1.md`
  - Semantic Hyperknowledge Intermediate Representation draft: preserves n-ary relations, role bindings, context, evidence, temporal scope, policy scope, induction traces, projection loss reports, and receipts before downstream lowering
- `docs/specs/candidate-link-intelligence-plane.md`
  - governed candidate-link, link-prediction, scoring, evidence, curation, and promotion contract
- `docs/specs/candidate-link-to-shir.md`
  - mapping from binary links, hyperedges, alignments, evidence bundles, prediction traces, counterexamples, and receipts into SHIR
- `docs/specs/ontology-query-adapter.md`
  - governed ontology-query adapter contract for OWL/SHACL/schema-alignment/reasoning queries in the Lattice FederatedQueryPlane
- `docs/specs/semantic_enterprise_architecture.md`
  - semantic enterprise lifecycle, mapping, named graph, alignment, SHACL, and implementation contracts
- `docs/specs/valueflows-governed-canonical-v0.4.md`
  - governed ValueFlows profile spec
- `docs/specs/agentic-purple-team-and-mitre.md`
  - SCOPE-D/Ontogenesis semantic bridge for agentic-purple-team actions, adversarial scenarios, ATT&CK/ATLAS alignment, local SourceOS technique equivalents, SHACL gates, and future governed MITRE STIX/TAXII import pipeline
- `docs/specs/smart_home_privacy_gaia_hdt_bridge.md`
  - smart-home privacy bridge specification for Ontogenesis, GAIA, HolographMe/HDT, Sherlock, SourceOS, ProCybernetica, Sociosphere, and Policy Fabric
- `docs/banking-reference-crosswalk.md`
  - FIBO/BIAN reference-anchor crosswalk for the banking twin seed tranche; records alignment intent only and makes no conformance claim

## Supplemental registries and contexts
- `catalog/registry.ttl` and `catalog/registry.jsonld` — primary module registries
- `catalog/semantic_enterprise_registry.ttl` — supplemental semantic-enterprise registry tranche
- `catalog/knowledge_context_registry.ttl` — supplemental Knowledge Context registry tranche; transitional until #93 normalizes registry posture
- `catalog/reasoning_failure_registry.ttl` — supplemental reasoning-failure registry tranche; transitional until #93 normalizes registry posture
- `catalog/smart_home_privacy_registry.ttl` — supplemental smart-home privacy registry tranche; transitional until #93 normalizes registry posture
- `catalog/view_governance_registry.ttl` — supplemental View Governance registry tranche; transitional until #93 normalizes registry posture
- `catalog/prophet_artifact_registry.ttl` — supplemental Prophet Artifact registry tranche; transitional until #93 normalizes registry posture
- `catalog/banking_registry.ttl` — supplemental banking registry tranche; transitional until #93 normalizes registry posture
- `contexts/main.context.jsonld` — main JSON-LD context
- `contexts/semantic-enterprise.context.jsonld` — semantic-enterprise context
- `contexts/governed-intelligence.context.jsonld` — governed-intelligence context
- `contexts/knowledge-context.context.jsonld` — Knowledge Context context
- `contexts/reasoning-failure.context.jsonld` — reasoning-failure context
- `contexts/smart-home-privacy.context.jsonld` — smart-home privacy context
- `contexts/view-governance.context.jsonld` — View Governance context
- `contexts/prophet-artifact.context.jsonld` — Prophet Artifact context
- `contexts/banking.context.jsonld` — Banking context

## Gates and audits
- SHACL bundles: `shapes/core.shacl.ttl`, `shapes/ontogenesis.shacl.ttl`, `shapes/cybernetic-self.shacl.ttl`, `shapes/product-service.shacl.ttl`, `shapes/parsing-gates.ttl`, `shapes/ontology-query.shacl.ttl`, `shapes/valueflows-governed.shacl.ttl`, `shapes/michael-belief.shacl.ttl`, `shapes/human-digital-twin.shacl.ttl`, `shapes/kg_lifecycle.shacl.ttl`, `shapes/semantic_mapping.shacl.ttl`, `shapes/named_graph_governance.shacl.ttl`, `shapes/agentic-purple-team.shacl.ttl`, `shapes/governed_intelligence.shacl.ttl`, `shapes/knowledge-context.shacl.ttl`, `shapes/reasoning_failure.shacl.ttl`, `shapes/smart-home-privacy.shacl.ttl`, `shapes/view-governance.shacl.ttl`, `prophet/shapes/prophet_artifact.shacl.ttl`, `shapes/banking-core.shacl.ttl`
- Scripts:
  - parse validation, SHACL gates, JSON-LD roundtrip
  - dist build, ledger build/verify, detached signatures, SPDX SBOM
