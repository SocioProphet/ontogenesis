# Business ontology bridge

## Purpose

This document specifies how to extend Ontogenesis with a **business ontology + runtime-governance lane** without creating a competing semantic stack.

The goal is to keep Ontogenesis as the canonical authored ontology/governance repository while allowing downstream compiler/runtime systems to derive executable IR for business analysis, value-driver reasoning, source binding, benchmark selection, and critic-gated recommendations.

This document assumes the current upstream Ontogenesis baseline captured in:

- `docs/specs/ontogenesis_upstream_capture_20260412.md`

---

## Core principle

Do **not** build a rival ontology tree for business semantics.

Instead:

- author canonical business semantics as Ontogenesis modules
- register them in Ontogenesis registry surfaces
- gate them with SHACL where semantic promotion invariants matter
- compile them downstream into executable IR / runtime forms

That yields this shape:

`Ontogenesis authored modules -> registry + SHACL + dist/audit/ledger -> downstream compiler -> PackIR / runtime artifacts`

---

## What belongs upstream vs downstream

### Upstream Ontogenesis should own

- canonical classes / properties / individuals
- namespace discipline
- module boundaries and SemVer
- import graph
- JSON-LD contexts and examples
- SHACL promotion gates
- release / audit / ledger / signature / SBOM posture

### Downstream compiler/runtime should own

- normalized executable IR (`PackIR`, `PackArtifact`, similar compiled forms)
- formula AST and execution plan
- conflict-set scoring and binding resolution
- freshness scoring and precedence resolution
- benchmark ranking/blending implementation
- runtime critic and workflow gating execution
- scenario overlays and report generation

The downstream layer is executable; the upstream layer is canonical and governed.

---

## Proposed new Ontogenesis module family

The current repo has strong platform / Prophet / EPI / generic domain coverage but lacks a first-class business-analysis lane.

The proposed first module family is:

### 1. `Domains/business_core.ttl`

Canonical business entities and relationships.

Scope:

- Company
- BusinessUnit
- Offering / Product / SKU / Module
- Customer / CustomerSegment
- Channel / Partner / RouteToMarket
- Contract / Subscription / Renewal / Amendment
- RevenueStream / CostPool / CapacityUnit
- Geography / RegulatoryRegion / Scenario
- Competitor / Market / BenchmarkCohort

Purpose:

This becomes the business entity substrate that downstream analysis/runtime work binds against.

### 2. `Domains/business_metrics.ttl`

Canonical business and unit-economics metric concepts.

Initial scope:

- ARR / MRR / recurring revenue
- GRR / NRR / logo retention / churn variants
- CAC / CAC payback / LTV / payback basis components
- gross margin / contribution margin
- ASP / ACV / AOV / take rate
- utilization / reimbursement / denial rate / yield / inventory turns where applicable
- metric metadata primitives such as unit family, grain family, time behavior, and scope family

Purpose:

This becomes the concept surface for business metrics and removes ambiguity around overloaded metric names.

### 3. `Domains/business_drivers.ttl`

Canonical causal/operational driver and lever vocabulary.

Initial scope:

- DriverEdge
- Lever
- Relation sign (positive / negative / mixed)
- lag
- elasticity / range
- condition / saturation / regime
- evidence policy
- driver class examples such as:
  - localization reduces churn
  - capacity constrains throughput
  - review delay depresses win rate
  - pricing uplift modifies expansion ARR

Purpose:

This is the upstream causal layer that supports downstream value-driver graphs without forcing the causal graph to live only in runtime code.

### 4. `Domains/business_benchmarks.ttl`

Canonical benchmark-record and selector vocabulary.

Initial scope:

- BenchmarkRecord
- SampleFrame
- SelectorProfile
- NormalizationProfile
- BenchmarkQuality
- benchmark evidence and sample size fields
- freshness / provenance / normalization quality surfaces

Purpose:

This gives benchmark priors and benchmark evidence a governed semantic shape upstream.

### 5. `Middle/observations_runtime.ttl`

Cross-domain observation/binding/runtime-governance vocabulary.

Why `Middle` instead of `Domains`:

Observation, binding, freshness, precedence, and restatement semantics are not purely business-specific. They are runtime-governance surfaces that can apply beyond business analytics.

Initial scope:

- SourceProfile
- RawObservation
- CanonicalObservation
- ResolvedBinding
- DerivationClass
- FreshnessPolicy
- BindingEpoch
- Restatement
- PeriodState (`open`, `soft_closed`, `hard_closed`)
- SourceEvent / Correction / Tombstone / NullClass

Purpose:

This gives the downstream binding engine an upstream canonical semantic basis for observations and historical rebinding.

### 6. `Middle/workflow_critic.ttl`

Cross-domain workflow-output gating and support-quality vocabulary.

Initial scope:

- EvaluatedMetric
- Claim
- Recommendation
- CriticFinding
- WorkflowGateDecision
- OutputMode
- support level / caveat / suppress / publish-with-caveat surfaces
- claim classes (`descriptive`, `comparative`, `forecast`, `causal`, `prescriptive`)

Purpose:

This gives the runtime critic/governance layer an upstream semantic contract instead of leaving it entirely implicit in code.

---

## Proposed supporting assets

### SHACL bundles

Add new SHACL bundles for business and runtime-governance modules.

Suggested files:

- `shapes/business_core.shacl.ttl`
- `shapes/business_metrics.shacl.ttl`
- `shapes/business_benchmarks.shacl.ttl`
- `shapes/observations_runtime.shacl.ttl`
- `shapes/workflow_critic.shacl.ttl`

Examples of gates to encode:

- benchmark records must declare metric concept + selector + sample frame + stats
- business metrics must declare unit/grain/time-behavior metadata
- driver edges must declare source, target, sign, and lag
- restatements must point to prior binding epoch or source correction
- recommendations must reference at least one modeled lever and one target metric

### JSON-LD contexts

Suggested contexts:

- `contexts/business.context.jsonld`
- `contexts/observations_runtime.context.jsonld`
- `contexts/workflow_critic.context.jsonld`

### Examples

Suggested examples:

- `examples/business_company_demo.ttl`
- `examples/business_metric_demo.ttl`
- `examples/benchmark_demo.jsonld`
- `examples/resolved_binding_demo.jsonld`
- `examples/workflow_gate_demo.jsonld`

Purpose:

Examples should show how the semantics work in practice and should be used by tests and documentation.

---

## Import-bridge design into downstream compiler/runtime

The downstream compiler should treat Ontogenesis modules as canonical source materials.

### Input surfaces to ingest

At minimum:

- `catalog/registry.ttl`
- `catalog/registry.jsonld`
- canonical namespace rules from `docs/specs/namespaces.md`
- registered Turtle modules
- SHACL bundles
- relevant JSON-LD contexts

### What the import bridge should preserve

- module path
- layer
- base IRI
- semver / status
- import relations
- canonical concept/property IRIs
- shape/gate provenance
- example provenance

### What the import bridge should compile into

For downstream executable use, the bridge should derive:

- concept registry entries
- alias tables / label maps
- property/type surfaces for binding and reasoning
- module dependency graph
- gate metadata for compiler/runtime validation
- version-aware provenance records for compiled artifacts

### Hard rule

No downstream compiled concept should lose its traceability back to:

- Ontogenesis module path
- module semver / `owl:versionInfo`
- canonical IRI
- registry record
- applicable SHACL gate(s)

---

## Alignment with existing Ontogenesis modules

The proposed business/runtime modules should not ignore the current upstream ontology backbone.

### Alignment to Upper

New modules should reuse `upper:` primitives such as:

- `Entity`
- `Process`
- `Agent`
- `System`
- `InformationArtifact`
- `Policy`
- `Evidence`

### Alignment to Middle system architecture

Business/runtime modules should reuse or reference:

- spaces
n- gates
- update flows

This matters especially for source ingestion, promotion, and outside→inside adjudication.

### Alignment to Middle action ontology

Recommendation/workflow semantics should connect to:

- action types
- states
- traces
- coordination patterns

This is important for agentic execution and auditability.

### Alignment to Prophet modules

Capability-bearing business/runtime surfaces should align to:

- `ServiceDescriptor`
- `CapabilityDescriptor`
- carriers such as `schemaRef` and `leafRef`

This matters if business/runtime modules are surfaced through Prophet-managed capabilities.

### Alignment to EPI / Noether

Learning, assessment, and report-based evidence should be able to reference:

- `epi:Report`
- `learn:Assessment`
- `nl:LayerContract`

This matters for curriculum, evaluation, and optimization-lane integration.

---

## Suggested first implementation order

### Phase 1 — semantic substrate

Author and register:

- `Domains/business_core.ttl`
- `Domains/business_metrics.ttl`
- `Domains/business_drivers.ttl`
- `Domains/business_benchmarks.ttl`
- `Middle/observations_runtime.ttl`
- `Middle/workflow_critic.ttl`

Add registry entries and minimal SHACL bundles.

### Phase 2 — JSON-LD and examples

Add contexts and example files for:

- company / business unit / product relationships
- metric concept declarations
- benchmark records
- resolved binding / restatement examples
- workflow gate / recommendation examples

### Phase 3 — import bridge

Implement downstream compiler support that:

- reads Ontogenesis registry and module graph
- builds runtime concept tables
- compiles gate metadata into executable validation/rule sets
- emits PackIR/PackArtifact-style runtime structures with provenance back to Ontogenesis

### Phase 4 — runtime integration

Use the upstream semantic basis for:

- binding resolution
- benchmark selection
- critic gating
- scenario overlay audit
- recommendation support-quality checks

---

## Proposed first SHACL invariants

### Business metric invariants

Every canonical business metric should declare:

- unit family
- grain family
- time behavior
- scope family

### Benchmark invariants

Every benchmark record should declare:

- metric concept
- selector profile
- sample frame
- normalization profile
- stats
- evidence/provenance surface

### Observation / binding invariants

Every resolved binding should declare:

- concept
- selected value
- unit
- derivation class
- effective period
- source lineage or derived-from lineage
- binding epoch

### Critic / recommendation invariants

Every recommendation should declare:

- lever
- target metric
- support level
- at least one dependency quality surface

---

## What should *not* be done

1. Do not model business/runtime semantics only in downstream code with no Ontogenesis source module.
2. Do not create a rival namespace detached from the Ontogenesis base IRI unless explicitly justified.
3. Do not bypass registry entries or SHACL because the semantics seem “obvious.”
4. Do not flatten benchmark, observation, and recommendation semantics into informal docs only.
5. Do not let compiled runtime artifacts become the canonical authored truth.

---

## Deliverables this bridge is meant to unlock

Once the proposed business/runtime modules exist upstream, downstream systems should be able to:

- compile a governed concept registry directly from Ontogenesis
- bind live source observations to canonical business metric concepts
- track restatements and binding epochs semantically
- rank and blend benchmark records with governed selector/provenance structure
- produce claims/recommendations with explicit support levels and caveats
- reason over business actions/levers in a way that aligns with existing Prophet/action/state/trace semantics

---

## Immediate follow-on tasks

1. Draft the first two ontology files:
   - `Domains/business_core.ttl`
   - `Domains/business_metrics.ttl`
2. Register them in `catalog/registry.ttl` and `catalog/registry.jsonld`.
3. Add minimal SHACL bundles for metric metadata completeness.
4. Add at least one JSON-LD context and one example file.
5. Build the first downstream import-bridge prototype against those modules.

---

## Status

This document is a bridge spec, not the implementation itself.

It should be updated when:

- the first business modules land upstream
- SHACL bundles and contexts are added
- downstream import-bridge code is implemented
- runtime binding/critic semantics stabilize enough to harden the ontology split between `Middle` and `Domains`
