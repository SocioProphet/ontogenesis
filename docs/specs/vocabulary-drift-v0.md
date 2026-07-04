# Vocabulary Drift v0

Status: draft v0.1  
Owner repository: `SocioProphet/ontogenesis`  
Parent issue: `SocioProphet/ontogenesis#63`  
Depends on: `docs/specs/systema-concept-entry-v0.md`

## Purpose

Vocabulary drift is the condition where the same term, alias, label, policy phrase, UI label, schema field, or agent instruction carries materially different meanings across repositories, artifacts, runtimes, or time.

Systema treats vocabulary as interoperability infrastructure. A term is not merely a token. It is a governed interface between source, concept, policy, implementation, search, and user-facing surfaces.

## Scope

This tranche adds the Ontogenesis-side vocabulary drift model and SHACL gate.

It does not implement runtime scanning, search ranking, or automatic refactoring. Downstream tools can later emit `systema:VocabularyDriftReport` instances for review and remediation.

## Core classes

| Class | Meaning |
| --- | --- |
| `systema:TermUsage` | A repo/artifact-specific usage of a term, alias, label, or field |
| `systema:VocabularyDriftReport` | A report that two or more term usages conflict, diverge, or require governance |
| `systema:DriftResolution` | A proposed or accepted resolution path for the drift |

## Drift kinds

| Drift kind | Meaning |
| --- | --- |
| `alias_conflict` | Two aliases point to different concepts or scopes |
| `definition_conflict` | Same term has incompatible definitions |
| `scope_drift` | Term scope widened or narrowed without versioning |
| `policy_language_drift` | Policy text and implementation semantics diverge |
| `schema_label_drift` | Schema field or JSON-LD term meaning diverges from concept definition |
| `ui_label_drift` | UI label implies a different concept than the ontology/policy surface |
| `agent_instruction_drift` | Agent-facing instruction uses a term differently from governed doctrine |
| `stale_term` | Term remains in use after deprecation or supersession |
| `unowned_term` | Term lacks owner repo, concept record, or promotion state |

## Severity

| Severity | Meaning |
| --- | --- |
| `notice` | visible drift, not blocking |
| `warn` | material review burden or possible confusion |
| `error` | blocks promotion or release readiness |
| `critical` | creates trust, safety, public-claim, or execution risk |

## Required fields

A `systema:VocabularyDriftReport` should include:

- `systema:term`
- `systema:driftKind`
- `systema:severity`
- at least two `systema:termUsage`
- at least one `systema:evidenceRef`
- `systema:ownerRepo`
- `systema:resolutionPath`
- `systema:reviewState`

A `systema:TermUsage` should include:

- `systema:term`
- `systema:ownerRepo`
- `systema:surfacePath`
- `systema:meaningText`
- optional `systema:conceptRef`

## Promotion rule

A doctrine-bearing term cannot be promoted to `public_standard` when it has unresolved `error` or `critical` vocabulary drift.

A term used in a runtime, policy, or public claim surface should either map to a governed concept or be explicitly classified as provisional.

## Example

See:

- `examples/systema/vocabulary-drift.example.ttl`

## Validation

The SHACL gate is:

- `shapes/vocabulary_drift.shacl.ttl`

Expected validation:

```bash
make validate
make shacl
make jsonld
make ledger
make verify
```
