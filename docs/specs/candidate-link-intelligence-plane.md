# Candidate Link Intelligence Plane v0.1

Status: draft  
Owner: Ontogenesis  
Companion mapping: `docs/specs/candidate-link-to-shir.md`

## 1. Purpose

The Candidate Link Intelligence Plane defines how SocioProphet proposes, scores, explains, validates, and promotes candidate links across governed semantic graphs.

It covers binary links, n-ary links, hyperedges, schema alignments, entity linkages, relation completions, role-binding completions, and evidence-backed repair suggestions.

The central rule is:

> Predicted links are candidates, not facts.

A model may propose a relation. It may not promote that relation into canonical knowledge by itself.

## 2. Why this exists

The stack now has several semantic layers that must interoperate:

- Link Grammar parser output
- ACSET-backed parse state
- SHIR semantic hyperknowledge representation
- RDF / OWL / SHACL / JSON-LD ontology modules
- ValueFlows governed profiles
- ontology-query reasoning and SHACL evaluation
- semantic-enterprise lifecycle, mapping, named graph, and alignment modules
- downstream retrieval, memory, graph ML, rule, and agent execution systems

A single KG-BERT-style triple classifier is insufficient because our graph is not merely a set of binary triples. We need a governed candidate system that preserves:

- context
- evidence
- temporal scope
- policy scope
- n-ary connector roles
- projection loss
- scoring traces
- model provenance
- curation decisions
- replay receipts

## 3. Non-goals

This spec does not define a specific model runtime.

It does not mandate KG-BERT, NBFNet, ULTRA, NodePiece, HYPER, PyG, DGL, Neo4j, RDF-star, or any proprietary runtime.

It does not permit model output to bypass SHACL, ontology-query, policy, curation, or evidence gates.

It does not flatten SHIR into binary triples unless the projection declares what was lost.

## 4. Pipeline position

```text
Source graph / parser output / evidence / ontology modules
  -> candidate generation
  -> candidate scoring
  -> candidate explanation and counterexample search
  -> SHIR candidate representation
  -> policy / SHACL / ontology-query / curation gates
  -> promotion, rejection, quarantine, repair, or deferred review
```

## 5. Core object model

### 5.1 CandidateLink

A provisional binary link between subject and object under a candidate predicate.

Required fields:

- `candidateId`
- `subject`
- `predicate`
- `object`
- `candidateKind`
- `sourceContext`
- `evidenceBundle`
- `scoringTrace`
- `policyScope`
- `temporalScope`
- `status`

Allowed status values:

- `proposed`
- `scored`
- `quarantined`
- `needs-review`
- `rejected`
- `promoted`

### 5.2 CandidateHyperedge

A provisional n-ary relation represented by a connector and role bindings.

Required fields:

- `candidateId`
- `connector`
- `roleBindings`
- `context`
- `evidenceBundle`
- `scoringTrace`
- `policyScope`
- `temporalScope`
- `projectionLossReport` when lowered into a simpler representation
- `status`

### 5.3 CandidateRoleBinding

A proposed binding between a connector role and a node or evidence anchor.

Examples:

- `provider -> TopoLVM`
- `resource -> PersistentVolume`
- `target_context -> KubernetesNode`
- `authority_holder -> DelegatedAgent`

### 5.4 CandidateAlignment

A proposed mapping between classes, properties, schemas, table columns, API fields, event fields, ontology modules, or domain terms.

Evidence classes should be explicit:

- lexical evidence
- structural evidence
- instance-level evidence
- temporal evidence
- provenance evidence
- embedding evidence
- rule-derived evidence
- human-curated evidence

### 5.5 CandidateEvidenceBundle

Evidence supporting a candidate.

May include:

- RDF triples
- SHIR anchors
- document spans
- table cells
- log ranges
- parser links
- ACSET parse-state objects
- ValueFlows event fragments
- graph paths
- ontology-query reports
- SHACL reports
- retrieval snippets
- human annotations

### 5.6 PredictionTrace

A record of how a candidate was produced or scored.

Required fields:

- `traceId`
- `candidateId`
- `modelId` or `ruleId`
- `modelFamily`
- `modelVersion`
- `inputArtifactRefs`
- `featureRefs`
- `score`
- `calibratedConfidence`
- `thresholdProfile`
- `negativeSamplingPolicy` where applicable
- `createdAt`

### 5.7 ScoringModel

A description of a scoring engine.

Model families may include:

- symbolic rule scorer
- SHACL/domain-range scorer
- ontology-query/reasoner scorer
- embedding scorer
- path reasoning scorer
- KG-BERT-style text cross-encoder
- graph neural network scorer
- hypergraph scorer
- LLM-assisted explanation scorer

### 5.8 NegativeSamplePolicy

A declared policy for constructing negative examples during training or evaluation.

It must distinguish:

- closed-world negative
- open-world unknown
- type-constrained corruption
- relation-constrained corruption
- temporal invalid negative
- policy-invalid negative
- evidence-missing negative

### 5.9 Counterexample

A structured objection to a candidate.

Counterexamples may come from:

- SHACL violation
- ontology-query contradiction
- disjointness or domain/range mismatch
- temporal contradiction
- source trust conflict
- policy violation
- evidence mismatch
- human review

### 5.10 CurationDecision

A decision made by a human, policy engine, agent, rule, or review workflow.

Allowed decision values:

- `promote`
- `reject`
- `quarantine`
- `request-evidence`
- `request-human-review`
- `repair`
- `merge`
- `split`
- `rescope`
- `defer`

### 5.11 CandidateReceipt

A reproducibility record for candidate generation, scoring, curation, projection, or promotion.

Required fields:

- source graph hash
- ontology profile
- policy profile
- model identity
- scorer identity
- feature manifest hash
- candidate output hash
- random seed where applicable
- curation decision reference
- projection-loss report reference where applicable

## 6. Candidate generation strategies

The candidate plane supports several generation strategies. These should be treated as complementary, not mutually exclusive.

### 6.1 Ontology-constrained generation

Generate candidates from:

- domain/range constraints
- SHACL shape targets
- class hierarchy
- equivalent-class/property hints
- inverse property hints
- part-whole constraints
- lifecycle state transitions

### 6.2 Path and motif expansion

Generate candidates from:

- graph paths
- typed metapaths
- neighborhood overlap
- relation motifs
- transitive closure candidates
- missing inverse candidates
- role-completion candidates

### 6.3 Parser-derived generation

Generate candidates from:

- Link Grammar links
- ACSET parse objects
- relation phrase patterns
- syntactic modifiers
- appositions
- possession / ownership patterns
- temporal qualifiers
- agent-action-object structures

### 6.4 Evidence retrieval generation

Generate candidates from:

- document spans
- tables
- logs
- examples
- code references
- annotations
- prior receipts

### 6.5 Model-assisted generation

Generate candidates from:

- embedding nearest neighbors
- graph neural prediction
- KG text cross-encoders
- hypergraph role completion
- LLM-assisted schema mapping suggestions

## 7. Scoring portfolio

World-class candidate scoring should use a portfolio, not one model.

### 7.1 Cheap structural baselines

Use fast KGE-style baselines for early scoring and ablation:

- TransE-like translational scoring
- DistMult-like bilinear scoring
- ComplEx-like complex-valued scoring
- RotatE-like relation rotation scoring

These are useful, but they are insufficient for governed promotion.

### 7.2 Path reasoning scorer

Use path/subgraph reasoning for multi-hop evidence.

This scorer should produce:

- supporting paths
- path weights
- path confidence
- path-to-evidence references

### 7.3 Textual cross-encoder scorer

KG-BERT-style scoring is appropriate when candidate entities and relations have useful natural-language descriptions.

It should score structured text such as:

```text
subject description [SEP] relation description [SEP] object description [SEP] evidence text
```

It should not be the sole gate.

### 7.4 Inductive graph scorer

Use an inductive scorer for unseen entities, newly added modules, and evolving vocabularies.

The scorer must record whether a prediction is:

- transductive
- inductive over entities
- inductive over relations
- inductive over both

### 7.5 Hypergraph scorer

Use hypergraph and n-ary role-completion scorers for SHIR connector structures.

This is mandatory for candidate structures that cannot be faithfully represented as one binary triple.

### 7.6 Symbolic validation scorer

Use SHACL, ontology-query, and policy checks as hard or weighted validation signals.

Symbolic checks should produce counterexamples, not just booleans.

### 7.7 LLM-assisted explanation scorer

LLMs may propose explanations, counterexamples, repair actions, and mapping rationales.

LLMs may not promote candidates directly.

## 8. Evaluation metrics

Link prediction evaluation must include governance metrics, not only ranking metrics.

### 8.1 Ranking metrics

- MRR
- Hits@1
- Hits@3
- Hits@10
- mean rank
- filtered MRR when appropriate

### 8.2 Calibration metrics

- expected calibration error
- Brier score
- confidence bucket accuracy

### 8.3 Governance metrics

- evidence coverage
- policy-invalid rate
- SHACL violation rate
- ontology-query contradiction rate
- temporal leakage rate
- projection-loss rate
- unreviewed promotion rate

### 8.4 Operational metrics

- candidate throughput
- scoring latency
- curation queue pressure
- promotion acceptance rate
- false promotion incident rate
- rollback rate

## 9. Promotion gates

A candidate may be promoted only if:

1. it has at least one evidence bundle
2. it has a scoring trace
3. it has a policy scope
4. it has temporal scope where temporal claims are involved
5. SHACL constraints pass or violations are explicitly waived
6. ontology-query does not find disqualifying contradiction
7. projection-loss is acceptable for the target representation
8. curation decision permits promotion
9. a receipt is emitted

## 10. Repo ownership boundaries

Ontogenesis owns:

- this semantic contract
- ontology vocabulary
- SHACL gate expectations
- SHIR mapping expectations
- candidate/promotion policy semantics

Semantic-serdes owns:

- machine-readable schemas
- SHIR projection manifests
- candidate fixtures
- projection-loss report schemas
- receipt schemas

Prophet-platform-fabric-mlops-ts-suite owns:

- model packs
- training jobs
- evaluation jobs
- leakage diagnostics
- scorer receipts

Agentplane owns:

- orchestration of candidate generation, scoring, validation, curation, and promotion jobs

Policy-fabric owns:

- consent, PII, export, training eligibility, and exposure gates

Memory-mesh / Sherlock / Holmes own:

- retrieval evidence
- search surfaces
- graph-neighborhood evidence
- explanation traces
- memory capsule persistence

## 11. Acceptance criteria for v0.1

- Candidate outputs are represented as candidates, not facts.
- Binary and n-ary candidates are both supported.
- SHIR mapping is explicit.
- Evidence bundles are required.
- Prediction traces are required.
- Policy and temporal scopes are first-class.
- Promotion requires a curation decision and receipt.
- Model families are pluggable.
- KG-BERT-style scoring is included as one scorer, not the architecture.

