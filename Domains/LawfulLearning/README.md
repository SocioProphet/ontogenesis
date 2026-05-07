# LawfulLearning Domain Module

## Purpose

This domain module reserves the ontology vocabulary for calibrated lawful learning across SocioProphet.

The general doctrine and executable reference examples land in `SocioProphet/ProCybernetica`. Ontogenesis owns the semantic vocabulary, SHACL gates, and generated downstream schema alignment.

## Vocabulary to define

Initial vocabulary targets:

- `LawfulLearningModel`
- `SpectralState`
- `SpectralMode`
- `UnitaryExpansion`
- `SpatialConnection`
- `PoincareEmbedding`
- `ConstraintFamily`
- `SlackVariable`
- `Gate`
- `LearnedThreshold`
- `GateTemperature`
- `HyperparameterTrial`
- `LawfulAdmissibility`
- `EvidenceConfidence`
- `TruthScore`
- `Observer`
- `ObserverStableEvidence`
- `LedgerDigest`
- `ReplayArtifact`

## Required validation concepts

SHACL gates should validate that any asserted `LawfulLearningRun` includes:

- model state definition;
- constraint definitions;
- tuning record;
- ledger record;
- observer identity;
- truth score definition;
- explicit disclaimer when examples are illustrative.

## Boundary

This domain module is a semantic placeholder for follow-up OWL/SHACL/JSON-LD generation. It does not claim that empirical runs have occurred.

## Depends on

- `SocioProphet/ProCybernetica#23`
