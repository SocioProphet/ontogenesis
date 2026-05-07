# SCOPE-D Security Tool Ontology Alignment

## Purpose

This specification defines how SCOPE-D security-tool catalog records, including BlackArch-derived metadata, should be represented in Ontogenesis.

BlackArch remains source material only. Ontogenesis owns the durable semantic model: classes, properties, SHACL constraints, provenance rules, and promotion gates for security-tool capability governance.

## Source boundary

The BlackArch archive is cannibalized for:

- package/category metadata;
- package provenance fields;
- dependency and source references;
- category-to-capability hints;
- safe synthetic exercise seeds;
- image/profile composition lessons.

It is not a runtime authority. A catalog record does not authorize installation, execution, live target interaction, or production use.

## Alignment with SCOPE-D

SCOPE-D owns operational artifacts:

- `config/schemas/security-tool.schema.json`
- `config/schemas/blackarch-catalog.schema.json`
- `config/mappings/blackarch-category-capability-map.yaml`
- `tools/blackarch_readonly_miner.py`
- `tools/validate_blackarch_catalog.py`
- `exercises/blackarch/**`

Ontogenesis should own semantic permanence and validation:

- ontology classes;
- controlled value sets;
- JSON-LD context mapping;
- SHACL constraints;
- promotion gates;
- registry metadata;
- provenance and audit relationships.

## Proposed module placement

Recommended module path:

```text
Domains/security-tools/
  security-tools.ttl
  security-tools.context.jsonld
  security-tools.examples.jsonld
shapes/security-tools.shacl.ttl
```

If a broader cybersecurity domain module already exists later, this module can be merged or imported into it.

## Core classes

### SecurityTool

A tool or package candidate from a source corpus.

Required relationships:

- hasSourceCorpus
- hasProvenance
- hasSafetyClass
- hasExecutionMode
- hasEvidenceContract

### SecurityCapability

A normalized capability class used by SCOPE-D and SourceOS lab channels.

Initial values:

- DefensiveHostAssessment
- CodeAudit
- ForensicAnalysis
- AuthorizedScanning
- WebApplicationValidation
- NetworkAnalysis
- ReverseEngineering
- FuzzValidation
- WirelessLab
- RadioLab
- NFCLab
- BluetoothLab
- MobileLab
- HardwareLab
- VehicleSecurityLab
- DroneSecurityLab
- AIInfraAssessment
- RestrictedTaxonomy
- ThreatModeling
- UnknownCapability

### SafetyClass

Safety posture for a security tool record.

Allowed values:

- AllowDefensive
- LabGated
- RestrictedCatalogOnly
- BlockedRuntime
- UnknownReviewRequired

### ExecutionMode

Descriptive execution state. These values do not grant authority.

Allowed values:

- CatalogOnly
- SyntheticOnly
- ReadOnly
- SandboxedLab
- Blocked

### ToolRiskSignal

Risk indicators used for policy decisions.

Initial properties:

- requiresNetwork
- requiresRoot
- requiresRawSocket
- requiresCaptureDevice
- mayMutateTarget
- mayHandleSecrets
- mayContactExternalServices
- physicalDomain

### ToolEvidenceContract

Expected evidence produced by a tool wrapper or synthetic fixture.

Allowed evidence types:

- MetadataOnly
- SyntheticObservable
- ScanSummary
- FindingObservable
- DetectionExpectation
- PcapSummary
- FileMetadata
- HashObservable
- ProcessObservable
- NetworkObservable
- PolicyDecision
- RunReceipt

### PackageProvenance

Package-level source metadata.

Properties:

- sourceRef
- upstreamUrl
- packagePath
- observedAt
- sourceCommit
- sourceSha256
- claimLevel

### SecurityLabChannel

A SourceOS/SociOS channel candidate derived from classified tools.

Initial channel concepts:

- SourceOSSecCore
- SourceOSSecCodeAudit
- SourceOSSecForensics
- SourceOSSecWebLab
- SourceOSSecNetworkLab
- SourceOSSecReverseLab
- SourceOSSecFuzzLab
- SourceOSSecPhysicalLab

## Required invariants

SHACL gates should enforce:

1. Every `SecurityTool` has exactly one `SafetyClass`.
2. Every `SecurityTool` has at least one `ExecutionMode`.
3. Every `SecurityTool` has `productionAllowed false` unless a future explicit promotion process exists.
4. Every `SecurityTool` has `wrapperRequired true` before any execution mode beyond `CatalogOnly` or `SyntheticOnly`.
5. `RestrictedCatalogOnly`, `BlockedRuntime`, and `UnknownReviewRequired` cannot default to `ReadOnly` or `SandboxedLab`.
6. Physical-domain tools require `physicalDomain true` and a physical-domain gate.
7. Records with `rawOutputAllowed true` cannot be promoted from miner output.
8. Generated catalog records must retain source corpus provenance.
9. Package-level license metadata must be represented as unknown when not reliably extracted.
10. A catalog import must not be modeled as a runtime allow-list.

## JSON-LD alignment

The SCOPE-D JSON records should map to JSON-LD without changing their operational schema.

Suggested context aliases:

```json
{
  "toolId": "st:toolId",
  "sourceCorpus": "st:sourceCorpus",
  "categories": "st:category",
  "capabilities": "st:capability",
  "safety": "st:safety",
  "execution": "st:execution",
  "evidence": "st:evidenceContract",
  "provenance": "prov:wasDerivedFrom"
}
```

## Promotion gates

Catalog import is the lowest maturity state.

Recommended maturity states:

1. `cataloged` — metadata exists.
2. `classified` — safety class and execution mode assigned.
3. `validated` — schema and SHACL gates pass.
4. `fixture_backed` — synthetic SCOPE-D exercise exists.
5. `wrapper_specified` — wrapper contract exists.
6. `lab_candidate` — SourceOS lab-channel candidate only.
7. `lab_approved` — policy-gated lab use approved.
8. `deprecated` — retained for provenance and mapping only.

No maturity state in this spec grants production runtime authority.

## Downstream consumers

Ontogenesis output should feed:

- SCOPE-D control-loop validation;
- SocioSphere posture dashboards;
- Sherlock search over tool/capability/evidence graphs;
- SourceOS lab-channel planning;
- policy-fabric gates for security-tool promotion.

## Non-goals

This ontology must not:

- import executable tools;
- define package installation flows;
- authorize live target interaction;
- weaken SCOPE-D safety defaults;
- hide unknown license or provenance state;
- convert BlackArch into a SocioProphet-maintained distribution.

## Tranche 2 acceptance criteria

- Add this specification.
- Add a TTL module for the core classes and controlled individuals.
- Add SHACL gates for safety invariants.
- Add one JSON-LD example converted from a SCOPE-D smoke catalog record.
- Register the module in Ontogenesis registry only after local validation passes.
