# Rregis / ACR Ontogenesis Alignment
Version: v0.1
Status: draft spec-anchor

## Purpose

This specification aligns Ontogenesis with Rregis Entity Graph / Authority Concordance Rex (ACR), Gaia World Model, Prophet Platform, SourceOS, AgentPlane, TriRPC, and the broader SocioProphet estate.

Ontogenesis is the lifecycle semantics plane: it describes how entities, relationships, roles, policies, value flows, governance acts, and evidence-backed projections come into existence, change state, acquire validity, become disputed, merge, split, retire, or revive.

## Repository fit

This belongs in `SocioProphet/ontogenesis` because this repository is already the auditable, policy-gated ontology engineering framework for RDF, OWL, and JSON-LD assets across the SocioProphet stack. It already supports ontology creation, linking, validation, lifecycle governance, SHACL promotion gates, module registry metadata, dist generation, ledger verification, and SBOM generation.

## Core thesis

Rregis / ACR tells us what an entity is and why we believe it. Ontogenesis tells us how that entity, its relationships, and its authority-bearing state became valid over time.

The durable integration surface is:

- identity and evidence in Rregis / ACR
- lifecycle semantics in Ontogenesis
- civic and ecological meaning in Gaia
- local sovereign custody in SourceOS
- policy simulation and review in Prophet
- proof-carrying capability flow in AgentPlane / TriRPC

## Required ontogenic primitives

### GenesisEvent
A typed event that brings an entity, role, relationship, policy, value flow, consent, delegation, or governance state into recognized existence.

### LifecycleState
The current or historical state of an object, including active, proposed, pending review, superseded, merged, split, disputed, revoked, retired, or revived.

### ValidityInterval
Temporal scope for an assertion, role, relationship, identifier, consent, delegation, policy, or value-flow state.

### DerivationPath
The provenance path by which an object or relationship came to be recognized, including source records, evidence claims, policy decisions, ledger entries, and proof artifacts.

### EntityFormationRecord
The formation story for a canonical entity, including source records, concordance links, evidence claims, resolver decisions, human stewardship, and imported-authority assertions.

### RelationshipFormationRecord
The formation story for an entity-to-entity relationship, including relationship type, evidence, validity interval, policy basis, and dispute state.

### ValueFlowEvent
A governed event representing offers, intents, proposals, commitments, claims, receipts, fulfillments, resource movements, obligations, and dispute/reopen transitions.

### GovernanceAct
A decision, consent, vote, delegation, override, appeal, revocation, stewardship action, or public-interest policy act.

### ParticipationRole
A lifecycle-bounded role held by a citizen, steward, delegate, agent, institution, cooperative, maintainer, reviewer, issuer, controller, processor, or beneficiary.

### OntogenicRule
A policy or invariant controlling legal state transitions.

## Alignment with ACR contracts

ACR owns the entity/evidence backbone:

- CanonicalEntity
- SourceRecord
- ConcordanceLink
- EvidenceClaim
- DecisionLedgerEntry
- EnergyLedgerEntry
- PromotionPolicy

Ontogenesis adds formation and transition semantics:

- GenesisEvent
- LifecycleState
- ValidityInterval
- DerivationPath
- EntityFormationRecord
- RelationshipFormationRecord
- ValueFlowEvent
- GovernanceAct
- ParticipationRole
- OntogenicRule

## Invariants

### Formation invariant
No canonical object should appear without either a GenesisEvent, an imported-authority assertion, or a replayable derivation path from source evidence.

### Temporal invariant
Every mutable role, relationship, consent, delegation, and value flow must carry validity semantics.

### Replay invariant
Ontogenic transitions must be replayable under the policy version that produced them.

### Sovereign-local invariant
Citizen-local ontogenic state cannot be overwritten by a cloud projection without SyncIntent plus consent or an explicit lawful/public-interest policy artifact.

### Reversibility invariant
Merge, split, appeal, revocation, and dispute transitions must preserve prior state and derivation paths.

### Proof-binding invariant
High-stakes lifecycle transitions should be able to bind to ProofArtifact records.

## ValueFlows binding

The governed ValueFlows profile already defines a canonical object set including Actor, Group, Role, Membership, ProcessRun, Task, Commitment, Delegation, CapabilityGrant, PolicyDecision, EvidencePack, and CairnCheckpoint.

This alignment extends that lane by treating governed ValueFlow events as ontogenic transitions. ValueFlow commitments, grants, claims, receipts, and fulfillments are not merely records; they are lifecycle-changing acts.

Minimum event bindings:

- `processrun.created.v1` becomes a GenesisEvent for a process run.
- `delegation.issued.v1` becomes a GovernanceAct plus Delegation lifecycle transition.
- `capabilitygrant.issued.v1` becomes a GovernanceAct plus capability lifecycle transition.
- `task.offered.v1` becomes a ValueFlowEvent.
- `commitment.accepted.v1` becomes a binding lifecycle transition.
- `task.completed.v1` becomes a fulfillment transition.
- `checkpoint.created.v1` becomes a replay boundary.

## Gaia binding

Gaia provides civic and ecological semantics: citizens, commons, jurisdictions, public services, institutions, places, resources, participation, and consent.

Ontogenesis describes how those Gaia objects become valid, change state, and participate in governance.

Examples:

- a community garden becomes a recognized commons
- a citizen delegates authority to a cooperative
- a public-service boundary changes jurisdiction
- a governance act creates a participation role
- a receipt closes a value-flow obligation
- a dispute reopens a completed flow

## SourceOS binding

SourceOS owns sovereign local-first runtime state.

A local node must be able to store and replay:

- GenesisEvent records
- ConsentReceipt formation and revocation
- DelegationGrant lifecycle
- SyncIntent lifecycle
- ParticipationRole lifecycle
- local ValueFlowEvent receipts
- local GovernanceAct records
- local ProofArtifact links

Cloud replication may mirror or coordinate this state, but must not become the root of citizen ontogenic validity.

## Prophet binding

Prophet consumes ontogenic transitions for policy simulation, scenario planning, governance workflows, appeals, and review queues.

Prophet should be able to ask:

- which lifecycle states are reachable from here?
- which governance acts can alter this state?
- which obligations remain unsatisfied?
- which claims are disputed or appealable?
- which futures preserve citizen sovereignty constraints?

## AgentPlane / TriRPC binding

Agents operate over lifecycle-bounded capabilities, not ambient access.

A proof-carrying request should reference:

- capability grant
- purpose
- consent or policy basis
- validity interval
- originating governance act
- proof artifact where required

## Minimal implementation tranche

1. Add Ontogenesis lifecycle contracts for GenesisEvent, LifecycleState, ValidityInterval, DerivationPath, GovernanceAct, and ValueFlowEvent.
2. Add SHACL shapes for formation, temporal validity, replay metadata, and authority-bound transitions.
3. Add JSON-LD examples for consent genesis, cooperative membership formation, value-flow fulfillment, entity merge with formation history, and appeal reopening a governance decision.
4. Add a ledger fixture proving deterministic replay of at least one governed value-flow sequence.
5. Add documentation index references from `docs/README.md`.

## Maximal implementation tranche

1. Add a lifecycle transition engine.
2. Add ValueFlows-compatible adapters.
3. Add Gaia ontology bindings for commons, participation, jurisdiction, and public-service objects.
4. Add Prophet policy simulation over lifecycle transitions.
5. Add SourceOS local replay/export of citizen ontogenic records.
6. Add proof-carrying ontogenic transitions for agent-mediated governance.

## Acceptance criteria

- Every lifecycle object has a schema or SHACL shape.
- Every high-stakes transition has an example fixture.
- Every example fixture validates locally.
- Every replayable transition carries policy version and derivation path.
- Every citizen-impacting transition supports review, appeal, or revocation semantics where applicable.
