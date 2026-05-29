# Privacy Non-Linkability Doctrine v0

Status: draft  
Authority plane: `SocioProphet/ontogenesis`  
Scope: governed-intelligence privacy constraints over learning, linking, memory, vectors, graphs, evidence, claims, actions, and receipts

## Purpose

This doctrine defines the first Ontogenesis-level privacy boundary for non-learning and non-linkability constraints in the SocioProphet governed-intelligence architecture.

The core distinction is:

- `DoNotLearn` governs representation formation.
- `DoNotLink` governs relation formation.

A system can violate `DoNotLearn` without linking anything, for example by embedding private text into a reusable vector index. A system can violate `DoNotLink` without learning anything new, for example by joining two already-existing identifiers across domains.

This doctrine is a semantic control artifact. It does not yet add Turtle terms, SHACL gates, JSON-LD context terms, JSON Schema fields, or runtime enforcement.

## Relationship to governed intelligence

This doctrine extends the governed-intelligence object model without replacing it.

The governed-intelligence loop remains:

```text
Observe -> Anchor -> Normalize -> Propose -> Explain -> Verify -> Govern -> Act -> Receipt -> Learn
```

Privacy constraints apply across the loop. They are especially important at the boundary between evidence and claim formation, between candidate recall and durable memory, between graph inference and entity resolution, and between action admission and runtime effects.

The existing invariant that raw model output, graph candidates, and vector candidates are proposals remains intact. A privacy constraint can block or restrict a proposal even if that proposal is otherwise structurally valid.

## Definitions

### ProtectedSignal

A `ProtectedSignal` is any source signal, observation, identifier, anchor, feature, embedding, graph relation, user-supplied artifact, workroom event, or derived representation that may not be learned from, linked, or reused outside its admitted policy scope.

Protected signals may include direct identifiers, quasi-identifiers, behavioral traces, private text, latent-vector neighborhoods, sensitive graph edges, audio segments, workroom participation signals, device or account metadata, fraud/risk indicators, and any signal that can reconstruct or materially narrow identity, affiliation, intent, vulnerability, or protected context.

### LearningOperation

A `LearningOperation` is any operation that updates or produces a reusable representation.

Examples include training, fine-tuning, embedding, summarization into durable memory, clustering, profile construction, topic-pack promotion, feature extraction, vector-index insertion, policy learning, model-state updates, memory-mesh updates, entity-profile enrichment, and feedback-loop incorporation.

### LinkingOperation

A `LinkingOperation` is any operation that creates, preserves, exposes, infers, or operationalizes a relation across protected scopes.

Examples include entity resolution, join-key creation, cross-domain graph edge creation, latent nearest-neighbor linking, identity bridge creation, workroom-to-workroom linkage, evidence-context linkage, account/device/person correlation, topic-pack membership linkage, and equivalence-class promotion.

### PrivacyBoundary

A `PrivacyBoundary` is a policy scope separating domains that may not be co-learned, joined, projected, searched, clustered, or operationalized together without explicit admission.

Privacy boundaries may be defined around user, tenant, workspace, workroom, engagement, jurisdiction, legal basis, consent scope, source artifact, evidence domain, risk tier, investigation boundary, or model-governance scope.

### NonLearningConstraint

A `NonLearningConstraint` prohibits representation formation from a protected signal unless a policy decision explicitly allows the proposed learning operation.

A non-learning constraint may require deletion, exclusion from training, exclusion from embeddings, exclusion from summaries, exclusion from durable memory, exclusion from profile construction, or use only in ephemeral computation.

### NonLinkabilityConstraint

A `NonLinkabilityConstraint` prohibits relation formation across protected scopes unless a policy decision explicitly allows the proposed linking operation.

A non-linkability constraint may block join keys, graph edges, identity bridges, latent-neighbor exposure, cross-topic membership, profile merges, context joins, or workroom-to-workroom references.

### PrivacyDecision

A `PrivacyDecision` is a policy decision over a proposed learning or linking operation.

The initial decision vocabulary reuses the governed-intelligence policy vocabulary:

```text
allow | deny | require_review | provisional
```

Future versions may add privacy-specific disposition terms, but v0 intentionally reuses the existing admission vocabulary.

### PrivacyReceipt

A `PrivacyReceipt` records the outcome of privacy enforcement over a learning or linking operation.

A receipt should identify the proposed operation, target signal or relation, policy decision, enforcement mode, scope, timestamp, and resulting disposition.

Example dispositions include:

```text
blocked | admitted | minimized | redacted | aggregated | anonymized | ephemeral_only | expired | require_review
```

## DoNotLearn

`DoNotLearn` means a system must not transform, train on, embed, summarize, memorize, cluster, profile, generalize from, or otherwise incorporate a protected signal into any reusable representation unless an explicit policy decision permits that learning operation.

The prohibition covers direct and indirect learning. A system violates `DoNotLearn` if the protected signal can materially influence a durable representation, even if the original signal is no longer directly visible.

### DoNotLearn applies to

- model training and fine-tuning;
- embedding and vector-index insertion;
- durable memory summaries;
- user, entity, tenant, device, or workroom profiles;
- topic packs and semantic membranes;
- graph-derived features;
- policy-learning feedback loops;
- reusable agent state;
- downstream datasets and evaluation corpora.

### DoNotLearn does not prohibit

- ephemeral computation that does not update reusable state;
- policy-gated inspection for safety, security, compliance, or debugging;
- source-backed evidence use inside its admitted scope;
- aggregate statistics when re-identification and reconstruction risks are controlled by policy.

Those exceptions require explicit scope and receipt semantics. They are not implied permissions.

## DoNotLink

`DoNotLink` means a system must not create, infer, preserve, expose, or operationalize a join path between protected domains, subjects, anchors, vector spaces, latent representations, graphs, workrooms, evidence contexts, accounts, devices, or topics unless an explicit policy decision permits that linking operation.

The prohibition covers direct and indirect linking. A system violates `DoNotLink` if it creates a practical bridge that allows identity, affiliation, source, intent, or protected context to be reconstructed across a privacy boundary.

### DoNotLink applies to

- entity resolution;
- cross-domain join keys;
- account-device-person correlations;
- graph edges and equivalence relations;
- latent nearest-neighbor exposure;
- vector-space bridges;
- shared topic-pack membership;
- workroom-to-workroom references;
- evidence-context joins;
- provenance bridges that reveal protected source identity.

### DoNotLink does not prohibit

- independent processing inside each admitted scope;
- aggregate reporting where reconstruction risk is controlled;
- explicit policy-approved joins with receipts;
- human-readable citations that do not create reusable join surfaces beyond the admitted scope.

Those exceptions require policy admission and receipt generation.

## Binding to governed-intelligence objects

| Governed-intelligence object | Privacy binding |
| --- | --- |
| `Anchor` | May carry privacy scope, selector-level protection, source boundary, and non-learning/non-linkability flags. |
| `Evidence` | May support or oppose a claim while still being non-learnable, non-linkable, or scope-limited. |
| `Claim` | May be proposed from protected evidence, but claim admission does not automatically authorize learning or linking. |
| `VectorCandidate` | Remains `candidate_only`; must not become a durable cross-domain bridge when source signals are protected. |
| `PolicyDecision` | May admit, deny, require review, or provisionally admit learning/linking operations. |
| `ActionProposal` | Any effectful learning or linking action must be explicitly admitted before execution. |
| `ActionAdmission` | Carries the admitted state for the proposed learning/linking action. |
| `RuntimeReceipt` | Records whether privacy constraints were enforced and what disposition occurred. |
| `LearningEvent` | Is not automatically legitimate; a learning event may be denied by `DoNotLearn`. |
| `SlashTopicProfile` | Must not become a hidden linking membrane across protected scopes. |
| `Revocation` | May withdraw a prior learning or linking admission and require downstream cleanup. |

## Required invariants

1. A `VectorCandidate` is not an admitted claim and is not a privacy admission.
2. A valid `Claim` is not a learning permission.
3. A valid `Evidence` object is not a linking permission.
4. A source citation is not permission to add the source to reusable memory.
5. A search result is not permission to create a graph edge.
6. A workroom event is not permission to profile a participant outside the workroom scope.
7. A policy `allow` decision must identify the operation, scope, basis, and receipt expectation.
8. If the operation crosses a privacy boundary and has no explicit privacy decision, the default disposition is `require_review` or `deny`, depending on consuming policy.

## Failure modes

### Silent memory capture

A private artifact is summarized into durable memory, topic packs, embeddings, or model context without explicit admission.

Primary constraint: `DoNotLearn`.

### Latent identity reconstruction

A system does not store a direct identifier but preserves enough vector, graph, behavioral, or quasi-identifier structure to reconstruct identity or affiliation.

Primary constraints: `DoNotLearn` and `DoNotLink`.

### Cross-workroom leakage

A person, claim, document, or topic from one workroom becomes visible or actionable in another workroom without an admitted bridge.

Primary constraint: `DoNotLink`.

### Candidate-to-claim laundering

A vector or graph candidate is converted into an admitted claim without source-backed evidence and policy review.

Primary constraints: governed-intelligence candidate-only invariant and `DoNotLink`.

### Feedback-loop contamination

An evaluation, correction, or operator action derived from protected material becomes training data or policy-learning input without admission.

Primary constraint: `DoNotLearn`.

## Enforcement posture for v0

This v0 doctrine is a specification anchor. It creates vocabulary obligations and implementation direction but does not yet enforce constraints mechanically.

The next implementation stages should be:

1. add ontology terms in a dedicated platform module;
2. add SHACL shapes for required privacy-operation fields;
3. add JSON-LD context terms;
4. add example JSON-LD fixtures for denied and review-required operations;
5. add negative fixtures once the object model stabilizes;
6. add validators only after fixture semantics are stable.

## Proposed file targets for later stages

Likely implementation paths:

```text
Platform/GovernedIntelligence/privacy-nonlinkability.ttl
shapes/privacy_nonlinkability.shacl.ttl
contexts/privacy-nonlinkability.context.jsonld
examples/privacy-nonlinkability/do-not-learn-denied.example.jsonld
examples/privacy-nonlinkability/do-not-link-require-review.example.jsonld
```

This v0 doctrine intentionally does not mutate those surfaces.

## Repo boundary notes

| Repo | Boundary |
| --- | --- |
| `ontogenesis` | Canonical vocabulary, doctrine, shapes, contexts, and examples for non-learning and non-linkability semantics. |
| `policy-fabric` / `guardrail-fabric` | Runtime admission policies and decision logic. |
| `model-governance-ledger` | Training, inference, evaluation, drift, feedback, and learning-event receipts. |
| `prophet-platform` | Workroom, memory, topic-pack, and user-facing substrate integration. |
| `agentplane` | Action proposal, action admission, and runtime receipt enforcement for effectful operations. |
| `sherlock-search` | Retrieval candidates, source anchors, answer candidates, and candidate-only discipline. |
| `holmes` | Reasoning traces and proof/explanation boundaries; no independent admission authority. |
| `sociosphere` | Cross-repo adoption projection and recovery-ledger coordination. |

## Non-goals

This doctrine does not claim full privacy compliance, legal sufficiency, anonymization guarantees, differential privacy guarantees, or complete enforcement. It does not replace jurisdiction-specific privacy analysis. It does not assert that aggregation, redaction, pseudonymization, or anonymization is safe by default.

This doctrine also does not grant runtime authority to Ontogenesis. Ontogenesis defines semantic contracts. Consuming systems enforce them through their own policy, runtime, and receipt machinery.

## Claim boundary

`DoNotLearn` and `DoNotLink` are governance constraints, not empirical claims. They describe required system behavior and failure modes. Their effectiveness depends on downstream enforcement, validation, auditability, and receipt discipline.
