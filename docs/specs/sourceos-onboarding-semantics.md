# SourceOS Onboarding Semantics

## Purpose

This specification binds the SourceOS/SociOS onboarding control-plane contracts from `SourceOS-Linux/sourceos-spec` into Ontogenesis RDF/OWL/SHACL semantics.

The semantic slice covers:

- `WorkspaceScope`
- `TrustMode`
- `CapabilityPack`
- `ConnectorActionScope`
- `AutomationTemplate`
- `OnboardingReceipt`
- supporting concepts for role profiles and permission vocabulary entries

The goal is to make onboarding not just a UI ceremony, but a governable graph surface that Sociosphere, Agentplane, SourceOS Shell, Prophet Platform, and future Ontogenesis gates can query and validate.

## Files

| File | Purpose |
|------|---------|
| `Platform/sourceos/onboarding.ttl` | RDF/OWL semantic lift for the onboarding contract family |
| `shapes/sourceos/onboarding.shacl.ttl` | SHACL gates for minimum semantic correctness |
| `examples/sourceos/onboarding-receipt-example.jsonld` | Example graph binding workspace, trust, capability, connector scope, automation, and receipt |
| `catalog/sourceos-onboarding-registry.ttl` | Supplemental module registry entry for this tranche |

## Contract source of truth

The JSON Schema contracts remain canonical in `SourceOS-Linux/sourceos-spec`.

Ontogenesis adds semantic validation and graph interoperability. It does not replace the JSON Schema definitions.

## Core classes

`srcos:WorkspaceScope` represents the bounded workspace or repository context selected during onboarding.

`srcos:TrustMode` represents the user-visible permission envelope.

`srcos:CapabilityPack` represents a curated bundle of skills, connector scopes, policies, expected artifacts, and revocation behavior.

`srcos:ConnectorActionScope` represents exact connector verbs, risk, approval, and access-level semantics.

`srcos:AutomationTemplate` represents reusable governed work-product templates.

`srcos:OnboardingReceipt` represents the proof artifact for what was selected, enabled, disabled, scoped, trialed, and made revocable.

## Initial SHACL gates

The initial gates intentionally focus on high-value correctness rules:

1. `WorkspaceScope` must declare `workspaceKind` and `mountMode`.
2. `TrustMode` must declare a supported `riskLevel`.
3. `CapabilityPack` must reference at least one skill and declare `receiptRequired`.
4. `ConnectorActionScope` must distinguish exact allowed actions and access level.
5. High-risk or critical connector scopes must require explicit approval.
6. `AutomationTemplate` must require receipts.
7. `OnboardingReceipt` must reference a workspace scope and trust mode.
8. Enabled capability packs, connector scopes, and automation templates must resolve to their corresponding classes when present in the graph.

## Downstream bindings

Sociosphere should use these terms to validate workspace onboarding manifests, capability-pack registry entries, automation template registry entries, and onboarding receipts.

Agentplane should use these terms to attach onboarding context to validation, placement, run, replay, and receipt artifacts.

SourceOS Shell should use these terms to drive first-run onboarding, permission cards, capability catalog filtering, composer runtime footer state, and evidence-rail state.

Prophet Platform should index these terms so onboarding receipts become searchable evidence artifacts.

## Follow-up work

Next semantic slices should add:

- `RoleProfile` as a full semantic module or a dedicated JSON Schema in sourceos-spec.
- `PermissionVocabulary` and canonical action taxonomy.
- `AutomationBinding` and `AutomationRunRecord` semantics.
- `RevocationRecord` semantics.
- `WorktreeScope` semantics for branch/worktree policy.
- Richer SHACL gates for Browser Use, Computer Use, credential use, source exposure, purpose binding, data classification, and retention.
