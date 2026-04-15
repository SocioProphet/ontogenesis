# Parsing module family

This directory holds the initial ontology scaffolding for the language-to-hypergraph ingestion path described in:

- `docs/hypergraph-parser-acset-linkgrammar-spec.md`
- `docs/hypergraph-parser-implementation-checklist.md`

Current module stubs:

- `core.ttl` — shared parsing vocabulary for utterances, tokens, spans, links, candidates, evidence, and promotion decisions
- `link-grammar.ttl` — Link Grammar-specific classes and properties
- `acset-parse.ttl` — ACSET parse-state representation vocabulary
- `hypergraph-promotion.ttl` — promotion and gating vocabulary for canonical hypergraph insertion

These files are scaffolding, not the final ontology design. They exist to establish stable paths, namespaces, and implementation lanes for the parser/indexer/linker buildout.
