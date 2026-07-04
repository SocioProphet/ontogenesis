# Constrained Multistate Pathway Design for Ontogenesis

Status: draft v0.1  
Owner: SocioProphet / Ontogenesis  
Primary source pattern: constrained multistate sequence design for nucleic acid reaction pathway engineering

## Purpose

This note generalizes a design pattern from constrained multistate nucleic-acid sequence design into an Ontogenesis-native doctrine for agentic, semantic, and runtime pathway engineering.

The source pattern is not imported as a biological claim. It is imported as a systems formulation: represent a desired pathway as multiple modeled states, represent undesired crosstalk explicitly, impose constraints during candidate generation, score the whole ensemble, and admit only designs whose global defect is below threshold.

In the source formulation, a reaction pathway is represented by target test tubes for reactant, intermediate, product, and crosstalk states. Each test tube has desired on-target complexes and undesired off-target complexes. Optimization reduces an ensemble defect while satisfying sequence constraints. The decisive architectural lesson is that positive design alone is insufficient; negative design against crosstalk is load-bearing.

## Translation

| Source formulation | Ontogenesis / SocioProphet generalization |
| --- | --- |
| Reaction pathway | Governed pathway, workflow, runtime transition, retrieval plan, fusion plan, or ontology promotion flow |
| Elementary step | A single state transition with declared preconditions, outputs, and constraints |
| Target test tube | State tube: bounded evaluation ensemble for one phase of the pathway |
| On-target complex | Desired state, artifact, evidence object, ontology write, API result, or runtime transition |
| Off-target complex | Prohibited or undesired interaction, false join, unsafe capability use, stale evidence path, crosstalk product, or invalid state |
| Global crosstalk tube | Cross-pathway interference suite spanning agents, sources, ontologies, policies, tools, and runtimes |
| Sequence constraints | SHACL, JSON Schema, OpenAPI, Rego/OPA, DID/capability, provenance, resource, namespace, and admission constraints |
| Ensemble defect | Weighted pathway defect score across on-target failures and off-target activations |
| Stop condition | Admission threshold before a pathway can be promoted |

## Doctrine

A pathway is not admissible merely because its happy path works.

A pathway is admissible only when:

1. each declared on-target state is reachable, valid, and evidence-bound;
2. modeled off-target states are suppressed below threshold;
3. constraints are enforced during generation and transition, not only checked after the fact;
4. global crosstalk is weighted strongly enough that it does not disappear as the number of systems grows;
5. failures observed in staging or production are promoted into the off-target ensemble.

This yields the SocioProphet analogue of multistate test tube design: every important agentic, semantic, retrieval, fusion, or runtime pathway gets an on-target ensemble and an off-target crosstalk ensemble.

## Formal sketch

A `PathwaySpec` is a tuple:

```text
P = (T, C, W, A, R)
```

where:

- `T` is a set of state tubes.
- `C` is a set of constraints.
- `W` is a set of defect weights.
- `A` is an admission rule.
- `R` is a receipt model binding states, checks, and results to provenance.

Each state tube `t ∈ T` contains:

```text
t = (On_t, Off_t, Context_t)
```

where:

- `On_t` is the set of desired states for that phase.
- `Off_t` is the set of explicitly modeled undesired states for that phase.
- `Context_t` is the bounded environment in which the phase is evaluated.

The pathway defect is a weighted normalized score:

```text
D(P) = normalize(
  Σ_t W_t · (
    Σ_o∈On_t defect_on(o)
    +
    Σ_x∈Off_t defect_off(x)
  )
)
```

The pathway is admissible only if:

```text
D(P) ≤ threshold(P)
```

and all hard constraints in `C` pass.

This is not a thermodynamic model. It is a governance and validation model. The scoring function may be implemented as deterministic validation, model-based evaluation, property testing, adversarial fixtures, provenance checks, or a combination of these.

## Constraint classes

The design pattern maps cleanly onto Ontogenesis constraints:

| Constraint class | Examples |
| --- | --- |
| Assignment | Required namespace, fixed source, required model, fixed issuer, fixed API |
| Match | Entity identity agreement across RDF, JSON-LD, search index, and UI receipt |
| Complementarity | Required relationship pairing, inverse edge, capability-to-policy match, issuer-to-subject binding |
| Composition | Required mix of source types, minimum evidence diversity, feature bundle profile |
| Similarity | Controlled semantic proximity, bounded entity resolution, nearest-neighbor threshold |
| Pattern prevention | Forbidden prompt/tool pattern, forbidden ontology namespace pattern, unsafe API sequence |
| Library | Allowed runtime images, allowed tools, allowed policy templates, approved adapters |
| Window | Bounded source corpus, region/time window, transcriptome analogue, deployment scope |

## First implementation target: Sherlock retrieval safety

Sherlock is the lowest-friction first target because retrieval already has natural on-target and off-target states.

Example state tubes:

1. `candidate_retrieval`
   - On-target: relevant documents, correct entities, current versions, source receipts.
   - Off-target: stale docs, semantically similar but wrong entities, duplicated claims, untrusted sources.

2. `evidence_assembly`
   - On-target: cited claims, provenance-preserving snippets, contradiction scan.
   - Off-target: uncited synthesis, citation laundering, collapsed uncertainty, cross-source identity collision.

3. `answer_admission`
   - On-target: answer grounded in allowed evidence with explicit uncertainty.
   - Off-target: unsupported claim, stale fact, hidden source conflict, policy-violating disclosure.

4. `global_crosstalk`
   - On-target: no unmodeled cross-index contamination.
   - Off-target: ontology collision, source drift, near-duplicate poisoning, unrelated-but-plausible semantic neighbor.

## Second implementation target: GAIA fusion safety

GAIA state tubes should model geospatial and temporal fusion:

1. `bounded_ingest`
   - On-target: region-bounded features with CRS, bbox, H3, source attribution, and receipts.
   - Off-target: out-of-bounds features, missing attribution, invalid geometry, unknown CRS.

2. `layer_fusion`
   - On-target: OSM, EO, weather, terrain, and observation layers kept provenance-distinct.
   - Off-target: false entity merge, time-validity mismatch, uncertainty erasure, stale observation promotion.

3. `agent_review`
   - On-target: agent recommendation bounded by evidence and declared uncertainty.
   - Off-target: unsafe operational instruction, ungrounded causal inference, irreversible action without admission gate.

## Third implementation target: SourceOS boot/runtime admission

SourceOS can use the same pattern for lifecycle integrity:

1. `boot_release_selection`
   - On-target: signed BootReleaseSet, expected PCR policy, valid manifest chain.
   - Off-target: stale manifest, unsigned artifact, wrong issuer, hash-chain discontinuity.

2. `ignition_validation`
   - On-target: valid Butane/Ignition config, policy-compatible services, declared recovery path.
   - Off-target: host mutation outside policy, secret material embedded, unmanaged privileged service.

3. `runtime_admission`
   - On-target: permitted agent/runtime image with SBOM and capability scope.
   - Off-target: untrusted image, excess capability, policy bypass, identity mismatch.

## Schema landing

The companion schema is `schemas/pathway-spec.schema.json`.

The schema is intentionally small in v0.1. It is a carrier for:

- `id`, `version`, `title`, and `scope`;
- state tubes with on-targets and off-targets;
- constraints;
- defect weights;
- admission threshold;
- receipts and evidence requirements.

It should later project into SHACL shapes, JSON-LD contexts, OpenAPI admission endpoints, and CI fixtures.

## CI and validation plan

M0 — Doctrine captured  
Land this note and the v0.1 schema.

M1 — Static schema validation  
Add JSON Schema validation for example pathway specs.

M2 — SHACL projection  
Map `PathwaySpec`, `StateTube`, `OnTarget`, `OffTarget`, `Constraint`, and `AdmissionResult` into RDF/SHACL.

M3 — Sherlock fixture suite  
Create retrieval crosstalk fixtures and compute a deterministic pathway defect score.

M4 — GAIA fixture suite  
Create bounded-ingest and layer-fusion crosstalk fixtures.

M5 — SourceOS lifecycle suite  
Create boot/runtime admission fixtures for manifest, signature, policy, and capability failure modes.

M6 — Admission gate  
Add CI status that blocks promotion when hard constraints fail or weighted defect exceeds threshold.

## Non-goals

This note does not claim that nucleic-acid thermodynamics maps directly to agentic systems, ontologies, search, geospatial fusion, or OS lifecycle state.

This note does not replace SHACL, OPA, OpenAPI, SBOM, DID, or provenance gates.

This note provides the unifying design doctrine for using those gates as a multistate pathway ensemble rather than a bag of isolated checks.

## Open questions

1. Which pathway family becomes the first production gate: Sherlock retrieval, GAIA fusion, or SourceOS lifecycle?
2. Should defect weights be normalized per tube, per target, per severity, or per operational risk?
3. How do we promote observed failures into the global crosstalk ensemble without overfitting?
4. Which execution layer owns the admission result: Ontogenesis, Policy Fabric, Sociosphere, or prophet-platform?
5. What is the minimum evidence receipt format that can serve all three first targets?
