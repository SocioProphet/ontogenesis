# Model Plane ontology module (T7-7 / T7-8)

OWL + SHACL realization of the SourceOS Model Plane provider concept, the ontogenesis
side of Tranche 7 (sourceos-spec `InferenceProvider` + the Model Plane spec §VIII).

## Files
- `Domains/model-plane/inference-provider.ttl` (T7-7) — the `mp:InferenceProvider` OWL
  class and its residency/capability properties. Namespace
  `https://spec.sourceos.dev/vocab/model-plane#`, mirroring the agent-system sourceos
  realization.
- `shapes/model-plane/residency-constraints.shacl.ttl` (T7-8) — the residency teeth.
- `examples/model-plane/model-plane-providers.ttl` — positive fixtures (an on-device
  biometric `visiond` provider; a sovereign-cluster teacher).
- `examples/model-plane/invalid/*.invalid.ttl` — four negative fixtures, one per
  invariant.
- `scripts/validate_model_plane_examples.py` + `make validate-model-plane` — the lane
  validator asserting the positive conforms and each negative is rejected on its
  expected signal.

## Design decision (ADR-0017 in sourceos-spec)
A model-serving daemon is **not** a sixth `AgentPassport` agent class. It is an
`agentsys:HostAgent` (typically `system_core`) **and** an `mp:InferenceProvider`,
linked by `mp:passportRef`. The provider is modeled as an `upper:System`, composed
with — not a subtype of — the host-process classification.

## Enforced invariants (residency-constraints SHACL)
1. `dataResidencyClass` is exactly one of `{on_device_only, sovereign_cluster, external_permitted}`.
2. `emitsInferenceReceipt` must be `true` — a provider that emits no receipts is not a valid provider (§VIII).
3. `on_device_only` ⇒ `networkCapability false` (SEAM-015).
4. `escalationPermitted` ⇒ `dataResidencyClass ≠ on_device_only` (SEAM-015).
5. `handlesBiometric` ⇒ `on_device_only` **and** `escalationPermitted false` — the biometric hard boundary.

Invariants 3–5 are cross-field and expressed as `sh:sparql` constraints (the global
gate runs pyshacl with `advanced=True`).

## Out of scope (tracked in sourceos-spec #247)
Cross-document manifest-digest binding (`ModelAdapterManifest.baseModelDigest ==
ModelManifest.modelDigest`, carry-ref → manifest resolution) needs the sourceos-spec
manifests represented as RDF instances here; that is a later shape, not part of the
residency constraints.
