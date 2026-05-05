# Candidate Link to SHIR Mapping v0.1

Status: draft  
Owner: Ontogenesis  
Depends on: `docs/specs/candidate-link-intelligence-plane.md`, `docs/specs/shir-v0.1.md`

## 1. Purpose

This document defines how predicted candidate links are represented in SHIR before any canonical ontology or graph promotion.

Candidate links may be binary triples, n-ary relations, hyperedges, schema alignments, entity linkages, role-binding completions, or repair suggestions.

The mapping rule is:

> Every model-generated relation proposal must become a SHIR candidate object with evidence, policy, temporal scope, scoring trace, and receipt metadata before promotion.

## 2. Mapping summary

| Candidate Link object | SHIR target |
|---|---|
| `CandidateLink` | `shir:CandidateAssertion` plus binary `shir:Link` profile |
| `CandidateHyperedge` | `shir:Connector` plus `shir:RoleBinding` plus `shir:Link` |
| `CandidateRoleBinding` | `shir:RoleBinding` candidate attached to a connector |
| `CandidateAlignment` | `shir:SchemaAlignmentCandidate` or `shir:LinkageCandidate` |
| `CandidateEvidenceBundle` | `shir:Evidence` plus `shir:Anchor` references |
| `PredictionTrace` | `shir:InductionTrace` |
| `Counterexample` | `shir:NoiseAssessment` and optional `shir:RepairAction` |
| `CurationDecision` | `shir:CurationDecision` |
| `CandidateReceipt` | `shir:Receipt` |
| `ProjectionLossReport` | `shir:ProjectionLossReport` |

## 3. Binary candidate link mapping

A binary candidate link such as:

```json
{
  "candidateId": "cand-link-001",
  "subject": "TopoLVM",
  "predicate": "provisions",
  "object": "PersistentVolume",
  "score": 0.82
}
```

maps to:

- `shir:CandidateAssertion`
- one `shir:Link`
- connector profile with subject and object roles
- `shir:Evidence` references
- `shir:InductionTrace` from the scorer
- `shir:PolicyScope`
- `shir:TemporalScope` where applicable
- `shir:Receipt`

The candidate is not a canonical assertion until promotion gates pass.

## 4. Hyperedge / n-ary candidate mapping

A candidate hyperedge is represented as a connector-backed SHIR link.

Example source candidate:

```text
provisions(provider=TopoLVM, resource=PersistentVolume, target_context=KubernetesNode)
```

SHIR mapping:

- `shir:Connector` = `provisions`
- role bindings:
  - `provider -> TopoLVM`
  - `resource -> PersistentVolume`
  - `target_context -> KubernetesNode`
- `shir:Link` references the connector and role bindings
- evidence anchors support the role bindings and the full link

If this is later lowered into binary RDF triples, the projection must emit a `shir:ProjectionLossReport` describing whether the n-ary structure was reified, approximated, split, or partially lost.

## 5. Schema alignment candidate mapping

A schema alignment candidate maps to `shir:SchemaAlignmentCandidate` when the proposal relates schema elements.

Examples:

- class-to-class mapping
- property-to-property mapping
- JSON field to RDF property mapping
- API field to ontology property mapping
- table column to ontology property mapping

Required SHIR fields:

- source schema element
- target schema element
- mapping type
- evidence bundle
- induction trace
- confidence
- human review requirement
- curation status

## 6. Entity linkage candidate mapping

An entity linkage candidate maps to `shir:LinkageCandidate` when the proposal concerns identity, overlap, equivalence, containment, joinability, or semantic overlap.

Allowed linkage types:

- `same-as`
- `close-match`
- `related-match`
- `subsumes`
- `part-of`
- `joinable-with`
- `overlaps-with`
- `conflicts-with`

Identity promotion must require stricter evidence and review than loose relatedness.

## 7. Evidence bundle mapping

Each `CandidateEvidenceBundle` maps to one or more `shir:Evidence` objects.

Evidence should preserve anchors wherever possible:

- document span
- PDF page region
- table cell or range
- log event range
- source graph triple set
- named graph
- parser linkage
- ACSET parse object
- ValueFlows event
- retrieval result
- human annotation

Candidate promotion must fail or defer when evidence cannot be anchored.

## 8. Prediction trace mapping

Each scoring trace maps to `shir:InductionTrace`.

Required fields:

- trace id
- candidate id
- model or rule id
- model family
- model version
- feature manifest
- source artifact references
- score
- calibrated confidence
- threshold profile
- negative sampling policy where applicable
- created timestamp

Multiple scorers may attach multiple induction traces to one candidate.

## 9. Counterexample mapping

Counterexamples map to `shir:NoiseAssessment` and optionally to `shir:RepairAction`.

Examples:

- SHACL violation -> `NoiseAssessment(policy-invalid fact)`
- temporal contradiction -> `NoiseAssessment(temporal leakage)`
- disjoint class mismatch -> `NoiseAssessment(wrong type)`
- unsupported assertion -> `NoiseAssessment(unsupported assertion)`
- likely hallucination -> `NoiseAssessment(hallucinated assertion)`

Repair actions may include:

- quarantine
- request evidence
- re-scope
- re-type
- split
- merge
- reject
- human review

## 10. Promotion mapping

A promoted candidate becomes a canonical assertion only after a `shir:CurationDecision` permits promotion and a `shir:Receipt` records the transformation.

Promotion output must preserve backreferences to:

- original candidate id
- evidence bundle
- induction trace
- policy scope
- temporal scope
- curation decision
- projection-loss report when applicable
- receipt

## 11. Parser-specific mapping

Parser-derived candidate links follow this path:

```text
Link Grammar parse
  -> ACSET parse state
  -> CandidateLink / CandidateHyperedge
  -> SHIR CandidateAssertion / LinkageCandidate / SchemaAlignmentCandidate
  -> curation and promotion gates
```

The mapping must preserve:

- token offsets
- linkage id
- parse alternative id
- connector labels
- parse score or cost
- ambiguity class
- evidence anchors back to source text

## 12. ValueFlows-specific mapping

ValueFlows candidate links and event-log projections should use the existing ValueFlows to SHIR projection manifest.

Recommended mapping:

- process run -> `shir:Context`
- task -> `shir:Node` and/or `shir:Assertion`
- delegated authority -> `shir:PolicyScope`
- capability grant -> `shir:PolicyScope`
- event checkpoint -> `shir:Evidence`
- replay receipt -> `shir:Receipt`
- terminal/canceled/revoked states -> temporal/policy scoped assertions

## 13. Validation expectations

A candidate-to-SHIR implementation should validate:

- candidate id is stable
- evidence anchors exist
- scoring trace exists
- policy scope exists
- temporal scope exists when needed
- connector role bindings are complete
- projection-loss report exists for lossy lowering
- receipt exists for promotion or projection
- promoted assertions retain candidate backreferences

## 14. Ownership boundaries

Ontogenesis owns this mapping contract.

Semantic-serdes should implement machine-readable schemas, fixtures, and projection validators.

Agentplane should orchestrate candidate generation, scoring, validation, and promotion workflows.

Policy-fabric should evaluate consent, PII, export, training, and exposure gates.

Memory-mesh / Sherlock / Holmes should provide retrieval evidence, explanation traces, and memory/search integration.

## 15. Acceptance criteria for v0.1

- Binary links map to SHIR candidate assertions.
- N-ary relations map to SHIR connectors and role bindings.
- Schema alignments map to schema alignment candidates.
- Entity linkage proposals map to linkage candidates.
- Evidence bundles map to evidence and anchors.
- Prediction traces map to induction traces.
- Counterexamples map to noise assessments and repair actions.
- Promotion requires curation and receipts.
- No candidate bypasses SHIR before promotion.
