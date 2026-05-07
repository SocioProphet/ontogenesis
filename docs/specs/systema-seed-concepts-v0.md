# Systema Seed Concepts v0

Status: draft v0.1  
Owner repository: `SocioProphet/ontogenesis`  
Parent issue: `SocioProphet/ontogenesis#63`  
Depends on: `docs/specs/systema-concept-entry-v0.md`

## Purpose

This specification defines the first Systema seed concept inventory for Ontogenesis.

The seed inventory demonstrates how Fuller/Synergetics-derived and ProCybernetica-derived doctrine enters Ontogenesis as source-anchored concept records rather than uncontrolled vocabulary.

## Source-confidence posture

All seed concepts in this tranche are `extracted_candidate` concepts unless explicitly reviewed in a later pass.

They are operational translations from the ProCybernetica Systema capture and should not be used as load-bearing quotations or proof-facing claims.

## Seed concepts included

- Dymaxion Metrics
- Tensegrity Architecture
- Geodesic Relation
- Membrane Doctrine
- Frequency Ledger
- Projection Loss
- Catalog-as-Access-Device
- Word as Industrial Tool
- Manual Commons
- Livingry Classification

See `examples/systema/seed-concepts.example.jsonld`.

## Common source anchors

The seed graph references ProCybernetica Systema source captures and profiles:

- `SocioProphet/ProCybernetica:docs/source-captures/FULLER_SYNERGETICS_COMPLETION_CAPTURE.md`
- `SocioProphet/ProCybernetica:docs/doctrine/SYNERGETIC_CYBERNETICS_ALIGNMENT.md`
- `SocioProphet/ProCybernetica:docs/evidence/SOURCE_CONFIDENCE_AND_PROJECTION_LOSS.md`
- `SocioProphet/ProCybernetica:profiles/source_confidence_profile.yaml`
- `SocioProphet/ProCybernetica:profiles/projection_loss_profile.yaml`
- `SocioProphet/ProCybernetica:profiles/frequency_ledger_profile.yaml`
- `SocioProphet/ProCybernetica:profiles/dymaxion_service_metric_profile.yaml`
- `SocioProphet/ProCybernetica:profiles/entropy_accounting_profile.yaml`
- `SocioProphet/ProCybernetica:profiles/membrane_boundary_profile.yaml`

## Promotion rule

A seed concept cannot promote beyond `extracted_candidate` until it has:

1. a stronger source review state;
2. an owning downstream repo artifact;
3. allowed and forbidden uses;
4. evidence requirements;
5. example or fixture validation;
6. revision history.

## Validation

Expected validation:

```bash
make validate
make shacl
make jsonld
make ledger
make verify
```
