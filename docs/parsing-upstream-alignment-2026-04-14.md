# Parsing upstream alignment note — 2026-04-14

This note records the upstream state of `SocioProphet/ontogenesis` after the parsing integration work from PR `#5` and the subsequent upstream changes that landed in PR `#8` and the product/service tranche.

## Current upstream baseline checked before this branch

- Parsing integration PR `#5` is already merged into `main`.
- Current `main` head at branch creation time for this cleanup branch is commit `1f74a9438ca5d13b28af0e0f2ca95563f8dd261f`.
- Upstream moved after PR `#5`, including:
  - merged product/service tranche
  - `README.md` rewrite/expansion
  - delivered-state invariant fixes

## Why this branch exists

The original parsing lane successfully established the parsing module family and SHACL bundle paths, but one ontology scaffold remained semantically rough:

- `Platform/Parsing/acset-parse.ttl`

Specifically:

1. it subclasses `core:Entity`, which is not defined in `Platform/Parsing/core.ttl`
2. several name/key fields are modeled as object properties where datatype properties are more appropriate
3. the branch-level fix should land against current `main`, not against the old merged parsing branch

## What this branch does

Because the GitHub connector path available from chat did not reliably permit in-place tree rewriting for existing files on this repository, this branch lands an additive aligned replacement scaffold:

- `Platform/Parsing/acset-parse-aligned.ttl`

This file is intended as the corrected semantic target for a follow-on replacement of `acset-parse.ttl` once direct in-place file patching is available through the chosen execution path.

## Why this is still useful

This branch provides:

- an exact upstream checkpoint note
- a reviewable corrected ontology variant
- a clean basis for a future direct replacement PR
- a way to continue parsing-lane work without pretending upstream stood still

## Recommended next action

When a file-rewrite-capable path is available, replace `Platform/Parsing/acset-parse.ttl` with the aligned content from `Platform/Parsing/acset-parse-aligned.ttl`, then remove the aligned variant file and fold the result into the canonical parsing module family.
