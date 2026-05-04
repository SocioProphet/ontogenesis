# SHIR v0.1 — Semantic Hyperknowledge Intermediate Representation

Status: draft
Owner: Ontogenesis
Tracking issue: <https://github.com/SocioProphet/ontogenesis/issues/26>

## 1. Purpose

SHIR is the Semantic Hyperknowledge Intermediate Representation for the SocioProphet semantic stack.

Its purpose is to preserve semantic context before downstream projection into RDF, property graphs, graph machine learning datasets, vector indexes, retrieval corpora, rule engines, and agent memory artifacts.

SHIR exists because direct RDF-to-tensor conversion is too lossy for governed neuro-symbolic systems. RDF triples are strong for exchange, identity, ontology, and linked data, but they do not natively preserve all of the operational context required for n-ary relations, temporal validity, evidence anchors, policy scopes, induction traces, curation decisions, projection loss, or reproducible model training receipts.

The design is informed by public prior art in IBM Hyperknowledge, RDF-to-Hyperknowledge conversion, AutoRDF2GML-style RDF-to-graph-ML lowering, knowledge graph induction, semantic data curation, ontology lifecycle governance, and conceptual diagnostics. SHIR treats those as prior art and compatibility references, not mandatory runtime dependencies.

## 2. Position in the stack

SHIR is the middle contract between semantic authority and computational projection.

```text
RDF / OWL / SHACL / PROV / JSON-LD / TriG / RDF-star-style metadata / raw evidence
  -> knowledge induction and validation
  -> SHIR semantic hyperknowledge graph
  -> projection planner
  -> RDF, HK-compatible JSON, PyG, DGL, property graph, vector index, feature table,
     GraphRAG corpus, hypergraph tensor, PSL/ProbLog facts, or agent memory capsule
```

The authority remains the governed semantic source and ontology profile. Downstream tensors, vectors, feature tables, and retrieval stores are derived artifacts.

## 3. Design principles

1. Never flatten before the task requires flattening.
2. Preserve n-ary and higher-order relations through connectors and role bindings.
3. Preserve evidence anchors, provenance, validity, authority, and policy scope through every transformation.
4. Treat induced claims as candidates until validated, curated, or promoted by policy.
5. Separate valid time from observation or transaction time.
6. Report projection loss whenever SHIR is lowered into a simpler representation.
7. Detect semantic leakage before graph machine learning export.
8. Keep every transform replayable and receipt-bearing.
9. Support round-trip mappings where possible, and explicitly declare loss where round-trip preservation is impossible.
10. Keep SHIR compatible with open semantic-web practice while remaining independent from proprietary runtimes.

## 4. Core object model

### 4.1 `shir:Node`

A semantic object. A node may represent an entity, literal/value object, artifact, context, policy object, event, model, assertion object, relation node, or projection artifact.

Minimum fields:

- stable identifier
- type or class reference
- label or preferred display name when available
- provenance reference
- truth class when asserted as knowledge
- governance status

### 4.2 `shir:Anchor`

An addressable fragment of a node or artifact.

Examples:

- document span
- PDF page region
- table cell or column range
- image region
- video interval or frame range
- audio interval
- code file range
- log event range
- full-resource anchor

Anchors are required when an induced assertion depends on non-graph evidence.

### 4.3 `shir:Connector`

A relation schema with named roles and constraints. Connectors support binary, n-ary, higher-order, contextual, and recursive relations.

Examples:

- `provisions(provider, resource, target_context)`
- `employment(employee, employer, role, contract, valid_interval)`
- `cites(source_artifact, cited_artifact, evidence_anchor)`
- `derived_from(output, input, transform, receipt)`

### 4.4 `shir:RoleBinding`

A binding from a connector role to a node or anchor.

Role bindings prevent n-ary relations from being collapsed into ambiguous binary edges.

### 4.5 `shir:Link`

A relation instance. A link references a connector and contains role bindings, context, evidence, temporal scope, policy scope, and receipt metadata.

### 4.6 `shir:Context`

A recursive semantic scope.

A context may encode:

- graph name
- source corpus
- workspace
- domain
- trust plane
- policy domain
- temporal window
- scenario
- replay snapshot
- curation session

Contexts are first-class nodes so that context can be nested, linked, audited, and projected.

### 4.7 `shir:Assertion`

A governed claim. Assertions include truth class, confidence, evidence, authority, derivation, validity, policy scope, and curation status.

Assertions may be promoted from candidate assertions after validation and curation.

### 4.8 `shir:Evidence`

A source object supporting a candidate or promoted assertion.

Evidence may include graph triples, document anchors, table cells, logs, user annotations, model outputs, external references, or replay artifacts.

### 4.9 `shir:TemporalScope`

A bitemporal scope separating:

- valid time: when the fact is true in the modeled world
- observation or transaction time: when the system observed, ingested, asserted, changed, or retracted the fact

### 4.10 `shir:PolicyScope`

A policy envelope describing consent, PII, export eligibility, training eligibility, exposure constraints, retention, redaction, and publication controls.

### 4.11 `shir:Projection`

A declared lowering from SHIR into another representation.

Supported target families include:

- RDF / OWL / JSON-LD / TriG
- HK-compatible JSON
- property graph
- PyG / DGL heterogeneous graph manifests
- feature tables
- vector indexes
- GraphRAG corpora
- symbolic rule facts
- hypergraph tensors
- agent memory capsules

### 4.12 `shir:Receipt`

A reproducibility and governance record for a transform, validation, curation decision, projection, training step, or publication step.

Receipts should include source hashes, ontology profile, compiler version, transform code identity, model identity, policy decision, projection loss, random seed where relevant, and output artifact hash.

## 5. Induction and curation object model

### 5.1 `shir:CandidateAssertion`

An extracted or proposed claim before semantic promotion.

Candidate assertions must carry evidence, induction trace, confidence, extractor identity, and curation status.

### 5.2 `shir:InductionTrace`

Lineage for generated knowledge. Records extractor, model, prompt or rule version where applicable, source artifact, run ID, timestamp, and evidence anchors.

### 5.3 `shir:OntologyInfluence`

A reused ontology, standard, glossary, linked-open-data source, domain document, or expert input that influenced a class, property, shape, or rule.

### 5.4 `shir:LinkageCandidate`

A proposed identity, join, union, subset, crosswalk, or semantic-overlap relation between entities, tables, columns, schemas, APIs, artifacts, or classes.

The candidate must separate evidence types: lexical, structural, instance-level, temporal, provenance, embedding, rule-derived, and human-curated evidence.

### 5.5 `shir:SchemaAlignmentCandidate`

A proposed mapping between classes, properties, table columns, JSON fields, API fields, or event fields.

It may include active-learning state and required human review status.

### 5.6 `shir:NoiseAssessment`

A structured diagnosis of possible knowledge-graph noise.

Recommended noise classes:

- wrong entity
- wrong relation
- wrong type
- wrong scope
- stale fact
- malformed literal
- unit mismatch
- duplicate identity
- unsupported assertion
- hallucinated assertion
- provenance conflict
- policy-invalid fact
- temporal leakage
- label leakage

### 5.7 `shir:RepairAction`

A proposed or approved repair: quarantine, merge, split, re-type, re-link, re-scope, deprecate, retract, request evidence, request human review, redact, or promote.

### 5.8 `shir:CurationDecision`

A human, agent, policy, or automated decision that changes candidate status, assertion status, linkage status, ontology status, or projection eligibility.

### 5.9 `shir:ConceptualDiagnostic`

A generated consistency test derived from ontology structure or graph neighborhoods.

Diagnostics test whether a model, rule set, graph, or ontology module respects conceptual constraints such as subclass inheritance, disjointness, role expectations, and domain/range consistency.

### 5.10 `shir:ProjectionLossReport`

A required report for every lossy projection.

It records which semantics were preserved, transformed, approximated, dropped, or encoded indirectly.

## 6. Mapping rules

### 6.1 RDF to SHIR

RDF resources map to `shir:Node` objects.

RDF literals map to literal/value nodes or node attributes according to the ontology profile.

RDF predicates may map to simple binary `shir:Link` objects or to connector-backed relations when context, evidence, time, or role semantics are required.

Named graphs map to `shir:Context` objects.

Reified statements, RDF-star-style statement metadata, or PROV-qualified statements map to `shir:Assertion`, `shir:Evidence`, and `shir:TemporalScope` structures.

Blank nodes must be skolemized or stabilized by a declared canonicalization policy before deterministic projection.

### 6.2 SHIR to RDF

SHIR may be serialized back into RDF using a declared profile.

Lossless RDF round-trip is expected for simple triple graphs. Lossless round-trip is not guaranteed for all SHIR structures. When SHIR relations require role bindings, nested contexts, evidence anchors, or projection receipts, the serializer must either preserve them through RDF reification/named-graph/provenance patterns or emit a projection-loss report.

### 6.3 SHIR to graph ML

Graph-ML export must be task-aware.

The projection planner must choose whether to represent a relation as:

- a direct binary edge
- a relation node
- a hyperedge representation
- a typed edge with auxiliary feature tensors
- a subgraph pattern

A graph-ML projection must include leakage metadata, feature provenance, train/test split provenance, ontology profile, source hashes, and projection-loss reporting.

## 7. Worked example

Source statement:

```text
TopoLVM provisions local persistent volumes for Kubernetes nodes.
```

Candidate entities:

- `TopoLVM`
- `PersistentVolume`
- `KubernetesNode`
- `AgentMachineNode`
- `LocalStorage`

Candidate assertion:

```text
TopoLVM provisions PersistentVolume
```

Linkage candidate:

```text
KubernetesNode may overlap with AgentMachineNode in SourceOS/AgentOS orchestration context.
```

Noise assessment:

```text
The phrase local persistent volumes may create ambiguity between persistent and ephemeral local storage, depending on workload policy and TopoLVM configuration.
```

SHIR representation:

- connector: `provisions(provider, resource, target_context)`
- link role bindings:
  - provider -> `TopoLVM`
  - resource -> `PersistentVolume`
  - target_context -> `KubernetesNode`
- evidence anchor: source document span
- context: SourceOS/AgentOS storage profile
- policy scope: non-PII technical documentation
- temporal scope: valid for the cited version/snapshot only
- projection-loss report: required when exporting to binary edge form or PyG edge-type triples

PyG-style projection may emit:

```text
node types: Technology, StorageResource, ComputeNode, Context
edge types:
  (Technology, provisions, StorageResource)
  (StorageResource, scoped_to, ComputeNode)
  (Technology, mentioned_in, DocumentAnchor)
```

The projection-loss report must record whether the n-ary connector was reified, approximated, or split into multiple binary edges.

## 8. Validation gates

A SHIR implementation should provide gates for:

- required identifier and type fields
- evidence-anchor presence for induced assertions
- valid-time and observation-time separation
- policy-scope presence for training/export projections
- connector role completeness
- no silent n-ary-to-binary collapse
- leakage metadata before graph-ML export
- projection-loss report presence for lossy exports
- receipt presence for compiler/projection outputs

## 9. Non-goals for v0.1

- No full graph neural network trainer.
- No proprietary Hyperknowledge runtime dependency.
- No unchecked LLM-generated ontology promotion.
- No mandatory storage backend choice.
- No assumption that one graph representation is sufficient for all workloads.

## 10. Repo integration

Ontogenesis owns this semantic contract.

Semantic-serdes owns machine-readable SHIR schemas, examples, validation, and projection manifests.

Gaia-world-model owns temporal instance graphs, world-state snapshots, and replay state.

Prophet-platform-fabric-mlops-ts-suite owns executable induction, leakage, projection, and diagnostics packs.

Prophet-platform owns governance receipts, model registry, eval fabric, promotion, rollback, and publication gates.

Agentplane owns orchestration of compile, validate, project, train, evaluate, and publish jobs.

Policy-fabric owns consent, PII, export, exposure, and training-eligibility gates.

Memory-mesh and search surfaces consume SHIR-derived retrieval indexes, graph neighborhoods, embeddings, and explanation traces.
