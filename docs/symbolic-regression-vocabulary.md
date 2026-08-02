# Symbolic Regression Vocabulary Draft

Status: v0.2 Ontogenesis vocabulary draft. Cross-referenced against the Kautz/NSR
method-family taxonomy per `SocioProphet/ontogenesis#126` (see "Neuro-symbolic
method-family cross-reference" below).

This document records the Ontogenesis side of PROMETHEUS / symbolic-regression law discovery. Ontogenesis owns vocabulary draft and SHACL semantics. It does not own runtime execution, agent replay, policy admission, memory promotion, or canonical sourceos-spec schema promotion.

WebProtege is optional. It may be one semantic review surface, but it is not required by the contract.

## Position

Symbolic-regression output is candidate material until reviewed.

Equation candidates and program candidates may become `SRAssertionProposal` instances. They do not become admitted `SRAssertion` instances until evidence replay, semantic validation, and governance have occurred.

The safe flow is: EquationCandidate or ProgramCandidate becomes SRAssertionProposal. The proposal carries dataset evidence, feature set, operator library, fit metric, complexity metric, dimensional analysis, discovery method, replay reference, proposal promotion status, proposal admission state, vocabulary version, vocabulary promotion state, and a non-authority declaration. A configured semantic review surface may then display or edit the proposal. Only an admitted proposal becomes an SRAssertion.

## Dimensional analysis is first-class

Dimensional analysis is not a minor validation note. It is a gate.

Every equation candidate should carry a `DimensionalAnalysisResult` with `hasUnitsStatus` equal to one of: `sr:UnitsConsistent`, `sr:UnitsInconsistent`, `sr:UnitsUnknown`, or `sr:UnitsUnchecked`.

`hasUnitsStatus` is declared as a functional property. An equation candidate or dimensional analysis result should carry exactly one units status.

An inconsistent candidate may be stored as failure corpus because it is useful for search and curriculum. It must not be promoted beyond candidate status. It must not become proposed or admitted. It must not be treated as a law, ontology assertion, policy, or controller regardless of fit score.

Unknown and unchecked are allowed as draft states, but they should prevent automatic admission.

## Automated gate default

`automated_shacl_gate` should be the default semantic review surface for high-confidence candidates only after a machine-readable gate policy exists. A candidate may use the automated gate when dimensional status is consistent, fit metrics are below policy threshold, complexity is within policy, evidence replay is present, and Ontogenesis SHACL validates without violation.

TODO for the AgentPlane sprint: define the machine-readable high-confidence gate policy. The policy must encode the fit metric threshold, complexity ceiling, minimum dataset support or sample count, replay hash requirement, dimensional-status requirement, and any CHRONOS risk flags that force human review. Until that companion policy shape exists, the automated gate language in this document is advisory doctrine, not an executable admission rule.

Human review surfaces are exception handlers. Use `git_pr`, `webprotege`, `sparql_editor`, `cli`, or `prophet_platform_ui` for dimensionally ambiguous equations, low-data fits, novel operator combinations, high-governance-risk carriers, or any candidate flagged by CHRONOS.

The automated gate is not authority by itself. It is a configured review surface that still depends on evidence replay and the current governance policy.

## Optional semantic review surface

The vocabulary uses `SemanticReviewSurface` rather than making WebProtege mandatory.

Allowed review surface types are: git_pr, prophet_platform_ui, cli, sparql_editor, automated_shacl_gate, and webprotege.

The property `webProtegeProjectRef` is optional and should only appear when a deployment uses WebProtege.

## Vocabulary lifecycle versus proposal admission

There are two separate lifecycle axes.

Vocabulary lifecycle describes the namespace and vocabulary contract. It uses `vocabVersion` plus `vocabularyPromotionState`. The vocabulary promotion states are: draft, stabilizing, and canonical. Ontogenesis owns draft and stabilizing vocabulary. SourceOS-spec may later receive canonical schema material after stabilization.

Proposal admission describes a specific equation or program candidate. It uses `hasPromotionStatus` and `hasAdmissionState`. Proposal promotion states include candidate, proposed, admitted, rejected, and failure_corpus. Admission states include pending_review, admitted, rejected, and blocked.

Do not conflate vocabulary promotion with equation admission. A canonical vocabulary may still contain rejected equation candidates. A draft vocabulary may still carry candidate artifacts. SourceOS-spec promotion is not the same event as admitting a specific equation.

The `vocabVersion` field is required on SRAssertionProposal so downstream JSON-LD/RDF consumers can migrate from the Ontogenesis draft namespace to a later SourceOS-spec canonical namespace without breaking.

## Core classes

`EquationCandidate` is a symbolic-regression equation output before semantic, evidence, policy, or runtime admission.

`ProgramCandidate` is a generated program or function candidate from program-search or LLM-SR-style methods.

`SRAssertionProposal` is the review object emitted by PROMETHEUS after evidence and metrics are attached.

`SRAssertion` is an admitted assertion after review. This draft defines the term for continuity, but does not promote any proposal to admitted status.

`DimensionalAnalysisResult` records units and dimensional status.

`DatasetEvidenceRef`, `FeatureSetRef`, `OperatorLibraryRef`, `FitMetric`, `ComplexityMetric`, `DiscoveryMethodRef`, and `EvidenceReplayRef` carry the supporting structure.

## Required proposal posture

An SRAssertionProposal must include dataset evidence, fit metric, complexity metric, dimensional analysis, evidence replay, discovery method, proposal promotion status, proposal admission state, vocabulary version, vocabulary promotion state, and a non-authority declaration.

A proposal with `hasUnitsStatus` set to `sr:UnitsInconsistent` must be blocked from proposed or admitted status by SHACL.

A proposal must carry `hasEvidenceReplay` before the automated SHACL gate can validate it.

## Neuro-symbolic method-family cross-reference

`SocioProphet/ontogenesis#126` tracks the follow-on from `sociosphere/docs/integration/neurosymbolic-chronos-alignment.md`'s authority-plane table, which assigns Ontogenesis the "Semantic vocabulary draft" role for the ASU/Kautz neuro-symbolic method-family taxonomy. This is that follow-on, applied additively to this vocabulary.

Before this extension, an `EquationCandidate` produced by a dILP-style rule-learning method and one produced by ordinary symbolic regression looked identical in this vocabulary: nothing carried which method family produced a candidate, so downstream consumers could not apply the alignment doctrine's per-method-family admissible/forbidden-use rules.

`EquationCandidate`, `ProgramCandidate`, and `SRAssertionProposal` may now carry `mf:hasMethodFamily` from the shared `vocab/method-family/method-family.ttl` module. Its enumeration is the closed Kautz/NSR classification lens: `mf:NeuralToSymbolic`, `mf:SymbolicToNeural`, `mf:Hybrid`, `mf:RuleGuided`, `mf:EmbeddedSymbolic`, `mf:System1Reasoning`, `mf:System2Reasoning`. Per the doctrine, this label is a classification tag only -- it carries no maturity or authority grade of its own; promotion is still governed exclusively by `hasPromotionStatus` / `hasAdmissionState` as described above.

`mf:hasMethodFamily` is optional and fully backward compatible: an ordinary symbolic-regression proposal that declares no method family at all is unaffected. Once a proposal *does* declare `mf:hasMethodFamily`, SHACL requires it to also carry the alignment doctrine's remaining carrier-boundary fields: `mf:groundingStatus`, `mf:validationStatus`, `mf:methodOutputType`, `mf:explanationTraceRef`, and `mf:owningAuthorityPlane`. The doctrine's other carrier-boundary fields -- source evidence reference, non-authority declaration, replay reference, and governance decision/pending -- were already covered by this vocabulary's pre-existing `hasDatasetEvidence`, `nonAuthorityDeclaration`, `hasEvidenceReplay`, and `hasAdmissionState` fields, so this extension only adds what was missing rather than duplicating what already existed.

The legacy `sr:methodFamily` free-text property (present since v0.1, never used by any fixture) is unchanged but now documented as superseded by `mf:hasMethodFamily` for the closed Kautz/NSR taxonomy specifically; it remains available for any other free-text labeling need.

This extension does not redefine or take ownership of CHRONOS's canonical carrier model; it only makes this vocabulary's own carrier classes able to express which neuro-symbolic method family (if any) produced a given candidate or proposal, which is exactly Ontogenesis's stated "semantic vocabulary draft" role.

Prior to this change, this vocabulary tranche (unlike `corpus-event-semantics`) had no dedicated validator, no example fixtures, and no invalid fixtures, so its SHACL shapes were never exercised in this repo. `scripts/validate_symbolic_regression.py`, `examples/symbolic-regression/valid/symbolic-regression.valid.ttl`, `tests/fixtures/symbolic-regression/invalid/*.ttl`, and `catalog/symbolic-regression-vocabulary-registry.ttl` close that gap and additionally prove the method-family extension. Run:

```bash
make validate-symbolic-regression
```

The target is also included in `make validate`.

## Authority boundary

Ontogenesis defines this draft vocabulary and SHACL shape.

AgentPlane should own evidence and replay schemas.

SocioSphere owns cross-repo rollout and CHRONOS carrier registration.

SourceOS-spec may later receive canonical schemas after this draft stabilizes.

Policy fabric owns admission to policy or controller use.

Memory-mesh owns symbolic-numeric memory and retrieval only after carrier boundaries are observed.

## Implementation notes

This tranche intentionally avoids implementation code and model/tool installation. PySR, SINDy, KAN, LLM-SR, TPSR, and SNIP should all emit the same candidate or proposal artifact shape. After the EquationCandidate and SRAssertionProposal contract stabilizes, LLM-SR, KAN, and SNIP work can run in parallel.
