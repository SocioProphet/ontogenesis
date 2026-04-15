# Hypergraph Parser, Indexing, and Linking Integration Spec

Status: Draft for implementation

Repository: `SocioProphet/ontogenesis`

Scope: This document specifies how we integrate the CMU Link Grammar parser and attributed C-sets (acsets) into the basic parsing, indexing, and linking subroutines for the SocioProphet hypergraph model.

## 1. Decision

We will use **both** techniques, but not for the same job.

- **Link Grammar** is the front-end syntactic constraint engine.
- **Attributed C-sets (acsets)** are the typed structural substrate for parse-state representation, relational indexing, incidence management, migration between schema views, and safe composition into the wider hypergraph.

The system should not treat these as competing parsers. They are complementary layers:

1. Link Grammar gives us a sentence-local constraint graph over tokens, connectors, and linkage possibilities.
2. Acsets give us a formally typed and composable in-memory and persistence-adjacent representation for those structures, including attributes, provenance, ambiguity packs, and transformation rules.
3. The hypergraph becomes the promoted semantic and operational graph after parse-state normalization, entity resolution, ontology linking, and confidence/policy gating.

## 2. Formal comparison

### 2.1 CMU Link Grammar parser

Link Grammar is a rule- and connector-based syntactic formalism in which each lexical item carries connector requirements and a valid parse is a linkage satisfying planarity and other grammar constraints. Operationally, it is a constrained graph construction problem over tokens in a sentence.

Primary strengths:

- Strong explicit syntactic constraints.
- Transparent connector logic.
- Useful for extracting typed token-token grammatical relations without requiring a transformer stack.
- Good fit for deterministic or semi-deterministic parsing pipelines where we need inspectable evidence.
- Naturally yields a graph-like intermediate representation.

Primary weaknesses:

- It is fundamentally a **syntax engine**, not a complete semantic integration substrate.
- It does not by itself solve entity resolution, ontology alignment, cross-sentence identity, long-range discourse memory, or hypergraph lifecycle management.
- Native parser outputs are not automatically an institutional-grade typed data model.
- Ambiguity management exists, but downstream packaging into policy-aware evidence structures must be built separately.

### 2.2 Attributed C-sets (acsets)

Acsets are functorial data structures that generalize graphs and data frames by combining combinatorial structure with typed attributes. They are especially strong when a domain contains multiple object types, incidence maps, and attached metadata. The paper explicitly positions acsets as a joint generalization of graphs and data frames and emphasizes that they support general operations such as limits, colimits, and functorial migration while retaining performance competitiveness【8†source】. The schema-based definition distinguishes combinatorial objects and morphisms from attribute types and attributes【8†source】.

Primary strengths:

- Excellent for representing heterogeneous graph-like structures with attached typed data.
- Clean separation between combinatorial structure and attributes.
- Strong fit for parser state, ambiguity packs, indexing tables, provenance, evidence, and migration between schema projections.
- Good basis for deterministic subroutines because indices and incidence relations can be explicit.
- Supports composition with other graph-like structures, including wiring diagrams and Petri-net-like views【8†source】.

Primary weaknesses:

- Acsets are **not** a parsing theory on their own.
- They do not supply lexical connector rules or grammatical admissibility.
- Semantic quality depends on the schemas and transformation rules we define.
- Without discipline, acset schemas can become over-general and lose operational clarity.

### 2.3 Relationship between the two

Formally, Link Grammar answers: "Which local syntactic link structures are admissible for this utterance?"

Acsets answer: "How do we represent, index, compose, mutate, validate, and transform the resulting structures and attached evidence in a typed way?"

Therefore:

- **Link Grammar is a producer of constrained syntactic relations.**
- **Acsets are the representation and transformation layer.**
- **The hypergraph is the promoted semantic-operational substrate.**

## 3. Architectural role in our stack

This integration belongs in the basic language-to-hypergraph ingestion path.

### 3.1 Pipeline placement

1. Input normalization
2. Tokenization and span formation
3. Link Grammar parse generation
4. Parse packing and ambiguity retention
5. Acset instantiation of parse state
6. Parse-state indexing
7. Ontology linking and entity resolution
8. Hyperedge promotion into the canonical hypergraph
9. Confidence, provenance, and policy gating
10. Downstream symbolic, retrieval, and agent workflows

### 3.2 Why this fits our work

This design fits our stack because we repeatedly need all of the following at once:

- explicit evidence,
- deterministic subroutines,
- typed graph composition,
- policy-aware promotion into a governed graph,
- replayable parse and link traces,
- inspectable ambiguity instead of opaque collapse,
- compatibility with ontology repositories and schema-driven evolution.

The ontogenesis repository is already an ontology- and policy-centered repository. This spec therefore belongs here as the design bridge between linguistic parsing, typed structural representation, and ontology-backed hypergraph promotion.

## 4. Canonical intermediate representations

We will maintain three distinct but connected representations.

### 4.1 LG-IR: Link Grammar intermediate representation

Sentence-local parse object containing:

- utterance_id
- token_id
- token surface form
- lemma when available
- POS or coarse lexical class when available
- connector requirements emitted by lexicon
- chosen linkages
- alternative linkages
- disjunct/connector costs if available
- parser diagnostics and failure modes

This IR is syntax-centric and ephemeral but must be serializable.

### 4.2 ACSET-Parse: typed parse-state representation

This is the authoritative typed representation for parser output before semantic promotion.

Core object classes:

- `Utterance`
- `Token`
- `Span`
- `Linkage`
- `Connector`
- `Link`
- `ParseAlternative`
- `EntityCandidate`
- `RelationCandidate`
- `OntologyCandidate`
- `Evidence`
- `Source`
- `ProvenanceEvent`

Core homs / incidence relations:

- `in_utterance : Token -> Utterance`
- `in_span : Token -> Span`
- `from_linkage : Link -> Linkage`
- `left_token : Link -> Token`
- `right_token : Link -> Token`
- `uses_left_connector : Link -> Connector`
- `uses_right_connector : Link -> Connector`
- `belongs_to_parse_alt : Linkage -> ParseAlternative`
- `supports_entity : Evidence -> EntityCandidate`
- `supports_relation : Evidence -> RelationCandidate`
- `candidate_subject : RelationCandidate -> EntityCandidate`
- `candidate_object : RelationCandidate -> EntityCandidate`
- `maps_to_ontology : EntityCandidate -> OntologyCandidate`
- `maps_relation_to_ontology : RelationCandidate -> OntologyCandidate`

Key attributes:

- token text
- normalized text
- token offsets
- connector label
- connector direction
- parse score / cost
- ambiguity class
- confidence score
- source document id
- source span coordinates
- ontology IRI candidate
- policy status
- promotion status

### 4.3 HYPER-IR: promoted canonical hypergraph representation

After entity resolution and ontology linking, we emit:

- canonical entity nodes
- canonical relation hyperedges
- event/state/time qualifiers
- provenance and confidence attachments
- policy annotations
- replay references back to ACSET-Parse and raw source spans

The hypergraph should never lose the backpointer to ACSET-Parse artifacts.

## 5. Parsing subroutines

### 5.1 Normalize

Responsibilities:

- Unicode normalization
- punctuation policy
- casing policy
- whitespace repair
- sentence segmentation
- quote and parenthesis balancing hints
- optional domain-specific lexicon substitutions

Output:

- stable tokenization input with source offsets preserved

### 5.2 Parse

Responsibilities:

- invoke Link Grammar
- generate one-or-more admissible linkages
- retain parser diagnostics
- produce connector-level evidence
- avoid premature collapse to a single interpretation when ambiguity remains material

Output:

- LG-IR parse pack

### 5.3 Pack alternatives

Responsibilities:

- group alternative parses into `ParseAlternative`
- preserve shared substructure where possible
- compute ambiguity summary metrics
- attach ranking / cost / confidence

Output:

- ambiguity-preserving ACSET-Parse instantiation

### 5.4 Extract candidates

Responsibilities:

- convert token/link patterns into provisional entity candidates
- convert token/link patterns into provisional relation candidates
- emit typed extraction templates for ontology linking

Output:

- candidate objects with evidence references

## 6. Indexing subroutines

We need explicit indexes because the parser and linker will repeatedly perform the same joins under low-latency conditions.

### 6.1 Token index

Keys:

- normalized token
- lemma
- surface form
- utterance id
- span offsets

Uses:

- lexical lookup
- inverted references
- source-span reconstruction

### 6.2 Connector signature index

Keys:

- connector label
- direction
- lexical item
- parse alternative id

Uses:

- grammar diagnostics
- connector reuse analysis
- rule debugging
- parse-template induction

### 6.3 Link pattern index

Keys:

- `(left_token_type, connector, right_token_type)`
- `(token_lemma_a, link_label, token_lemma_b)`
- local parse motif hash

Uses:

- candidate relation extraction
- relation-template learning
- ambiguity clustering

### 6.4 Candidate entity index

Keys:

- normalized surface string
- ontology candidate IRI
- type guess
- source span

Uses:

- entity dedupe
- cross-sentence resolution
- ontology reconciliation

### 6.5 Candidate relation index

Keys:

- subject candidate
- predicate candidate
- object candidate
- qualifier signature
- source span

Uses:

- relation merging
- confidence accumulation
- hyperedge promotion gates

### 6.6 Provenance index

Keys:

- source document / source message
- utterance id
- parse alternative id
- extraction rule id
- ontology linker decision id

Uses:

- auditability
- replay
- rollback
- compare-and-comply flows

## 7. Linking subroutines

### 7.1 Lexical linking

Map token or span forms to:

- known lexicon entries
- ontology labels
- aliases
- synonyms
- abbreviations
- product/system vocabulary

### 7.2 Syntactic-to-semantic linking

Convert selected link patterns into semantic relation candidates.

Examples:

- subject-verb-object patterns
- modifier attachments
- appositive identity patterns
- possession / ownership patterns
- temporal qualifier patterns
- agent / action / object templates

### 7.3 Ontology linking

Map candidates to controlled IRIs and ontology classes/properties.

Requirements:

- multiple ontology candidates may coexist until resolution
- confidence and policy state must be explicit
- no destructive overwrite of prior candidate mappings

### 7.4 Hyperedge promotion

Promote a candidate relation to the canonical hypergraph only when:

- entity candidates are sufficiently resolved,
- relation typing is admissible,
- provenance is attached,
- confidence exceeds configured threshold,
- policy gates allow promotion.

Otherwise keep it in ACSET-Parse as unresolved or provisional.

## 8. Why acsets are the correct structural layer

The acset paper is directly relevant because it treats graph-like structures plus attributes in one formalism and explicitly includes queries, data migration, limits/colimits, and structured cospans as first-class operations【8†source】. That matters for us because our parsing pipeline is not just a graph builder. It needs:

- multiple schema views over the same parse-state,
- promotion from sentence-local structure into wider graph structures,
- ambiguity retention,
- safe mutation and merge operations,
- efficient indexed access,
- compatibility with ontology-centric artifacts.

In our setting, acsets should be used for:

- parse-state object storage,
- typed incidence maintenance,
- index generation,
- view/projection generation,
- migration from sentence parse to entity/relation candidate graph,
- promotion staging before canonical hypergraph insertion.

## 9. Why Link Grammar is still necessary

Acsets alone do not give us grammatical admissibility. The Link Grammar parser gives an explicit, inspectable, connector-based syntax engine that we can use as a deterministic front-end for extraction. This is especially useful where we want:

- rule visibility,
- auditability,
- fine-grained parser diagnostics,
- connector-level debugging,
- fallback parsing when neural systems are unavailable or too opaque,
- structured evidence rather than only latent embeddings.

## 10. Proposed ontology and repo impacts

This repository should eventually carry ontology support for the parsing layer, not just a prose spec.

### 10.1 Proposed ontology modules

Recommended future module family:

- `Platform/Parsing/core.ttl`
- `Platform/Parsing/link-grammar.ttl`
- `Platform/Parsing/acset-parse.ttl`
- `Platform/Parsing/hypergraph-promotion.ttl`
- `shapes/parsing-gates.ttl`

### 10.2 Core ontology concepts to define

Classes:

- `sp:Utterance`
- `sp:Token`
- `sp:Span`
- `sp:Connector`
- `sp:Linkage`
- `sp:Link`
- `sp:ParseAlternative`
- `sp:EntityCandidate`
- `sp:RelationCandidate`
- `sp:OntologyCandidate`
- `sp:Evidence`
- `sp:PromotionDecision`

Properties:

- `sp:inUtterance`
- `sp:leftToken`
- `sp:rightToken`
- `sp:usesConnector`
- `sp:belongsToAlternative`
- `sp:supportsCandidate`
- `sp:mapsToOntology`
- `sp:promotionStatus`
- `sp:confidence`
- `sp:sourceOffsetStart`
- `sp:sourceOffsetEnd`

### 10.3 SHACL gates to add later

- Every `sp:Link` must belong to exactly one `sp:Linkage`.
- Every `sp:EntityCandidate` must have at least one evidence object.
- Promoted relations must have provenance and confidence.
- Canonical hypergraph nodes must preserve backreferences to source parse objects.
- Ontology mappings must record decision provenance.

## 11. Minimal acset schema sketch

The actual implementation schema may differ, but the structural intent is:

```julia
@present TheoryParseGraph(FreeSchema) begin
  (Utterance, Token, Span, Linkage, Connector, Link,
   ParseAlternative, EntityCandidate, RelationCandidate,
   OntologyCandidate, Evidence)::Ob

  in_utterance::Hom(Token, Utterance)
  in_span::Hom(Token, Span)
  from_linkage::Hom(Link, Linkage)
  left_token::Hom(Link, Token)
  right_token::Hom(Link, Token)
  uses_left_connector::Hom(Link, Connector)
  uses_right_connector::Hom(Link, Connector)
  belongs_to_parse_alt::Hom(Linkage, ParseAlternative)
  supports_entity::Hom(Evidence, EntityCandidate)
  supports_relation::Hom(Evidence, RelationCandidate)
  candidate_subject::Hom(RelationCandidate, EntityCandidate)
  candidate_object::Hom(RelationCandidate, EntityCandidate)
  maps_entity_to_ontology::Hom(EntityCandidate, OntologyCandidate)
  maps_relation_to_ontology::Hom(RelationCandidate, OntologyCandidate)

  StringT::AttrType
  FloatT::AttrType
  IntT::AttrType
  BoolT::AttrType

  token_text::Attr(Token, StringT)
  token_norm::Attr(Token, StringT)
  token_start::Attr(Token, IntT)
  token_end::Attr(Token, IntT)
  connector_label::Attr(Connector, StringT)
  connector_dir::Attr(Connector, StringT)
  parse_cost::Attr(Linkage, FloatT)
  confidence::Attr(Evidence, FloatT)
  promoted::Attr(RelationCandidate, BoolT)
  ontology_iri::Attr(OntologyCandidate, StringT)
end
```

## 12. Execution model

### 12.1 Required invariants

- Token offsets are immutable once assigned.
- Parse alternatives are append-only; ranking may change, raw alternatives do not.
- Hypergraph promotion must preserve provenance pointers.
- Ontology linking must be non-destructive and evidence-backed.
- Candidate merging must be reversible or at least replayable.

### 12.2 Failure modes to handle

- no valid link grammar parse
- too many parses / ambiguity explosion
- lexical unknowns
- conflicting ontology mappings
- cross-sentence identity collisions
- hyperedge promotion denied by policy

### 12.3 Fallback policy

When Link Grammar fails or is underdetermined:

- preserve tokens and spans,
- emit partial candidate structures,
- mark parse state as degraded,
- allow downstream assistive resolution,
- do not silently fabricate high-confidence edges.

## 13. Acceptance criteria

This integration is only acceptable when all of the following are true:

1. We can parse a sentence into Link Grammar structures and serialize the result.
2. We can instantiate the parse into an ACSET-Parse object without losing offsets, connector labels, or alternative parse information.
3. We can index tokens, connectors, entity candidates, and relation candidates with stable IDs.
4. We can promote resolved relation candidates into the canonical hypergraph while preserving provenance backreferences.
5. We can reject promotion under SHACL/policy conditions.
6. We can replay the transformation from source span to hyperedge.
7. We can handle unresolved ambiguity without forced collapse.

## 14. Recommended implementation sequence

### Phase 1

- Define ontology vocabulary for parse artifacts.
- Implement LG-IR serialization contract.
- Implement initial ACSET-Parse schema.
- Add token/link/provenance indexes.

### Phase 2

- Add entity and relation candidate extraction.
- Add ontology candidate linking.
- Add promotion rules into the hypergraph.
- Add SHACL gates for provenance and promotion admissibility.

### Phase 3

- Add ambiguity packing metrics.
- Add cross-sentence resolution.
- Add replay and diff tooling.
- Add policy-aware merge/split handling for candidate entities and canonical nodes.

## 15. Explicit recommendation

We should adopt the combined design.

- Do **not** replace Link Grammar with acsets.
- Do **not** attempt to force Link Grammar to become the persistence/indexing substrate.
- Use Link Grammar as the syntactic admissibility engine.
- Use acsets as the typed parse-state and transformation substrate.
- Use the canonical hypergraph as the promoted semantic-operational substrate.

That division of labor is the correct fit for our governed, evidence-first, ontology-backed stack.

## 16. Source basis

The acset side of this design is grounded in *Categorical Data Structures for Technical Computing* (Patterson, Lynch, Fairbanks), which defines attributed C-sets as a typed generalization of graph-like and tabular structures and describes their mathematical and implementation properties, including schema definition, attributed graph structures, queries, and composition【8†source】.
