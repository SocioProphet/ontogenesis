# LC-VSM Query and ChatOps Object Model v0

Status: draft, additive profile

Parent model: `docs/specs/governed-intelligence-object-model-v0.md`

Related systems: `sherlock-search`, `sociosphere`, `prophet-platform`, `global-devsecops-intelligence`, `proofsoc-core`, `gitspine`

## Purpose

This profile binds Lifecycle-Cell / Viable-System-Model style governance to SocioProphet query, Sherlock Search, and Matrix ChatOps flows.

It does not define a Matrix homeserver implementation, a Sherlock resolver implementation, or a runtime orchestration engine. It defines the durable semantic objects that those systems emit, consume, or certify.

The central flow is:

```text
SurfaceEvent
  -> QueryIntentProfile
  -> SherlockSearchPacket
  -> ResolverPlan
  -> ResolverResult[]
  -> EvidenceBundleProfile
  -> SemanticBindingProfile
  -> SocioGraphClaim / ProofCertificate / OpsEventEnvelope
```

## Non-goals

- Do not place Matrix protocol code in Ontogenesis.
- Do not place resolver code in Ontogenesis.
- Do not move WordOps or AgentTerm surface-adapter authority out of `prophet-platform`.
- Do not move federated routing authority out of `sociosphere`.
- Do not make every chat message a promoted ontology claim.

Ontogenesis owns the semantic lift: durable classes, relations, constraints, examples, and portable contracts.

## Core objects

### LifecyclePhaseProfile

A lifecycle phase profile names the governance phase in which a query, decision, action, or evidence object currently sits.

Recommended phase identifiers:

- `intake`
- `normalize_intent`
- `plan_resolution`
- `retrieve`
- `validate_evidence`
- `bind_semantics`
- `render_response`
- `propose_action`
- `approve_action`
- `execute_action`
- `audit`
- `retain_or_retire`

The phase profile should preserve status, entrance criteria, exit criteria, owners, gate references, and linked evidence.

### ActorStratumProfile

An actor stratum profile identifies the accountable actor class for a lifecycle cell.

Recommended strata:

- `human_user`
- `support_operator`
- `agent`
- `resolver`
- `policy_authority`
- `runtime_surface`
- `repository_owner`
- `compliance_observer`
- `external_system`

### OperationalArtifactProfile

An operational artifact profile describes a concrete object crossing a boundary: Matrix event, WordOps `IntentEnvelope`, Sherlock search packet, resolver result, evidence bundle, response envelope, action proposal, runtime receipt, issue, PR, commit, CI run, or OpsEvent envelope.

Every operational artifact should carry:

- `artifact_id`
- `artifact_kind`
- `source_system`
- `created_at`
- `producer`
- `integrity_ref` when available
- `policy_scope`
- `evidence_refs`

### ConstraintProfile

A constraint profile captures a gate or rule that must hold before the artifact can move phases.

Common constraint families:

- source-fidelity constraints
- room/channel authorization constraints
- resolver-scope constraints
- privacy and retention constraints
- action-admission constraints
- provenance completeness constraints
- proof-promotion constraints
- disclosure/rendering constraints

### DecisionProfile

A decision profile records a nontrivial branch in the query or action lifecycle.

Recommended decision kinds:

- `route_query`
- `select_resolver`
- `suppress_resolver`
- `accept_evidence`
- `reject_evidence`
- `escalate_to_operator`
- `render_answer`
- `propose_action`
- `approve_action`
- `deny_action`
- `promote_claim`
- `retire_claim`

### EvidenceBundleProfile

An evidence bundle profile aggregates evidence atoms produced by Sherlock, repository search, ops ingestion, Matrix thread context, document lookup, CI, runtime telemetry, or human operator annotation.

Each bundle should include:

- bundle identifier
- query or intent reference
- resolver references
- evidence atom references
- source-fidelity rating
- freshness rating
- confidence statement
- known gaps
- claim-promotion recommendation

### MatrixCellProfile

A matrix cell profile binds one lifecycle phase to one accountable actor stratum.

Example cells:

- `(intake, runtime_surface)` for Matrix/WordOps intake
- `(plan_resolution, agent)` for Sherlock query planning
- `(retrieve, resolver)` for adapter execution
- `(validate_evidence, policy_authority)` for evidence gates
- `(bind_semantics, ontogenesis)` for semantic lift
- `(audit, compliance_observer)` for DevSecOps/ProofSoc handoff

A cell may declare required inputs, outputs, controls, KPIs, and escalation policy.

### DomainFabricProfile

A domain fabric profile extends the core lifecycle model for a concrete domain: support, premium support, incident response, source-code discovery, legal/compliance, product intelligence, civic/governance, privacy, or customer success.

Domain fabrics must be additive. They may specialize gate rules, KPIs, resolver priority, ontology bindings, and evidence requirements, but should not redefine the core lifecycle phases.

### SurfaceEventProfile

A surface event profile describes a raw event entering from Matrix, WordOps, AgentTerm, GitHub, Gmail, Docs, shell, browser, or another interface.

For Matrix ChatOps, the minimum fields are:

- `room_ref`
- `event_ref`
- `thread_ref` when available
- `sender_ref`
- `surface_timestamp`
- `command_or_message_kind`
- `redaction_or_edit_state`
- `authorization_context`

### QueryIntentProfile

A query intent profile is the semantic form of a user/operator/agent request after surface normalization.

Minimum fields:

- `intent_id`
- `surface_event_ref`
- `requested_capability`
- `topic_refs`
- `slash_topic_refs`
- `target_scope`
- `freshness_requirement`
- `evidence_requirement`
- `actionability_level`
- `policy_scope`

### ResolverProfile

A resolver profile describes a source adapter or tool available to Sherlock Search.

Resolver profiles should declare:

- resolver identifier
- supported artifact kinds
- supported scopes
- source-fidelity guarantees
- freshness behavior
- authorization requirements
- output evidence shape
- known blind spots

### SemanticBindingProfile

A semantic binding profile links operational outputs to Ontogenesis durable objects.

Common bindings:

- `QueryIntentProfile` -> `SlashTopicProfile`
- `ResolverResult` -> `EvidenceAtom`
- `EvidenceBundleProfile` -> `SocioGraphClaim`
- `DecisionProfile` -> `PolicyDecision`
- `ActionProposal` -> `ActionAdmission`
- `RuntimeReceipt` -> `OpsEventEnvelope`
- promoted claims -> `ProofCertificate`

## Required invariants

1. A Matrix or ChatOps event is not itself a claim. It is a surface event until normalized and bound.
2. A Sherlock result is not itself a promoted fact. It is evidence until promoted through policy and proof gates.
3. A resolver must declare its source-fidelity class before its output can enter an evidence bundle.
4. A query answer that proposes an action must produce an action proposal, not an implicit execution.
5. A runtime execution must produce a runtime receipt and an ops event.
6. An ontology update must be traceable to evidence atoms and a decision profile.
7. A domain fabric may refine gates and KPIs but must not fork the core lifecycle vocabulary.
8. Stale evidence must be represented explicitly; it must not be silently promoted.
9. Redacted or edited surface events must preserve their audit state.
10. Human approval boundaries must remain explicit for high-impact actions.

## Repository boundary map

- `ontogenesis` owns this semantic object profile and examples.
- `sherlock-search` owns packet, resolver, resolver-plan, search result, and evidence-bundle runtime design.
- `prophet-platform` owns WordOps and AgentTerm surface adapters and `IntentEnvelope`/`ResponseEnvelope` integration.
- `sociosphere` owns federated query-spine routing, registry binding, and stack-level governance placement.
- `global-devsecops-intelligence` owns measurable `OpsEventEnvelope` ingestion, metrics, and operational audit read models.
- `proofsoc-core` owns proof obligations, trust-policy checks, and proof-certificate promotion.
- `gitspine` owns repository graph, commit topology, and source-code lineage evidence.

## Promotion path

This v0 profile is intentionally documentation-first. Promotion to enforced ontology module should add, in order:

1. JSON-LD context terms.
2. RDF/OWL class surface under `Platform/GovernedIntelligence/` or a sibling `Platform/QueryChatOps/` module.
3. SHACL gates for required references and source-fidelity fields.
4. Example JSON-LD and RDF fixtures.
5. Registry entries and dist regeneration.
6. CI roundtrip and SHACL checks.

## Minimal end-to-end trace

```text
Matrix message in support room
  -> WordOps SurfaceEventProfile
  -> QueryIntentProfile: "find canonical Sherlock/Matrix ChatOps design"
  -> SherlockSearchPacket scoped to SocioProphet repos
  -> ResolverPlan selecting GitHub, docs, issues, PRs, and ontology resolvers
  -> EvidenceBundleProfile with cited files and PRs
  -> SemanticBindingProfile binding evidence to SlashTopicProfile and SocioGraphClaim candidates
  -> ResponseEnvelope rendered back to room
  -> OpsEventEnvelope emitted for query, resolver use, evidence production, and response
```

## Open gates

- Define exact JSON-LD context names after the runtime packet fields stabilize in `sherlock-search`.
- Decide whether `MatrixCellProfile` lives under governed intelligence or a dedicated LC-VSM module.
- Add proof-promotion gates for claims derived from chat context.
- Add retention/redaction semantics for Matrix room evidence.
- Add source-fidelity tiers shared with SocioSphere registry and DevSecOps ingestion.
