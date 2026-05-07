# Systema Concept Entry v0

Status: draft v0.1  
Owner repository: `SocioProphet/ontogenesis`  
Parent issue: `SocioProphet/ontogenesis#63`  
Source doctrine: `SocioProphet/ProCybernetica` Systema profiles and source-confidence law

## Purpose

The Systema Concept Entry model turns doctrine-bearing terms into source-anchored, reviewable, machine-readable concept records.

A concept is not just a word, tag, or UI label. A concept is a governed record with aliases, source anchors, operational definition, allowed uses, forbidden uses, evidence requirements, implementation surfaces, promotion state, and revision history.

This module supports the Fuller/Synergetics-derived Dictionary Doctrine while preserving the ProCybernetica source-confidence rule: low-confidence OCR, visual-only source cards, and operational translations remain candidate material until reviewed.

## Scope

This tranche adds the Ontogenesis-side concept entry shape and example. It does not create runtime search behavior, public answer generation, or platform promotion actions.

## Core classes

| Class | Meaning |
| --- | --- |
| `systema:SystemaConceptEntry` | Governed concept record for doctrine-bearing concepts |
| `systema:SourceAnchor` | Source reference with confidence, review state, and quote boundary |
| `systema:ConceptDefinition` | Textual or operational definition with claim level |
| `systema:ConceptUseBoundary` | Allowed and forbidden use boundary |
| `systema:ImplementationSurface` | Owning or consuming repo/artifact surface |
| `systema:EvidenceRequirement` | Evidence needed for concept promotion or use |
| `systema:ConceptRevision` | Revision/change note for concept history |

## Required fields

Every `systema:SystemaConceptEntry` should include:

- `systema:conceptId`
- `skos:prefLabel`
- at least one `systema:sourceAnchor`
- at least one `systema:definition`
- one `systema:operationalDefinition`
- one `systema:promotionState`
- at least one `systema:allowedUse`
- at least one `systema:forbiddenUse`
- at least one `systema:implementationSurface`
- at least one `systema:evidenceRequirement`

## Promotion states

```text
observed_term -> extracted_candidate -> source_anchored -> reviewed_definition -> operational_definition -> implementation_linked -> tested_doctrine -> public_standard -> deprecated | contested
```

## Source confidence

Source anchors should preserve:

- `systema:sourceRef`
- `systema:sourceKind`
- `systema:extractionConfidence`: `A`, `B`, `C`, `D`, or `E`
- `systema:reviewState`
- `systema:quoteBoundary`
- `systema:uncertaintyNote`

## Claim boundary

Concept entries must distinguish:

- historical source claim;
- operational definition;
- design analogy;
- formal claim;
- implementation requirement;
- conformance rule.

Analogy is not proof. A concept can inspire design without supporting a formal or scientific claim.

## First example concept

The first fixture models `systema:dictionary-doctrine`, which states that a serious concept is a source-anchored, cross-referenced, promoted object, not just a word.

See:

- `examples/systema/concept-entry.example.jsonld`

## Validation

The SHACL gate is:

- `shapes/systema_concept_entry.shacl.ttl`

Expected local validation after this tranche:

```bash
make validate
make shacl
make jsonld
make ledger
make verify
```

## Ownership boundary

Ontogenesis owns the machine-readable concept/dictionary governance layer.

ProCybernetica owns constitutional doctrine, profile semantics, conformance expectations, and downstream fanout.

Sherlock consumes concept entries for evaluated access.

GAIA, AgentPlane, SourceOS, Delivery Excellence, and Prophet Platform may reference concept entries as evidence or doctrine anchors, but they should not redefine the concept-entry model.
