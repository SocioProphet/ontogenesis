# Governed Intelligence Object Model v0

Status: draft
Parent issue: `SocioProphet/ontogenesis#77`
Rollout issue: `SocioProphet/sociosphere#310`

## Purpose

This specification defines the Ontogenesis schema root for the SocioProphet governed-intelligence reference architecture.

The architecture turns raw observations, model outputs, graph results, vector candidates, and agent intents into governed claims and governed actions through the canonical loop:

```text
Observe -> Anchor -> Normalize -> Propose -> Explain -> Verify -> Govern -> Act -> Receipt -> Learn
```

Ontogenesis owns the canonical semantic vocabulary, SHACL shape surface, JSON-LD context terms, and vector encoding manifest pattern for the objects below. Runtime behavior remains in the consuming repos.

## Non-negotiable invariants

- Raw model output is a proposal, not admitted truth.
- Raw graph candidates are proposals, not admitted truth.
- Raw vector candidates remain `candidate_only`.
- Holmes verifies and explains claims but does not admit them.
- Guardrail/Policy Fabric admits, denies, requires review, or marks provisional.
- Agentplane performs effectful work only after action admission and emits runtime receipts.

## Canonical objects

| Object | Required purpose | Key fields |
| --- | --- | --- |
| `Entity` | Canonical actor, concept, repo, region, model, artifact, or domain object. | `identifier`, `label`, `entityType`, `lifecycleStatus` |
| `Anchor` | Pointer into a source artifact. | `artifactRef`, `selectorType`, `selector`, `sourceRef`, `confidence` |
| `Evidence` | Source-backed support or opposition. | `anchorRef`, `evidenceRole`, `provenanceRef`, `validTime` |
| `Claim` | Typed assertion over subject, predicate, object, context, evidence, and lifecycle state. | `subject`, `predicate`, `object`, `context`, `evidenceRef`, `status` |
| `ProofCertificate` | Structured reasoning artifact. | `claimRef`, `hypotheses`, `rulesApplied`, `conclusion`, `checker` |
| `ExplanationTrace` | Human/operator-readable reasoning path. | `claimRef`, `traceStep`, `evidenceRef`, `confidence` |
| `VectorCandidate` | Candidate returned by vector-symbolic or embedding recall. | `queryRef`, `candidateRef`, `similarity`, `matchedRoles`, `status = candidate_only` |
| `PolicyDecision` | Admission decision for a claim/action/model/artifact/workflow. | `targetRef`, `decision`, `policyRef`, `reason` |
| `ActionProposal` | Structured proposal to perform effectful work. | `agentRef`, `actionType`, `scope`, `expectedEffect`, `evidenceRef` |
| `ActionAdmission` | Admission state for an action proposal. | `proposalRef`, `decisionRef`, `admissionState` |
| `RuntimeReceipt` | Execution record after admitted work. | `actionRef`, `agentRef`, `runtimeRef`, `inputHash`, `outputHash`, `logRef`, `status` |
| `LearningEvent` | Evaluation, drift, calibration, adoption, rollout, or feedback event. | `sourceRef`, `eventType`, `metric`, `status` |
| `Revocation` | Lifecycle withdrawal/supersession event. | `targetRef`, `reason`, `supersedes`, `effectiveTime` |
| `SlashTopicProfile` | Governance membrane over allowed objects, evidence requirements, policy profile, and query/display behavior. | `topic`, `allowedType`, `requiredEvidence`, `policyProfile` |

## Lifecycle status vocabulary

Objects that represent claims, evidence, policies, actions, or receipts should use a controlled status vocabulary:

```text
proposed | provisional | admitted | denied | require_review | superseded | revoked | expired
```

`VectorCandidate` is stricter. It must remain:

```text
candidate_only
```

A vector candidate can become input evidence for a proposed claim, but it is never itself an admitted claim.

## Policy decision vocabulary

`PolicyDecision` and `ActionAdmission` use:

```text
allow | deny | require_review | provisional
```

## Anchor selector types

The first selector vocabulary is:

```text
text_span | image_region | geometry | h3_cell | code_range | log_range | table_cell | audio_segment | video_clip | generic_selector
```

## Example: text evidence to governed claim

A Sherlock answer over a technical document should produce:

```text
Anchor(text_span) -> Evidence(supports) -> Claim(proposed) -> ExplanationTrace -> PolicyDecision
```

The claim is not admitted until downstream policy decides it is allowed, provisional, denied, or requires review.

See `examples/governed-intelligence/text-claim.example.jsonld`.

## Example: action proposal to runtime receipt

An agent action should produce:

```text
ActionProposal -> PolicyDecision/ActionAdmission -> RuntimeReceipt
```

The action proposal may reference evidence and expected effects. The runtime receipt must reference the policy decision and record inputs, outputs, hashes, runtime identity, and status.

See `examples/governed-intelligence/action-receipt.example.jsonld`.

## Vector encoding manifest pattern

Vector-symbolic candidate generation is defined by a manifest rather than ad hoc vectors. A manifest declares roles, source schema, vector type, dimensions, candidate-only status, and cleanup index references.

Required invariant:

```text
VectorCandidate.status = candidate_only
```

See `examples/governed-intelligence/vector-encoding-manifest.example.json`.

## Ontology placement

Initial terms live in:

- `Platform/GovernedIntelligence/governed-intelligence.ttl`
- `shapes/governed_intelligence.shacl.ttl`
- `contexts/governed-intelligence.context.jsonld`

The module is Platform-layer because it is a shared contract surface used by Sherlock, Holmes, GAIA, Policy/Guardrail Fabric, Agentplane, Model Governance Ledger, and Sociosphere.

## Repo boundary notes

| Repo | Boundary |
| --- | --- |
| `ontogenesis` | Canonical semantic vocabulary, shapes, context, examples, vector encoding manifest pattern. |
| `holmes` | Reasoning traces, proof claims, contradiction reports, truth bounds. |
| `sherlock-search` | Evidence-answer pipeline, anchors, answer candidates, vector candidates for retrieval. |
| `gaia-world-model` | Spatial-temporal world claims, geospatial anchors, fusion evidence, uncertainty. |
| `guardrail-fabric` / `policy-fabric` | Admission policies and decisions. |
| `agentplane` | Action proposals, admissions, runtime receipts. |
| `model-governance-ledger` | Training runs, inference traces, evaluation reports, drift, learning events. |
| `sociosphere` | Slash-topic membranes and rollout/adoption projection. |

## Validation expectations

A complete implementation should validate:

1. Turtle parses for `Platform/GovernedIntelligence/governed-intelligence.ttl`.
2. SHACL parses for `shapes/governed_intelligence.shacl.ttl`.
3. JSON-LD context parses for `contexts/governed-intelligence.context.jsonld`.
4. Example JSON-LD files contain required object chains.
5. Vector encoding manifest uses `candidate_only` for vector candidate output.

Run the repository validation pipeline where available:

```bash
make validate
make shacl
make jsonld
```

Full release validation remains:

```bash
make all
```
