# Capability Fabric Ontology Alignment Note

This repository is an **ontology and dictionary alignment consumer** of the canonical Capability Fabric standards.

## Canonical source of truth

The protocol-independent Capability Fabric core and realization-profile standards live in:

- `SocioProphet/socioprophet-standards-knowledge`
  - `docs/standards/040-capability-fabric-core.md`
  - `docs/standards/041-capability-fabric-realization-profiles.md`
  - `docs/standards/042-capability-fabric-delivery-and-receipts.md`
  - `docs/standards/043-capability-fabric-controllability-and-proof-strength.md`
  - `schemas/jsonschema/capability-fabric/`

## Scope in this repository

This repository MAY define:
- ontology and JSON-LD alignment for capability-fabric concepts
- controlled vocabulary bindings
- namespace mappings
- dictionary and term-system governance
- SHACL shapes or validation overlays for ontology-backed usage

This repository MUST NOT redefine the canonical semantics of:
- `FunctionIdentity`
- `CapabilitySignature`
- `EffectContext`
- `InteractionMode`
- `DeliverySemantics`
- `ReceiptSemantics`
- `ExecutionControllabilityProfile`
- `ProofStrengthProfile`
- `RealizationMetadata`

These semantics MUST be imported, referenced, or aligned to the canonical source rather than re-specified here.

## Intended follow-on work

Future ontology work in this repository SHOULD explain:
- how capability-fabric objects map into ontology modules and namespaces
- how closed dictionaries and term systems are governed
- how ontology-backed validation constrains or extends usage without mutating the core semantic definitions
