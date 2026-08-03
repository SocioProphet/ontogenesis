# Consent Plane — OS ontologies for purpose-bound, consent-gated tool use

The semantic ground for the SourceOS **consent plane (E1)** and the
`sourceos-spec` integrated-agent-native-stack contract. Four aligned ontologies
+ a fail-closed SHACL projection make "role × surface × space × tool × purpose +
consent" (GDPR Art 5(1)(b) purpose-limitation) a *checked* structure, not prose.

| File | Ontology | Grounds |
|---|---|---|
| `consent-purpose.ttl` | **Purpose limitation** — closed purpose set (discover/implement/verify/ship/operate/egress/administer), `ConsentGrant` (Art 6 basis + Art 7 conditions), `ToolInvocation` (the join point, aligned to the Action Ontology `act:Action`). | KKO upper · Action Ontology |
| `isolation-spaces.ttl` | **OS layer** — `IsolationSpace` (kernel/system/user/agent/data-namespace), `Taint`/`Toleration` (k8s-style boundary gates), `Surface`, the six `SecuritySeam` kinds, and `SeamAssurance` (per-surface purple-team evidence). Ties `agentsys:ManagedSpace` (concrete macOS spatial auth) under the abstract space model. | agent-system · upper |
| `accessibility-binding.ttl` | **Accessibility** — `AssistiveAction ⊑ ToolInvocation`: human-via-AT and agent drive the *same* typed, consented, receipted act on the *same* seam. `AccessibilityDefault` = accommodations default-on, agent-assist opt-in. | consent-purpose |
| `app-intent-profile.ttl` | **Per-app intents** — `Intent` (grounded in the 23×6 intent grid), `AppProfile` binding each intent to purposes/spaces/seams/default-consent. App-native App-Intents, but purpose-bound not capability-only. | isolation-spaces · intent grid |

## Fail-closed teeth — `shapes/consent_plane.shacl.ttl`

Every constraint **refuses**, it does not warn:

- a `ToolInvocation` must bind exactly one admissible `Purpose`, a `ConsentGrant`, a space, and a surface;
- entering the **data-namespace** with no `Toleration` → refused (no cross-tenant bleed);
- an **egress/administer** invocation with no receipt → refused (E4 warrant);
- `lawfulBasis=consent` with no `grantedAt` → refused (Art 7);
- a `Surface` declaring a seam with no passing `SeamAssurance` → refused (no unaudited failure path).

## Proof

- `scripts/validate_consent_plane_examples.py` — `examples/consent-plane/conformant-invocation.ttl` **conforms**; `examples/consent-plane/invalid/violating-invocation.ttl` **fails on exactly** the three intended teeth. Run in CI across every domain by the *Lane conformance* step.
- The whole merged estate graph still `Conforms: True` under `scripts/shacl_gate.py` (these shapes do not flag the vocabulary — evidence is separated from the seam kinds).
