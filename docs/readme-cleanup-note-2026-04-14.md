# Root README cleanup note — 2026-04-14

This note records the current documentation cleanup debt on `main` after the upstream merges that landed after parsing PR `#5`.

## Observed state

The current root `README.md` contains two distinct layers that are both still present:

1. a newer Ontogenesis framework-oriented introduction with current base/version IRI, layered binding explanations, alignment-in-the-wild framing, and application-boundary language
2. a retained older repository-operations section beginning again with `# Ontogenesis`

As a result, the file currently has duplicated title framing and mixed-era structure.

## Why this matters

The parsing lane now exists as a first-class ontology/module family under `Platform/Parsing/`, but the root README does not yet present that family as part of the repo surface in a clean way. The broader issue is not just one missing bullet; the root README currently needs structural normalization.

## Recommended cleanup

### Keep

- the newer opening framework explanation
- the current base/version IRI section
- the layered mapping/binding explanation
- the ontology-alignment-in-the-wild framing
- the diagrams section
- the license and validation instructions

### Fold or rewrite

- the second `# Ontogenesis` heading
- duplicated repository-purpose language that follows it
- mixed old/new release-discipline narration where it can be normalized into one operational section

### Add

- a concise "Current module families" section mentioning parsing surfaces, including:
  - `Platform/Parsing/core.ttl`
  - `Platform/Parsing/link-grammar.ttl`
  - `Platform/Parsing/acset-parse.ttl`
  - `Platform/Parsing/hypergraph-promotion.ttl`
  - `shapes/parsing-gates.ttl`
  - `tools/validate_parsing.py`

## Suggested end state

The root README should have one opening title, one conceptual overview, one current-framework/module-surface section, one validation section, one license section, and one diagrams section. It should not restart itself midway through the file.
