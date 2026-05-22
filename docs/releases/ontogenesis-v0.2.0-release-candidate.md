# Ontogenesis v0.2.0 Release Decision

## Release target

- Release name: `ontogenesis-v0.2.0`
- Current release-decision base commit: `baf94964d851b51388463c3d1fe64e72c2ed4f3c`
- Release status: **ready for tag after operator approval**
- Release readiness issue: #92
- Registry posture issue: #93 — resolved by #107
- Consolidation-methodology extraction follow-up: #94

This file records the current release decision state. It is not itself a Git tag.

## Decision summary

Ontogenesis v0.2.0 can be cut from `baf94964d851b51388463c3d1fe64e72c2ed4f3c` after operator approval.

The release is no longer blocked by missing validation evidence or ambiguous registry posture:

- the consolidation and replay PRs were merged through exact-head protected PRs;
- CI validation evidence is recorded in #92 and PR bodies;
- the supplemental registry posture is documented and validated by #107;
- open PR count is zero at the time of this decision update.

## Merged release scope

The v0.2.0 release scope includes the original 2026-05-14 consolidation tranche plus the later current-main replay/completion tranches and the corpus-event schema tranche.

### Original consolidation tranche

| PR | Merge SHA | Scope |
|---:|---|---|
| #90 | `76506813e153b86fb2b103729cdfbc8c61fcde44` | Knowledge Context platform ontology, SHACL gates, JSON-LD context, docs, supplemental registry |
| #37 | `c3bf6ccc43a28fc65edb041eebbee33636c61a42` | Knowledge Context compliance links in README |
| #45 | `fb20bc0e7f660d7c16a929ee2bd5d45ad954d35c` | Reasoning Failure ontology slice, SHACL gates, JSON-LD context, example, supplemental registry, docs |
| #86 | `cec66b2dac9cdbd826c937c42bb6d26d54ce9ade` | Smart Home Privacy domain pack, SHACL gates, JSON-LD context, nursery example, supplemental registry, GAIA/HDT bridge spec |
| #91 | `c76ddb8eeb565c875331fac133fc03ca8cd465d7` | Consolidation addendum documenting decisions, validation gate, draft gates, and registry posture |

### Current-main replay and completion tranche

| PR | Merge SHA | Scope |
|---:|---|---|
| #98 | `092b028384574ac30671500fa46f2b4ea501c332` | LC-VSM query / ChatOps semantic spine replay |
| #99 | `03de2491c1357caf62399c89ebb3c1d3c2708d21` | View Governance ontology, SHACL, JSON-LD context, example, registry, module-map, JSON-LD harness |
| #100 | `2c24e8f97f8262574f36891f03e41f11d544218f` | Governed-intelligence JSON Schema, vector manifest, binding README, module-map entries |
| #101 | `905908aa04f5a6389d1fc341c361201aadd304d3` | Prophet Artifact ontology, SHACL, JSON-LD context, examples, registry, docs, integrity query |
| #102 | `fbd4c21d0dc5c658a22ac6059e2c6114333025eb` | Banking Twin seed tranche, remediation, registry, module-map, JSON-LD harness |
| #103 | `b67f458fe8f19fa37505784e4e072c7b954a04dd` | Corpus Event Semantics ontology, SHACL, fixtures, focused validator, docs, registry |
| #107 | `baf94964d851b51388463c3d1fe64e72c2ed4f3c` | Registry discovery posture doc, validator, and Makefile wiring |

## New and updated module surfaces

### Knowledge Context

Primary files:

- `Platform/knowledge-context.ttl`
- `shapes/knowledge-context.shacl.ttl`
- `contexts/knowledge-context.context.jsonld`
- `docs/knowledge-context-module.md`
- `catalog/knowledge_context_registry.ttl`

Ontogenesis owns the semantic governance layer for Knowledge Context v1 artifacts: passages, mentions, entities, claims, provenance, embedding references, vector index references, and entity resolution records.

### Reasoning Failure

Primary files:

- `Platform/ReasoningFailure/reasoning-failure.ttl`
- `shapes/reasoning_failure.shacl.ttl`
- `contexts/reasoning-failure.context.jsonld`
- `examples/reasoning_failure_demo.ttl`
- `catalog/reasoning_failure_registry.ttl`
- `docs/reasoning-failure-ontology-v0.1.md`

This module makes reasoning failure a first-class semantic surface. Broader fixture-family coverage is tracked separately in #106.

### Smart Home Privacy

Primary files:

- `Domains/smart-home-privacy.ttl`
- `shapes/smart-home-privacy.shacl.ttl`
- `contexts/smart-home-privacy.context.jsonld`
- `examples/smart-home-privacy-nursery.example.jsonld`
- `catalog/smart_home_privacy_registry.ttl`
- `docs/specs/smart_home_privacy_gaia_hdt_bridge.md`

The domain pack binds vendor privacy-policy claims to device capabilities, physical context, evidence, coverage findings, risk inferences, consent boundaries, GAIA world-model context, and HDT impact boundaries.

### LC-VSM Query / ChatOps

Primary files:

- `docs/specs/lc-vsm-query-chatops-object-model-v0.md`
- `examples/lc-vsm-query-chatops-sample.json`

This tranche records a documentation/profile-first semantic bridge for distributed Sherlock Search, Matrix ChatOps, WordOps, and SocioSphere query-loop work.

### View Governance

Primary files:

- `Platform/view-governance.ttl`
- `shapes/view-governance.shacl.ttl`
- `contexts/view-governance.context.jsonld`
- `examples/view-governance-demo.ttl`
- `catalog/view_governance_registry.ttl`
- `docs/specs/view-governance.md`

This tranche defines Ontogenesis-side semantics and gates for authority-bound ViewContract objects.

### Governed Intelligence

Primary files:

- `Platform/GovernedIntelligence/governed-intelligence.ttl`
- `shapes/governed_intelligence.shacl.ttl`
- `contexts/governed-intelligence.context.jsonld`
- `catalog/governed_intelligence_registry.ttl`
- `docs/specs/governed-intelligence-object-model-v0.md`
- `schemas/governed-intelligence.v1.schema.json`
- `manifests/governed-intelligence.vector-encoding.manifest.v1.json`
- `bindings/governed_intelligence/README.md`

The schema/vector manifest replay intentionally avoided creating a duplicate Middle-layer governed-intelligence ontology. Worked example flows remain tracked in #105.

### Prophet Artifact

Primary files:

- `prophet/prophet_artifact.ttl`
- `prophet/shapes/prophet_artifact.shacl.ttl`
- `contexts/prophet-artifact.context.jsonld`
- `examples/prophet_artifact_examples.ttl`
- `examples/prophet-artifact-gaia-bounded-osm-ingest.example.jsonld`
- `examples/prophet-artifact-notebook-promotion.example.jsonld`
- `examples/prophet-artifact-sourceos-image-reproducibility.example.jsonld`
- `catalog/prophet_artifact_registry.ttl`
- `docs/specs/prophet_artifact_contract.md`
- `tests/prophet-artifact-integrity.rq`

This tranche turns the computational artifact contract into an Ontogenesis-native ontology and promotion-gate surface.

### Banking Twin

Primary files:

- `Middle/banking-core.ttl`
- `Domains/balance-sheet.ttl`
- `Domains/regulatory-reporting.ttl`
- `contexts/banking.context.jsonld`
- `shapes/banking-core.shacl.ttl`
- `examples/banking_twin_minimal.jsonld`
- `catalog/banking_registry.ttl`
- `docs/banking-reference-crosswalk.md`

The replay remediated undefined upper-core references and records FIBO/BIAN as reference anchors only, not conformance claims.

### Corpus Event Semantics

Primary files:

- `Platform/corpus-event-semantics.ttl`
- `shapes/corpus-event-semantics.shacl.ttl`
- `examples/corpus-event-semantics/valid/corpus-event-semantics.valid.ttl`
- `tests/fixtures/corpus-event-semantics/invalid/`
- `scripts/validate_corpus_event_semantics.py`
- `catalog/corpus-event-semantics-registry.ttl`
- `docs/corpus-event-semantics.md`

This tranche implements the first deployable corpus-derived event/provenance/diagnostic semantics family. JSON-LD/YAML serialization fixtures are tracked in #104.

## Registry discovery posture

Registry posture is now explicit and validated.

Decision: **hybrid-discovery-now, normalization-decision-later**.

Consumer rule:

1. Load `catalog/registry.ttl` as the primary registry.
2. Also discover supplemental registry files under `catalog/` matching:
   - `*registry*.ttl`
   - `*.registry.ttl`

The authoritative policy document is:

- `docs/registry-discovery-posture.md`

The validation target is:

```bash
make validate-registry-discovery
```

It is included in:

```bash
make validate
```

This means supplemental registry files are not abandoned sidecars and not invisible transitional debris. They are part of the current discovery surface until a future normalization PR either folds entries into `catalog/registry.ttl` or formally adopts hybrid discovery permanently.

## Consumer upgrade guidance

### Registry consumers

Consumers must load both:

- the primary registry: `catalog/registry.ttl`
- supplemental registry files under `catalog/` matching the discovery rule above

Consumers that read only `catalog/registry.ttl` should treat their view as incomplete for v0.2.0.

### JSON-LD context consumers

Contexts remain per-module. Consumers should load the specific module context they need. v0.2.0 does not claim a merged central JSON-LD context.

Notable contexts include:

- `contexts/knowledge-context.context.jsonld`
- `contexts/reasoning-failure.context.jsonld`
- `contexts/smart-home-privacy.context.jsonld`
- `contexts/view-governance.context.jsonld`
- `contexts/governed-intelligence.context.jsonld`
- `contexts/prophet-artifact.context.jsonld`
- `contexts/banking.context.jsonld`

### Module-map consumers

`docs/module-map.md` has been updated across the consolidation/replay pass to include the merged tranches. It is a human-readable index, not the sole machine discovery source.

Machine discovery should use the registry discovery rule.

## Validation evidence

The release decision is supported by PR-level CI evidence.

Validated before merge:

- #98: `CI`, `validate`, `no-raster-images`
- #99: ontology validation, RDF parse, SHACL gates, JSON-LD roundtrip, dist + ledger verify, SPDX SBOM, `no-raster-images`
- #100: `CI`, `validate`, `semantic-import-contract`, `no-raster-images`
- #101: RDF parse, SHACL gates, JSON-LD roundtrip, dist + ledger verify, SPDX SBOM, `CI`, `validate`, `no-raster-images`
- #102: RDF parse, SHACL gates, JSON-LD roundtrip, dist + ledger verify, SPDX SBOM, `CI`, `validate`, `no-raster-images`
- #103: `CI`, `validate`, `no-raster-images`; CI job detail passed RDF parse, SHACL gates, JSON-LD roundtrip, dist + ledger verify, SPDX SBOM
- #107: `CI`, `validate`, `no-raster-images`; CI job detail passed RDF parse, SHACL gates, JSON-LD roundtrip, dist + ledger verify, SPDX SBOM

## Remaining non-release-blocking follow-ups

These are explicitly tracked and should not block v0.2.0 unless the operator chooses to broaden release scope:

- #94 — Extract reusable PR consolidation methodology after Ontogenesis pass
- #104 — Add corpus-event JSON-LD/YAML serialization fixtures
- #105 — Add governed-intelligence worked examples for claim and action flows
- #106 — Expand reasoning-failure examples and negative fixtures across ten families

## Suggested Git tag

```text
ontogenesis-v0.2.0
```

## Suggested GitHub Release title

```text
Ontogenesis v0.2.0
```

## Suggested release claim

Ontogenesis v0.2.0 consolidates the ontology estate after the 2026-05 replay pass, adds first-class semantic surfaces for Knowledge Context, Reasoning Failure, Smart Home Privacy, View Governance, Governed Intelligence contracts, Prophet Artifact contracts, Banking Twin seed semantics, LC-VSM Query/ChatOps, and Corpus Event Semantics, and formalizes hybrid registry discovery with validation.

## Non-goals

This release does not claim:

- runtime implementation of the ontology surfaces;
- permanent central-only or permanent hybrid registry posture;
- merged central JSON-LD context semantics;
- complete governed-intelligence worked examples;
- complete corpus-event JSON/YAML fixture coverage;
- complete reasoning-failure positive/negative fixture coverage;
- FIBO or BIAN conformance for the Banking Twin seed tranche.
