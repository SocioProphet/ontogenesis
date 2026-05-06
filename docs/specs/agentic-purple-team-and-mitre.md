# Agentic Purple Team Ontology and MITRE Alignment

Status: draft 0.1.0

## Purpose

This specification defines how Ontogenesis represents agentic purple-team actions and how those actions align to MITRE ATT&CK, MITRE ATLAS, and SourceOS/SCOPE-D local technique equivalents.

The goal is to support SCOPE-D, PolicyFabric, AgentPlane, SocioSphere, and related security-control loops with ontology-native semantics for:

- governed purple-team loops;
- agentic security actions;
- evidence envelopes;
- safety boundaries and control gates;
- atomic validation;
- countermeasure generation;
- threat-intel ingestion;
- AI infrastructure and MCP/tool risk;
- graph robustness;
- run receipts and tamper-evident summaries;
- ATT&CK/ATLAS/local technique mappings.

## Modules

- `Domains/agentic-purple-team.ttl` defines the local SocioProphet / SourceOS ontology for agentic purple-team loops and actions.
- `Alignments/mitre-attack.ttl` defines a governed alignment scaffold for MITRE ATT&CK and ATLAS. It does not vendor the full MITRE STIX corpus.
- `shapes/agentic-purple-team.shacl.ttl` defines promotion gates for core run, action, atomic testcase, and technique semantics.
- `examples/agentic-purple-team-scope-d-run.ttl` demonstrates a SCOPE-D synthetic run graph.

## Import policy

Ontogenesis should use a map-not-vendor-by-default posture for MITRE ATT&CK and ATLAS.

There are three allowed lanes:

1. **Alignment scaffold** — curated local classes and seed individuals for stable references. This is what `Alignments/mitre-attack.ttl` provides now.
2. **Generated import lane** — future generated module built from official MITRE STIX/TAXII releases, with source version, retrieval timestamp, hash, license notice, and provenance receipt.
3. **SourceOS local equivalent ontology** — local techniques for AI agents, MCP tools, memory boundaries, capability overreach, graph poisoning, and SourceOS-specific execution surfaces where MITRE coverage is incomplete or evolving.

## Why not vendor ATT&CK wholesale by default

Full ATT&CK import is useful for coverage, but uncontrolled vendoring creates governance and maintenance problems:

- version drift;
- license/provenance ambiguity;
- noisy ontology surface;
- brittle downstream references;
- poor alignment to agentic/AI/MCP-specific concepts;
- weak release reproducibility unless the import is deterministic.

Therefore the default is curated alignment plus a future deterministic import tool.

## Local equivalent techniques

The MITRE alignment module seeds SourceOS-local equivalents for concepts that matter to SCOPE-D and agentic runtime safety:

- `SOCIO-TOOL-POISONING`
- `SOCIO-PROMPT-INJECTION`
- `SOCIO-MEMORY-BOUNDARY-BYPASS`
- `SOCIO-CAPABILITY-OVERREACH`

These can map to MITRE ATT&CK, ATLAS, OWASP LLM Top 10, MCP-specific taxonomies, and internal SourceOS safety policy classes over time.

## Required action semantics

Every governed agentic purple-team action should declare:

- action class;
- safety mode;
- evidence product, when applicable;
- required gate, when applicable;
- technique mapping, when applicable;
- receipt or summary relationship for run-level artifacts.

## Required run semantics

Every SCOPE-D / SourceOS purple-team control-loop run should be representable as:

- `apt:ControlLoopRun`
- one or more `apt:AgenticPurpleTeamAction` instances;
- at least one `apt:SafetyBoundary`;
- one or more `apt:EvidenceEnvelope` instances;
- one `apt:RunReceipt`;
- optionally one `apt:RunSummary` for SocioSphere / PolicyFabric handoff.

## SHACL gates

The initial SHACL gate requires:

- `ControlLoopRun` has a `scope-d-*` run ID;
- `ControlLoopRun` references a `SafetyBoundary`;
- `ControlLoopRun` references a `RunReceipt`;
- `AgenticPurpleTeamAction` declares action class and safety mode;
- `AtomicTestCase` maps to at least one technique and remains synthetic/read-only/dry-run in examples;
- `Technique` has a technique ID.

## Future import pipeline

A future importer should:

1. fetch official MITRE ATT&CK STIX/TAXII bundles;
2. pin source version and retrieval timestamp;
3. compute source artifact hash;
4. transform tactics, techniques, mitigations, data sources, and detections into Ontogenesis local terms;
5. emit a generated TTL module under a generated namespace;
6. emit provenance and ledger records;
7. run SHACL validation;
8. update registry metadata only after validation passes.

## SCOPE-D integration

SCOPE-D JSON contracts should map into this ontology as follows:

| SCOPE-D contract | Ontogenesis class |
|---|---|
| `ControlLoopRun` | `apt:ControlLoopRun` |
| `SafetyBoundary` | `apt:SafetyBoundary` |
| `ControlGate` | `apt:ControlGate` |
| `EvidenceEnvelope` | `apt:EvidenceEnvelope` |
| `AtomicTestCase` | `apt:AtomicTestCase` |
| `EmulationPlan` | `apt:EmulationPlan` |
| `CountermeasureRule` | `apt:CountermeasureRule` |
| `ThreatIntelFeed` | `apt:ThreatIntelFeed` |
| `IndicatorRecord` | `apt:IndicatorRecord` |
| `AttackPathGraph` | `apt:AttackPathGraph` |
| `GraphRobustnessAssessment` | `apt:GraphRobustnessAssessment` |
| `AIInfraAssessment` | `apt:AIInfraAssessment` |
| `MCPToolRisk` | `apt:MCPToolRisk` |
| `AgentSkillRisk` | `apt:AgentSkillRisk` |
| `RunReceipt` | `apt:RunReceipt` |
| `RunSummary` | `apt:RunSummary` |

## Non-goals

- No uncontrolled vendoring of ATT&CK.
- No import of offensive payloads or C2 code.
- No modeling of destructive action as executable authorization.
- No persistent memory semantics without explicit tenant scope and redaction gates.
