# Symbolic Regression Vocabulary Draft

Status: v0.1 Ontogenesis vocabulary draft.

This document records the Ontogenesis side of PROMETHEUS / symbolic-regression law discovery. Ontogenesis owns vocabulary draft and SHACL semantics. It does not own runtime execution, agent replay, policy admission, memory promotion, or canonical sourceos-spec schema promotion.

WebProtege is optional. It may be one semantic review surface, but it is not required by the contract.

## Position

Symbolic-regression output is candidate material until reviewed.

Equation candidates and program candidates may become `SRAssertionProposal` instances. They do not become admitted `SRAssertion` instances until evidence replay, semantic validation, and governance have occurred.

The safe flow is:

EquationCandidate or ProgramCandidate becomes SRAssertionProposal. The proposal carries dataset evidence, feature set, operator library, fit metric, complexity metric, dimensional analysis, discovery method, replay reference, promotion status, admission state, and a non-authority declaration. A configured semantic review surface may then display or edit the proposal. Only an admitted proposal becomes an SRAssertion.

## Dimensional analysis is first-class

Dimensional analysis is not a minor validation note. It is a gate.

Every equation candidate should carry a `DimensionalAnalysisResult` with `unitsStatus` equal to one of: consistent, inconsistent, unknown, or unchecked.

An inconsistent candidate may be stored as failure corpus because it is useful for search and curriculum. It must not be promoted beyond candidate status. It must not become proposed or admitted. It must not be treated as a law, ontology assertion, policy, or controller regardless of fit score.

Unknown and unchecked are allowed as draft states, but they should prevent automatic admission.

## Optional semantic review surface

The vocabulary uses `SemanticReviewSurface` rather than making WebProtege mandatory.

Allowed review surface types are: git_pr, prophet_platform_ui, cli, sparql_editor, automated_shacl_gate, and webprotege.

The property `webProtegeProjectRef` is optional and should only appear when a deployment uses WebProtege.

## Core classes

`EquationCandidate` is a symbolic-regression equation output before semantic, evidence, policy, or runtime admission.

`ProgramCandidate` is a generated program or function candidate from program-search or LLM-SR-style methods.

`SRAssertionProposal` is the review object emitted by PROMETHEUS after evidence and metrics are attached.

`SRAssertion` is an admitted assertion after review. This draft defines the term for continuity, but does not promote any proposal to admitted status.

`DimensionalAnalysisResult` records units and dimensional status.

`DatasetEvidenceRef`, `FeatureSetRef`, `OperatorLibraryRef`, `FitMetric`, `ComplexityMetric`, `DiscoveryMethodRef`, and `EvidenceReplayRef` carry the supporting structure.

## Required proposal posture

An SRAssertionProposal must include dataset evidence, fit metric, complexity metric, dimensional analysis, evidence replay, discovery method, promotion status, admission state, and a non-authority declaration.

A proposal with `unitsStatus` set to inconsistent must be blocked from proposed or admitted status by SHACL.

## Authority boundary

Ontogenesis defines this draft vocabulary and SHACL shape.

AgentPlane should own evidence and replay schemas.

SocioSphere owns cross-repo rollout and CHRONOS carrier registration.

SourceOS-spec may later receive canonical schemas after this draft stabilizes.

Policy fabric owns admission to policy or controller use.

Memory-mesh owns symbolic-numeric memory and retrieval only after carrier boundaries are observed.

## Implementation notes

This tranche intentionally avoids implementation code and model/tool installation. PySR, SINDy, KAN, LLM-SR, TPSR, and SNIP should all emit the same candidate or proposal artifact shape. After the EquationCandidate and SRAssertionProposal contract stabilizes, LLM-SR, KAN, and SNIP work can run in parallel.
