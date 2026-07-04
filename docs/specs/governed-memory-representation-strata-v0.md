# Governed Memory Representation Strata v0

Status: draft  
Authority plane: `SocioProphet/ontogenesis`  
Scope: semantic doctrine for separating evidence, claims, memory, embeddings, learned representations, policy, actions, and receipts across SocioProphet memory-bearing systems

## Purpose

This specification defines the first governed memory representation strata for the SocioProphet estate.

The goal is to prevent the word `memory` from collapsing distinct representation types into a single unsafe substrate. Raw evidence, source anchors, claims, graph facts, embeddings, latent representations, policy decisions, action proposals, runtime receipts, learning events, and teaching objects have different authority, lifecycle, privacy, and validation semantics.

This document is an authority-plane doctrine artifact. It does not yet add Turtle terms, SHACL gates, JSON-LD context terms, runtime code, or product behavior.

## Relationship to governed intelligence

This specification extends the governed-intelligence object model and the privacy non-linkability doctrine.

The governed-intelligence loop remains:

```text
Observe -> Anchor -> Normalize -> Propose -> Explain -> Verify -> Govern -> Act -> Receipt -> Learn
```

Memory-bearing systems must preserve the difference between objects in that loop. A vector candidate is not a claim. A claim is not a policy decision. A policy decision is not a runtime receipt. A runtime receipt is not permission to train. A learning event is not automatically legitimate under DoNotLearn.

## Core rule

No representation may silently climb the authority ladder.

A lower-authority representation can become input to a higher-authority representation only through an explicit promotion path with evidence, policy, lifecycle state, and receipt semantics.

## Strata

### S0 Raw signal

Raw signal is unnormalized input: user text, uploaded files, logs, sensor data, event streams, model outputs, audio, images, telemetry, command output, source artifacts, and external observations.

Raw signal is not evidence until anchored. Raw signal is not memory merely because it entered a system.

Primary risks: overcapture, silent retention, privacy leakage, unbounded reuse, source ambiguity.

Required controls: source scope, retention scope, privacy scope, ingestion receipt where effectful.

### S1 Anchor

An anchor is a selector into a source artifact: text span, image region, geometry, code range, log range, table cell, audio segment, video clip, or generic selector.

Anchors make raw signal referencable. They do not make it true, reusable, or learnable.

Primary risks: selector drift, source alias confusion, hidden identity leakage, overbroad source capture.

Required controls: artifact reference, selector type, selector, source reference, valid time where relevant.

### S2 Evidence

Evidence is source-backed support, opposition, qualification, or context for a claim or action.

Evidence can be admissible for one purpose while still being non-learnable or non-linkable for another. Evidence admission is not training permission.

Primary risks: source laundering, quote overreach, claim inflation, privacy-boundary bypass.

Required controls: anchor reference, provenance, evidence role, lifecycle status, valid scope.

### S3 Claim

A claim is a typed assertion over subject, predicate, object, context, evidence, uncertainty, and lifecycle state.

Claims may be proposed, provisional, admitted, denied, superseded, revoked, or expired. A proposed claim is not admitted truth.

Primary risks: candidate-to-claim laundering, unsupported assertion, stale truth, context loss.

Required controls: subject, predicate, object, context, evidence reference, lifecycle status, policy decision where admission matters.

### S4 Symbolic graph representation

A symbolic graph representation is a graph, ontology assertion, edge, equivalence relation, topic membership, or semantic relation derived from claims, evidence, or curated ontology terms.

Graph representation is not automatically higher truth. A graph edge must preserve evidence and lifecycle semantics.

Primary risks: illegitimate joins, entity-resolution overreach, graph-edge persistence after revocation, relation formation across privacy boundaries.

Required controls: provenance, claim binding, non-linkability check, lifecycle status, revocation path.

### S5 Statistical feature representation

A statistical feature representation is an aggregate, metric, score, feature vector, risk signal, distributional summary, calibration output, or analytic measurement derived from evidence or events.

Statistical features are not self-explaining claims. They require scope, construction method, evaluation context, and drift handling.

Primary risks: proxy leakage, quasi-identifier construction, false precision, scope mismatch, untracked drift.

Required controls: feature definition, source scope, construction method, evaluation scope, privacy boundary, drift or expiry plan.

### S6 Vector candidate representation

A vector candidate is an embedding, vector-symbolic recall result, nearest-neighbor result, cleanup-index result, or retrieval candidate.

Vector candidates remain candidate-only. Similarity is not evidence, truth, admission, identity, or link permission.

Primary risks: latent identity reconstruction, candidate-to-claim laundering, hidden cross-domain bridge, durable memory capture, similarity-as-truth error.

Required controls: candidate-only status, manifest reference, query/source scope, similarity semantics, privacy boundary, non-linkability check.

### S7 Learned latent representation

A learned latent representation is reusable learned state: model weights, adapters, memory summaries, durable embeddings, learned profiles, clustering state, policy-learning state, topic-pack state, or agent memory.

Learned latent representation is the most dangerous memory stratum because protected information can influence behavior even when original artifacts are not visible.

Primary risks: DoNotLearn violation, memorization, irreversible leakage, cross-context generalization, model or memory contamination.

Required controls: explicit learning admission, training or memory receipt, data scope, retention scope, privacy decision, removal or expiry plan where feasible.

### S8 Policy and governance representation

Policy representation includes policy decisions, action admissions, privacy decisions, doctrine, review gates, status vocabulary, lifecycle state, and authority surfaces.

Policy representation decides what may be admitted, denied, held for review, or provisionally used. It is not evidence by itself.

Primary risks: policy laundering, stale admission, missing authority, review bypass, unclear scope.

Required controls: target reference, decision, policy basis, authority surface, lifecycle state, receipt expectation.

### S9 Action representation

Action representation includes action proposals, tool grants, agent intents, expected effects, scopes, and admitted action plans.

An action proposal is not permission to act. Effectful work requires admission and a receipt.

Primary risks: unadmitted side effects, overbroad scope, tool misuse, policy bypass, missing expected-effect record.

Required controls: action type, scope, expected effect, evidence reference, policy decision, action admission.

### S10 Receipt representation

Receipt representation records what happened: runtime receipts, privacy receipts, learning receipts, policy receipts, model-governance receipts, ledger entries, and audit artifacts.

Receipts are evidence about execution or adoption. They do not automatically prove the underlying claim correct.

Primary risks: receipt-as-proof error, incomplete logs, unverified hashes, missing policy reference, orphaned receipts.

Required controls: action or operation reference, policy decision, input/output hashes, log reference, status, transaction time, verification path.

### S11 Teaching representation

Teaching representation includes workroom cards, Academy objects, examples, checklists, drills, operator notes, agent boot notes, and explanatory material derived from admitted doctrine or patterns.

Teaching objects are not authority unless linked to doctrine and evidence.

Primary risks: folk doctrine, outdated guidance, uncited lessons, oversimplification, claim-boundary loss.

Required controls: doctrine reference, evidence or pattern reference, audience, lifecycle state, reobservation trigger.

## Promotion rules

### Raw signal to anchor

Requires source reference, selector semantics, and retention/privacy scope.

### Anchor to evidence

Requires evidence role, provenance, and lifecycle status.

### Evidence to claim

Requires bounded assertion, context, evidence reference, and claim lifecycle status.

### Claim to graph relation

Requires claim binding, relation type, lifecycle status, and non-linkability review where a privacy boundary may be crossed.

### Evidence or event to statistical feature

Requires feature definition, construction method, source scope, and evaluation context.

### Signal, evidence, or feature to vector candidate

Requires vector encoding manifest, candidate-only status, and query/source scope.

### Any representation to learned latent representation

Requires explicit learning admission, DoNotLearn review, policy decision, and receipt.

### Any proposal to action

Requires action admission and runtime receipt.

### Any lesson to teaching object

Requires doctrine or pattern reference and claim boundary preservation.

## Default denials

Absent an explicit policy decision:

- vector similarity must not become an admitted claim;
- graph proximity must not become identity equivalence;
- evidence admission must not become learning permission;
- source citation must not become durable memory permission;
- action proposal must not become effectful work;
- learning event must not become model or memory update;
- teaching object must not become authority doctrine.

## Binding to DoNotLearn / DoNotLink

DoNotLearn primarily constrains movement into S7 learned latent representation.

DoNotLink primarily constrains movement into S4 symbolic graph representation, S6 vector candidate representation when exposed as a bridge, and any cross-context relation formation.

Both constraints may apply at once. A system can learn without linking, link without learning, or do both.

## Consumer responsibilities

| Consumer | Responsibility |
| --- | --- |
| `ontogenesis` | Defines canonical vocabulary, doctrine, shapes, contexts, and examples for representation strata. |
| `prophet-platform` | Applies the strata to workroom memory, topic packs, retrieval, user-facing memory behavior, and product UX. |
| `model-governance-ledger` | Records training, inference, evaluation, drift, privacy, and learning receipts. |
| `agentplane` | Enforces action proposal/admission/receipt boundaries for effectful operations. |
| `sherlock-search` | Preserves candidate-only semantics for retrieval and vector results. |
| `holmes` | Produces reasoning and explanation traces without independent admission authority. |
| `policy-fabric` / `guardrail-fabric` | Issues policy decisions over learning, linking, action, and admission. |
| `systems-learning-loops` | Converts lessons about memory failures into patterns, countermeasures, receipts, and teaching objects. |
| `sociosphere` | Tracks cross-repo adoption and estate-level stabilization of the doctrine. |

## Non-goals

This specification does not define runtime storage architecture, database schemas, vector-index implementation, model-training procedure, UI behavior, or legal privacy compliance. It does not assert that all strata are always present in every workflow.

This specification also does not claim that higher strata are more truthful. Higher strata are more governed, more reusable, or more effectful; truth still depends on evidence, verification, policy, and lifecycle status.

## First implementation path

1. Stabilize this doctrine document.
2. Add a lightweight ontology extension for representation strata.
3. Add JSON-LD context terms.
4. Add example fixtures showing valid and invalid promotion paths.
5. Add conservative SHACL gates for structural promotion fields only.
6. Coordinate downstream adoption with Prophet Platform memory/workroom surfaces.

## Claim boundary

Representation strata are governance semantics, not a storage implementation. They define how representations may be interpreted and promoted. Downstream systems remain responsible for enforcement, receipts, and runtime behavior.
