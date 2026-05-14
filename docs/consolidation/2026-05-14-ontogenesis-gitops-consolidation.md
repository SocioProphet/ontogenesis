# Ontogenesis GitOps Consolidation Addendum — 2026-05-14

## Purpose

This addendum records the 2026-05-14 Ontogenesis PR consolidation pass and preserves the operational decision trail for the module map, supplemental registries, remaining drafts, and issue-closure discipline.

The consolidation goal was to reduce stale PR surface without damaging current `main`, especially because ontology modules carry layer, registry, SHACL, JSON-LD, ledger, and downstream-consumer implications.

## Final merged tranches

| PR | Merge SHA | Classification | Notes |
|---:|---|---|---|
| #90 | `76506813e153b86fb2b103729cdfbc8c61fcde44` | Platform / Knowledge Context | Current-main replay of the Knowledge Context module. Supersedes #40, which superseded #30. |
| #37 | `c3bf6ccc43a28fc65edb041eebbee33636c61a42` | README / compliance links | Companion docs PR for Knowledge Context links. Merged only after #90 landed. |
| #45 | `fb20bc0e7f660d7c16a929ee2bd5d45ad954d35c` | Platform / Reasoning Failure | Additive reasoning-failure ontology slice with SHACL, context, example, registry supplement, and docs. |
| #86 | `cec66b2dac9cdbd826c937c42bb6d26d54ce9ade` | Domain / Smart Home Privacy | Additive smart-home privacy domain pack with SHACL, context, example, registry supplement, and GAIA/HDT bridge spec. |

## Supersession chain

### Knowledge Context

The original Knowledge Context chain is now:

```text
#30 -> #40 -> #90
```

- #30 was closed unmerged as superseded by #40.
- #40 was later closed unmerged after GitHub rejected it with merge conflicts.
- #90 was created as a current-main replay that preserved Knowledge Context module content without carrying stale registry/module-map edits forward.

The key decision was to avoid merging the stale primary-registry and module-map edits from #40 because `main` had advanced substantially and contained newer ontology modules and registry entries.

## Registry discipline used in this pass

The merged tranches prefer supplemental registry files instead of direct edits to the primary registry when replaying stale or additive modules:

- `catalog/knowledge_context_registry.ttl`
- `catalog/reasoning_failure_registry.ttl`
- `catalog/smart_home_privacy_registry.ttl`

This pattern avoids destructive conflicts in `catalog/registry.ttl` while preserving discoverability for downstream compilers. A later registry-normalization pass may fold these supplements into the primary registry if the repo chooses to centralize again.

## Module-map follow-up

`docs/module-map.md` was intentionally not rewritten in the connector pass. The file is large and the prior stale branch showed that broad replacement can risk deleting newer mainline entries.

Recommended follow-up is a narrow local patch, not a connector-side full rewrite:

```bash
cd ~/dev/ontogenesis && \
  git fetch origin --prune && \
  git checkout main && \
  git pull --ff-only origin main && \
  git checkout -b docs/module-map-merged-tranches && \
  python - <<'PY'
from pathlib import Path
p = Path('docs/module-map.md')
s = p.read_text()
platform_anchor = '- `Platform/lattice-ontology-query.ttl`\n  - governed ontology-query adapter contract for Lattice FederatedQueryPlane; distinct from SPARQL routing\n'
platform_insert = platform_anchor + '- `Platform/knowledge-context.ttl`\n  - Knowledge Context v1 semantic governance: passages, mentions, entities, claims, provenance, embeddings, vector index references, and entity resolution records\n- `Platform/ReasoningFailure/`\n  - `reasoning-failure.ttl` — reasoning-failure ontology slice covering failure modes, perturbations, invariants, verifiers, traces, mitigation patterns, residual risk, regression cases, and evidence receipts\n  - SHACL: `shapes/reasoning_failure.shacl.ttl`\n  - JSON-LD context: `contexts/reasoning-failure.context.jsonld`\n  - example: `examples/reasoning_failure_demo.ttl`\n'
if platform_anchor in s and 'Platform/knowledge-context.ttl' not in s:
    s = s.replace(platform_anchor, platform_insert)

domain_anchor = '- `Domains/agentic-purple-team.ttl` — governed agentic purple-team loops/actions, evidence envelopes, safety boundaries, gates, atomic tests, countermeasure rules, run receipts/summaries, AI/MCP/agent-skill risk, graph robustness, and MITRE-compatible local technique model\n'
domain_insert = domain_anchor + '- `Domains/smart-home-privacy.ttl` — smart-home privacy governance for vendors, devices, capabilities, physical contexts, privacy claims, evidence, coverage findings, risk inferences, consent boundaries, GAIA bindings, and HDT impact bindings\n'
if domain_anchor in s and 'Domains/smart-home-privacy.ttl' not in s:
    s = s.replace(domain_anchor, domain_insert)

registry_anchor = '- `catalog/semantic_enterprise_registry.ttl` — supplemental semantic-enterprise registry tranche\n'
registry_insert = registry_anchor + '- `catalog/knowledge_context_registry.ttl` — supplemental Knowledge Context registry tranche\n- `catalog/reasoning_failure_registry.ttl` — supplemental reasoning-failure registry tranche\n- `catalog/smart_home_privacy_registry.ttl` — supplemental smart-home privacy registry tranche\n'
if registry_anchor in s and 'catalog/knowledge_context_registry.ttl' not in s:
    s = s.replace(registry_anchor, registry_insert)

context_anchor = '- `contexts/governed-intelligence.context.jsonld` — governed-intelligence context\n'
context_insert = context_anchor + '- `contexts/knowledge-context.context.jsonld` — Knowledge Context context\n- `contexts/reasoning-failure.context.jsonld` — reasoning-failure context\n- `contexts/smart-home-privacy.context.jsonld` — smart-home privacy context\n'
if context_anchor in s and 'contexts/knowledge-context.context.jsonld' not in s:
    s = s.replace(context_anchor, context_insert)

gate_anchor = '- SHACL bundles: `shapes/core.shacl.ttl`, `shapes/ontogenesis.shacl.ttl`, `shapes/cybernetic-self.shacl.ttl`, `shapes/product-service.shacl.ttl`, `shapes/parsing-gates.ttl`, `shapes/ontology-query.shacl.ttl`, `shapes/valueflows-governed.shacl.ttl`, `shapes/michael-belief.shacl.ttl`, `shapes/human-digital-twin.shacl.ttl`, `shapes/kg_lifecycle.shacl.ttl`, `shapes/semantic_mapping.shacl.ttl`, `shapes/named_graph_governance.shacl.ttl`, `shapes/agentic-purple-team.shacl.ttl`, `shapes/governed_intelligence.shacl.ttl`\n'
gate_insert = '- SHACL bundles: `shapes/core.shacl.ttl`, `shapes/ontogenesis.shacl.ttl`, `shapes/cybernetic-self.shacl.ttl`, `shapes/product-service.shacl.ttl`, `shapes/parsing-gates.ttl`, `shapes/ontology-query.shacl.ttl`, `shapes/valueflows-governed.shacl.ttl`, `shapes/michael-belief.shacl.ttl`, `shapes/human-digital-twin.shacl.ttl`, `shapes/kg_lifecycle.shacl.ttl`, `shapes/semantic_mapping.shacl.ttl`, `shapes/named_graph_governance.shacl.ttl`, `shapes/agentic-purple-team.shacl.ttl`, `shapes/governed_intelligence.shacl.ttl`, `shapes/knowledge-context.shacl.ttl`, `shapes/reasoning_failure.shacl.ttl`, `shapes/smart-home-privacy.shacl.ttl`\n'
if gate_anchor in s:
    s = s.replace(gate_anchor, gate_insert)

p.write_text(s)
PY
```

Then run:

```bash
make all && git diff -- docs/module-map.md
```

Only open and merge that follow-up after the diff is confirmed to be additive.

## Required post-merge validation

Run the full validation pipeline on final main:

```bash
cd ~/dev/ontogenesis && \
  git fetch origin --prune && \
  git checkout main && \
  git pull --ff-only origin main && \
  make all
```

If `make all` does not enumerate supplemental registry tranches, run explicit file-level checks for the new tranches:

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

## Issue-closure discipline

Do not close an issue only because a PR mentions it. Closure requires acceptance-criteria verification.

Recommended verification flow:

1. Read the issue acceptance criteria.
2. Compare the merged diff against every criterion.
3. Close only if fully satisfied.
4. If partially satisfied, comment with the merged coverage and create or update follow-up issues for the remaining criteria.

Immediate candidate:

- #38 may be partially or fully addressed by #45, but it requires explicit verification against the issue's criteria before closure.

## Remaining draft PRs

| PR | Current gate |
|---:|---|
| #28 | Banking twin draft: needs registry decision before promotion. Either add registry/context completion and undraft, or close with content preserved for a later banking tranche. |
| #67 | ViewContract draft: known gaps remain — example JSON-LD graph, registry entries, context file, and full SHACL pipeline wiring. |
| #76 | Copilot Prophet artifact draft: requires ontology review of class hierarchy, domains/ranges, SHACL tightness, namespace alignment, examples, and registry metadata. |
| #78 | Copilot governed-intelligence draft: requires duplication review against already-present `Platform/GovernedIntelligence/` content and schema-surface review before promotion. |
| #87 | LC-VSM query ChatOps draft: decide whether to remain docs/profile-only or become a full module with ontology, context, SHACL, registry, and roundtrip checks. |

## Failure handling rule

If validation fails after a merge:

- If the failure is local to the merged tranche, fix forward or revert that merge.
- If the failure reveals current `main` is already broken, stop PR consolidation and repair main first.
- If the failure is due to supplemental registry enumeration gaps, update the validation harness so supplemental registries are included explicitly.
