# Parsing module family note

This note consolidates the current parsing-oriented ontology surfaces in `ontogenesis` and records the current operational state of the language-to-hypergraph ingestion lane.

## Purpose

The parsing module family exists to support a governed pipeline from language inputs into typed parse-state artifacts and onward into canonical hypergraph structures.

The intended division of labor remains:

- **Link Grammar** as the syntactic admissibility engine
- **ACSET-backed parse state** as the typed structural representation and indexing substrate
- **Canonical hypergraph promotion** as the semantic-operational landing surface

## Current module surfaces

### Ontology modules

- `Platform/Parsing/core.ttl`
  - shared vocabulary for utterances, tokens, spans, links, candidates, evidence, and promotion decisions
- `Platform/Parsing/link-grammar.ttl`
  - Link Grammar-specific connector, disjunct, linkage, lexicon, and parse-failure terms
- `Platform/Parsing/acset-parse.ttl`
  - canonical ACSET parse-state scaffold
- `Platform/Parsing/hypergraph-promotion.ttl`
  - promotion decisions, gates, and backreference-preservation terms

### Policy and validation surfaces

- `shapes/parsing-gates.ttl`
  - SHACL bundle for parsing links, entity candidates, relation candidates, and promotion decisions
- `tools/validate_parsing.py`
  - dedicated validator for the parsing ontology family
- `.github/workflows/validate-parsing.yml`
  - dedicated CI lane for parser-family validation

### Design and implementation notes

- `docs/hypergraph-parser-acset-linkgrammar-spec.md`
- `docs/hypergraph-parser-implementation-checklist.md`
- `docs/parsing-upstream-alignment-2026-04-14.md`

## Current operational status

### What is already in place

- parsing ontology module family paths exist
- parser-family SHACL bundle exists
- dedicated parser-family validator exists
- dedicated parser-family CI workflow exists
- the canonical ACSET scaffold has been normalized onto `Platform/Parsing/acset-parse.ttl`

### Historical note

The earlier temporary aligned replacement file was used as an intermediate correction target while the available connector path did not yet support a safe canonical file overwrite from chat. That temporary split state has been resolved in the cleanup branch for this change set.

## Validation commands

Broader repo validation:

```bash
python tools/validate.py
```

Parsing-family validation:

```bash
python tools/validate_parsing.py
```

## Why this note exists

The repo documentation surface moved substantially after the parsing lane first landed. This note makes the parsing family discoverable in the current documentation era without assuming that every reader will reconstruct the sequence from merged PRs alone.
