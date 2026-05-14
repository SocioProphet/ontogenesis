# Ontogenesis v0.2.0 Release Candidate

## Release target

- Release name: `ontogenesis-v0.2.0`
- Candidate base commit: `c76ddb8eeb565c875331fac133fc03ca8cd465d7`
- Release status: **blocked pending validation evidence in #92**
- Release readiness issue: #92
- Registry normalization follow-up: #93
- Consolidation-methodology extraction follow-up: #94

This file is a release-candidate note, not evidence that the release has been validated or tagged.

## Scope

Ontogenesis v0.2.0 is intended to capture the 2026-05-14 consolidation tranche after validation passes.

The candidate release includes:

- Knowledge Context platform module
- Knowledge Context README compliance links
- Reasoning Failure ontology slice
- Smart Home Privacy domain pack
- GitOps consolidation addendum
- explicit release-readiness gate for validation and consumer upgrade guidance
- explicit follow-up for supplemental-registry normalization
- explicit follow-up for reusable consolidation-methodology extraction

## Candidate merged tranches

| PR | Merge SHA | Scope |
|---:|---|---|
| #90 | `76506813e153b86fb2b103729cdfbc8c61fcde44` | Knowledge Context platform ontology, SHACL gates, JSON-LD context, docs, supplemental registry |
| #37 | `c3bf6ccc43a28fc65edb041eebbee33636c61a42` | Knowledge Context compliance links in README |
| #45 | `fb20bc0e7f660d7c16a929ee2bd5d45ad954d35c` | Reasoning Failure ontology slice, SHACL gates, JSON-LD context, example, supplemental registry, docs |
| #86 | `cec66b2dac9cdbd826c937c42bb6d26d54ce9ade` | Smart Home Privacy domain pack, SHACL gates, JSON-LD context, nursery example, supplemental registry, GAIA/HDT bridge spec |
| #91 | `c76ddb8eeb565c875331fac133fc03ca8cd465d7` | Consolidation addendum documenting decisions, validation gate, draft gates, and registry posture |

## New module surfaces

### Knowledge Context

Primary files:

- `Platform/knowledge-context.ttl`
- `shapes/knowledge-context.shacl.ttl`
- `contexts/knowledge-context.context.jsonld`
- `docs/knowledge-context-module.md`
- `catalog/knowledge_context_registry.ttl`

The module gives Ontogenesis ownership of the semantic governance layer for Knowledge Context v1 artifacts: passages, mentions, entities, claims, provenance, embedding references, vector index references, and entity resolution records.

### Reasoning Failure

Primary files:

- `Platform/ReasoningFailure/reasoning-failure.ttl`
- `shapes/reasoning_failure.shacl.ttl`
- `contexts/reasoning-failure.context.jsonld`
- `examples/reasoning_failure_demo.ttl`
- `catalog/reasoning_failure_registry.ttl`
- `docs/reasoning-failure-ontology-v0.1.md`

The module makes reasoning failure a first-class semantic surface without implementing runtime execution, trace storage, routing, guardrail actions, ledger writes, or UI.

### Smart Home Privacy

Primary files:

- `Domains/smart-home-privacy.ttl`
- `shapes/smart-home-privacy.shacl.ttl`
- `contexts/smart-home-privacy.context.jsonld`
- `examples/smart-home-privacy-nursery.example.jsonld`
- `catalog/smart_home_privacy_registry.ttl`
- `docs/specs/smart_home_privacy_gaia_hdt_bridge.md`

The domain pack binds vendor privacy-policy claims to device capabilities, physical context, evidence, coverage findings, risk inferences, consent boundaries, GAIA world-model context, and HDT impact boundaries.

## Transitional registry posture

This candidate release uses supplemental registry files for the newly merged tranches:

- `catalog/knowledge_context_registry.ttl`
- `catalog/reasoning_failure_registry.ttl`
- `catalog/smart_home_privacy_registry.ttl`

This is a **transitional posture**, not a silent new registry convention.

The current recommendation is:

- v0.2.0 may ship with supplemental registries if validation passes and release notes disclose the consumer behavior.
- v0.2.1 or a follow-up cleanup should normalize the registry posture under #93.

## Consumer upgrade guidance

### Central registry consumers

Consumers that read only `catalog/registry.ttl` should not assume they have discovered the full v0.2.0 candidate module set.

Until #93 resolves registry normalization, consumers must either:

1. load the central registry plus the supplemental registry files listed above, or
2. use release notes / module-map follow-up documentation as an explicit source of the added tranches.

This is a transitional discovery requirement.

### JSON-LD context consumers

The newly added contexts are not merged into a single central context surface in this candidate state.

Consumers needing these terms should load the specific module context they use:

- Knowledge Context: `contexts/knowledge-context.context.jsonld`
- Reasoning Failure: `contexts/reasoning-failure.context.jsonld`
- Smart Home Privacy: `contexts/smart-home-privacy.context.jsonld`

Central-context consolidation, if desired, should be handled as a separate compatibility decision after validation.

### Module-map consumers

At candidate time, `docs/module-map.md` may lag the newly merged tranches. The consolidation addendum includes a safe local patch plan for a narrow module-map update.

If v0.2.0 is tagged before that follow-up lands, release notes must explicitly state that module-map updates are deferred.

## Required validation before tagging

The release must not be tagged until #92 records validation evidence.

Required command:

```bash
cd ~/dev/ontogenesis && \
  git fetch origin --prune && \
  git checkout main && \
  git pull --ff-only origin main && \
  make all
```

If `make all` does not enumerate supplemental registry tranches, run explicit checks:

```bash
python scripts/validate_rdf.py \
  Platform/knowledge-context.ttl \
  shapes/knowledge-context.shacl.ttl \
  catalog/knowledge_context_registry.ttl \
  Platform/ReasoningFailure/reasoning-failure.ttl \
  shapes/reasoning_failure.shacl.ttl \
  catalog/reasoning_failure_registry.ttl \
  Domains/smart-home-privacy.ttl \
  shapes/smart-home-privacy.shacl.ttl \
  catalog/smart_home_privacy_registry.ttl

python scripts/jsonld_roundtrip.py \
  contexts/knowledge-context.context.jsonld \
  contexts/reasoning-failure.context.jsonld \
  contexts/smart-home-privacy.context.jsonld
```

## Validation receipt requirements

The validation comment in #92 should record:

- command run
- timestamp
- local environment, including Python version and any Nix/Make environment notes
- pass / warning / failure disposition
- relevant output summary
- if failed, the failing step and suspected tranche

## Failure triage

If validation fails, diagnose in this order:

1. #90 / Knowledge Context replay and supplemental registry
2. #45 / Reasoning Failure ontology slice
3. #86 / Smart Home Privacy domain pack
4. #37 / README links
5. pre-existing main failure unrelated to consolidation

## Suggested Git tag after validation

```text
ontogenesis-v0.2.0
```

## Suggested GitHub Release title after validation

```text
Ontogenesis v0.2.0
```

## Non-goals

This candidate does not claim:

- that v0.2.0 has already been validated;
- that supplemental registries are the permanent registry convention;
- that central JSON-LD contexts have absorbed the new module contexts;
- that issue #38 is closed;
- that draft PRs #28, #67, #76, #78, or #87 are ready for merge;
- that runtime systems implement these ontology surfaces.
