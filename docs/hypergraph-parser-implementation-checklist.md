# Hypergraph Parser Implementation Checklist

This checklist operationalizes `docs/hypergraph-parser-acset-linkgrammar-spec.md`.

## Phase 1 — parser artifact model

- [ ] Finalize the parsing core ontology vocabulary in `Platform/Parsing/core.ttl`
- [ ] Finalize Link Grammar-specific vocabulary in `Platform/Parsing/link-grammar.ttl`
- [ ] Finalize ACSET parse-state vocabulary in `Platform/Parsing/acset-parse.ttl`
- [ ] Finalize hypergraph promotion vocabulary in `Platform/Parsing/hypergraph-promotion.ttl`
- [ ] Add SHACL gates in `shapes/parsing-gates.ttl`
- [ ] Define the LG-IR serialization contract
- [ ] Define canonical object identifiers for utterance, token, span, linkage, and candidate objects
- [ ] Define ambiguity pack representation and ranking metadata

## Phase 2 — runtime ingestion path

- [ ] Implement input normalization with stable source offsets
- [ ] Implement sentence segmentation policy
- [ ] Integrate CMU Link Grammar parser invocation
- [ ] Serialize raw parse output into LG-IR
- [ ] Instantiate ACSET-Parse objects from LG-IR
- [ ] Build token, connector, link-pattern, entity-candidate, relation-candidate, and provenance indexes
- [ ] Add parse failure/degraded-state handling

## Phase 3 — linking and promotion

- [ ] Implement entity candidate extraction templates
- [ ] Implement relation candidate extraction templates
- [ ] Add ontology candidate linking
- [ ] Add confidence and policy status propagation
- [ ] Add canonical hypergraph promotion routines
- [ ] Preserve parse backreferences during node/edge promotion
- [ ] Enforce SHACL promotion gates before canonical insertion

## Phase 4 — validation and replay

- [ ] Add replay from source span -> LG-IR -> ACSET-Parse -> canonical hyperedge
- [ ] Add ambiguity retention tests
- [ ] Add promotion denial tests
- [ ] Add provenance completeness tests
- [ ] Add parser failure fallback tests
- [ ] Add deterministic ID and indexing tests

## Acceptance checks

- [ ] Sentence parses serialize without losing offsets or connector labels
- [ ] ACSET-Parse instantiation preserves parse alternatives
- [ ] Candidate extraction is evidence-backed
- [ ] Canonical hypergraph insertion preserves provenance
- [ ] Policy gates can deny promotion cleanly
- [ ] Replay can reconstruct the source path for any promoted edge
