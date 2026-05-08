# Governed Intelligence Canonical Contracts (v1)

This binding captures the canonical SocioProphet governed-intelligence object model used by the reference architecture loop:

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

## Generated / mapped artifacts in this repository

- OWL/RDF terms: `Middle/governed-intelligence.ttl`
- SHACL shapes: `shapes/governed-intelligence.shacl.ttl`
- JSON Schema: `schemas/governed-intelligence.v1.schema.json`
- JSON-LD context: `contexts/governed-intelligence.context.jsonld`
- Vector encoding manifests: `manifests/governed-intelligence.vector-encoding.manifest.v1.json`

## Worked examples

- text evidence span to policy decision:
  - `examples/governed-intelligence-evidence-policy-demo.ttl`
- action proposal to admission to runtime receipt:
  - `examples/governed-intelligence-action-receipt-demo.ttl`

## Deferred artifact notes

- Avro-compatible record generation: deferred (no Avro generation pipeline exists in this repository today).
- TriTRPC IDL generation: deferred (no TriTRPC generator/tooling exists in this repository today).
- Kubernetes CRD mapping notes: deferred (current module boundaries are ontology-first and not CRD-first).
