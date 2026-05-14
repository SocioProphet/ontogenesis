# Governed Intelligence Canonical Contracts (v1)

This binding records the portable contract surfaces around the canonical SocioProphet governed-intelligence object model.

The canonical semantic model is the Platform-scoped ontology already landed in Ontogenesis:

`Observe -> Anchor -> Normalize -> Propose -> Explain -> Verify -> Govern -> Act -> Receipt -> Learn`

## Canonical objects

- Entity
- Anchor
- Evidence
- Claim
- ProofCertificate
- ExplanationTrace
- VectorCandidate
- PolicyDecision
- ActionProposal
- ActionAdmission
- RuntimeReceipt
- LearningEvent
- Revocation
- SlashTopicProfile
- VectorEncodingManifest

## Canonical repository surfaces

- OWL/RDF terms: `Platform/GovernedIntelligence/governed-intelligence.ttl`
- SHACL shapes: `shapes/governed_intelligence.shacl.ttl`
- JSON-LD context: `contexts/governed-intelligence.context.jsonld`
- Registry supplement: `catalog/governed_intelligence_registry.ttl`
- Object-model spec: `docs/specs/governed-intelligence-object-model-v0.md`

## Contract-side additions

- JSON Schema: `schemas/governed-intelligence.v1.schema.json`
- Vector encoding manifest: `manifests/governed-intelligence.vector-encoding.manifest.v1.json`

## Boundary discipline

This binding does not introduce a second Middle-layer governed-intelligence ontology. The Platform-scoped ontology remains canonical:

`https://socioprophet.github.io/ontogenesis/platform/governed-intelligence#`

Any downstream schema, vector manifest, fixture, or generated contract must target that namespace unless a future migration explicitly changes the canonical location.

## Deferred artifact notes

- Avro-compatible record generation: deferred; no Avro generation pipeline exists in this repository today.
- TriTRPC IDL generation: deferred; no TriTRPC generator/tooling exists in this repository today.
- Kubernetes CRD mapping notes: deferred; current module boundaries are ontology-first and not CRD-first.
