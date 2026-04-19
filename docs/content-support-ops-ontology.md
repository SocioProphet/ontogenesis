# Content, Support, Query, and Ops Ontology Design

## Purpose

This document defines the ontology-design tranche for governed content assets, support and premium-support interactions, query orchestration, learning loops, and operations-domain intelligence.

`ontogenesis` is the canonical semantic source of truth for these concepts. Runtime contracts, storage contracts, and execution systems consume these classes, but do not redefine their meaning.

## Design objective

The platform should not treat content, support, logs, anomalies, metering, learning, and memory as disconnected features.

They are one governed semantic system.

This ontology tranche formalizes the object model needed for:

- reusable content and template composition
- support and premium-support workflows
- query orchestration through `sherlock-search`
- operations-domain intelligence from `global-devsecops-intelligence`
- long-horizon retained memory in `memory-mesh`
- pedagogic and learning-objective loops in `alexandrian-academy`
- bounded execution and replay through `agentplane`
- runtime query, preview, and evaluation surfaces in `prophet-platform`

## Canonical semantic classes

### Asset and composition layer

- `sp:Asset`
- `sp:TemplateSpec`
- `sp:CompositionSpec`
- `sp:RouteSurface`
- `sp:PolicyBundle`
- `sp:PromotionDecision`
- `sp:EvidenceReceipt`

### Support layer

- `sp:SupportInteraction`
- `sp:SupportTier`
- `sp:SupportDomain`
- `sp:SupportCategory`
- `sp:TaskContext`
- `sp:AssetUsageRecord`
- `sp:SupportComment`
- `sp:SupportRecommendation`
- `sp:EscalationDecision`
- `sp:PremiumOverlay`
- `sp:ResolutionOutcome`

### Query layer

- `sp:QueryRequest`
- `sp:QueryPlan`
- `sp:QueryResultSet`
- `sp:ActionSuggestion`
- `sp:EscalationPacket`

### Learning and memory layer

- `sp:LearningObjective`
- `sp:CurriculumObject`
- `sp:MemoryRecord`
- `sp:Observation`
- `sp:ImprovementProposal`
- `sp:Experiment`

### Operations-domain intelligence layer

- `sp:LogEvent`
- `sp:TelemetryEvent`
- `sp:TicketEvent`
- `sp:ChatOpsEvent`
- `sp:AnomalyFinding`
- `sp:IncidentStory`
- `sp:MeterRecord`
- `sp:ServiceHealthObservation`
- `sp:OpsRecommendation`
- `sp:OpsEvidenceArtifact`
- `sp:SupportOpsContext`

## Core relationships

### Asset and composition

- `sp:Asset sp:bindsInto sp:TemplateSpec`
- `sp:CompositionSpec sp:projectsTo sp:RouteSurface`
- `sp:CompositionSpec sp:governedBy sp:PolicyBundle`
- `sp:PromotionDecision sp:approves sp:CompositionSpec`
- `sp:EvidenceReceipt sp:proves sp:PromotionDecision`

### Support

- `sp:SupportInteraction sp:hasTier sp:SupportTier`
- `sp:SupportInteraction sp:resolvedByDomain sp:SupportDomain`
- `sp:SupportInteraction sp:resolvedByCategory sp:SupportCategory`
- `sp:SupportInteraction sp:usesAsset sp:Asset`
- `sp:SupportInteraction sp:hasTaskContext sp:TaskContext`
- `sp:SupportInteraction sp:producesComment sp:SupportComment`
- `sp:SupportInteraction sp:producesRecommendation sp:SupportRecommendation`
- `sp:SupportInteraction sp:mayEscalateVia sp:EscalationDecision`
- `sp:SupportTier sp:mayUseOverlay sp:PremiumOverlay`

### Query

- `sp:QueryRequest sp:targetsSemanticClass iri`
- `sp:QueryPlan sp:plansFor sp:QueryRequest`
- `sp:QueryResultSet sp:answers sp:QueryRequest`
- `sp:ActionSuggestion sp:suggestedFor sp:QueryResultSet`
- `sp:EscalationPacket sp:derivedFrom sp:QueryResultSet`

### Learning and memory

- `sp:LearningObjective sp:appliesTo sp:Asset`
- `sp:LearningObjective sp:appliesTo sp:SupportInteraction`
- `sp:CurriculumObject sp:supportsObjective sp:LearningObjective`
- `sp:Observation sp:observes sp:Asset`
- `sp:Observation sp:observes sp:SupportInteraction`
- `sp:MemoryRecord sp:retainsContextFor sp:SupportInteraction`
- `sp:ImprovementProposal sp:derivedFrom sp:Observation`
- `sp:Experiment sp:evaluates sp:ImprovementProposal`

### Operations-domain intelligence

- `sp:LogEvent sp:groupedInto sp:IncidentStory`
- `sp:TelemetryEvent sp:groupedInto sp:IncidentStory`
- `sp:TicketEvent sp:groupedInto sp:IncidentStory`
- `sp:ChatOpsEvent sp:groupedInto sp:IncidentStory`
- `sp:AnomalyFinding sp:scopedTo sp:IncidentStory`
- `sp:MeterRecord sp:measures sp:SupportInteraction`
- `sp:MeterRecord sp:measures sp:AssetUsageRecord`
- `sp:OpsRecommendation sp:derivedFrom sp:AnomalyFinding`
- `sp:OpsEvidenceArtifact sp:proves sp:IncidentStory`
- `sp:SupportOpsContext sp:attachesTo sp:SupportInteraction`

## Tier semantics

### Standard support

Standard support uses shared canonical assets, standard memory scopes, generic operational intelligence views, and bounded recommendation rights.

### Premium support

Premium support is not a different ontology. It is the same ontology with narrower entitlement and overlay rules.

`sp:PremiumOverlay` should support:

- tenant or customer-specific assets
- customer-specific memory scopes
- premium anomaly thresholds and service groupings
- custom runbooks and handoff rules
- stricter or broader recommendation rights depending on policy

### Mission-critical / sovereign support

This tier adds stronger disclosure boundaries, narrower data scopes, more required evidence, and stronger human-review requirements at recommendation and promotion boundaries.

## Learning-loop semantics

The system uses three distinct but connected learning loops.

### Alexandrian Academy loop
Defines normative learning quality, pedagogy-aware explanation, and curriculum-backed support and education objects.

### Memory Mesh loop
Defines retained memory, recall-before-change, prior-case linkage, decision history, and writeback-after-outcome.

### Meshrush loop
Defines short-horizon adaptation pressure, fresh observation clustering, rapid drift detection, and immediate improvement proposal pressure.

## Query semantics

The canonical query plane must be able to bind to these classes without redefining them.

Sherlock should query over:

- asset and template classes
- support interaction history
- memory records
- curriculum objects
- operational stories, anomalies, and metering
- evidence artifacts and promotion decisions

## SHACL / gate implications

The SHACL layer should eventually enforce at least:

1. `sp:SupportInteraction` must resolve to exactly one support tier.
2. `sp:SupportRecommendation` must carry rationale and policy eligibility references.
3. `sp:AnomalyFinding` must link to evidence lineage.
4. `sp:QueryResultSet` must support provenance and citation handles.
5. `sp:PremiumOverlay` must not be applied without explicit entitlement linkage.
6. `sp:PromotionDecision` must carry replay/evidence references when moving a composition or support asset to a more trusted state.

## Immediate next steps

1. Add the corresponding machine-readable ontology modules under the layered ontology structure.
2. Add SHACL bundles for support, query, and ops-domain validity gates.
3. Align runtime and transport contracts in downstream standards and platform repos.
4. Bind Sherlock, support loops, AI4IT ops intelligence, memory, and Academy learning objects to these semantic classes.
