# Smart Home Privacy GAIA/HDT Bridge

## Purpose

This bridge establishes a first-class smart-home privacy domain pack for Ontogenesis and defines how it binds into GAIA and HolographMe/HDT without collapsing physical-world telemetry into a personal surveillance dossier.

The immediate source pattern is the smart-home privacy-policy study by Manandhar et al., which shows that policy availability, policy content, and policy coverage are all broken in different ways. The important architectural lesson is not that policies are messy. The lesson is that smart-home privacy must be evaluated by joining four evidence surfaces:

1. what the vendor claims in privacy policies and related documents;
2. what the vendor sells or integrates as device classes;
3. what the device class is capable of collecting, inferring, storing, transmitting, or actuating;
4. what the affected person, household, guest, child, worker, or institution has consented to permit.

This bridge makes Ontogenesis the canonical semantic source, GAIA the physical-context world model, and HDT the person-centered consent and impact model.

## Non-negotiable boundary

GAIA models the sensed world. HDT models the affected person. Ontogenesis defines the lawful ontology that lets both systems communicate without becoming a surveillance blob.

That boundary yields the following rule:

- GAIA may know that a camera is in a nursery and that the camera is capable of video and audio capture.
- HDT may know that the subject context is child-sensitive, that the household denies cloud retention by default, and that third-party sharing requires explicit consent.
- Ontogenesis owns the shared terms, claim grammar, coverage findings, evidence records, and validation rules.
- Policy Fabric or a downstream policy engine decides whether an observation, claim, or action is permitted across the membrane.

## Why this belongs in Ontogenesis first

The smart-home privacy problem cannot be solved by retrieval alone. Search can locate policies, app-store records, FAQs, law-enforcement guidelines, certification records, product catalogs, and endpoint evidence. But the decisive act is semantic: converting those materials into claims, device classes, data attributes, physical contexts, risk inferences, consent boundaries, and coverage findings.

Ontogenesis therefore owns:

- canonical smart-home privacy classes and properties;
- controlled device types and data attributes;
- physical context vocabulary for indoor/outdoor/private/child-sensitive spaces;
- claim types for collection, sharing, retention, transfer, and negative assertions;
- finding types such as no-policy, no-device-policy, broad collection, vague sharing, incomplete coverage, irrelevant template data, and context collapse;
- SHACL gates for minimum claim/evidence/finding integrity;
- bridge contracts for GAIA and HDT.

Downstream systems compile from Ontogenesis. They must not invent rival names for device types, policy findings, or consent boundaries.

## Domain model

The first module is:

`Domains/smart-home-privacy.ttl`

The first shape bundle is:

`shapes/smart-home-privacy.shacl.ttl`

The first registry supplement is:

`catalog/smart_home_privacy_registry.ttl`

### Core chain

```text
Vendor
  -> Product / Device
  -> DeviceType
  -> DeviceCapability
  -> DataAttribute
  -> PhysicalContext
  -> PrivacyClaim
  -> EvidenceRecord
  -> CoverageFinding
  -> RiskInference
  -> ConsentBoundary
```

### Required reasoning distinction

Policy text is not truth. Device capability is not behavior. Network metadata is not full content. User consent is not permanent permission.

The bridge preserves those distinctions as separate evidence classes so downstream systems can make bounded claims instead of overclaiming.

## GAIA binding

GAIA receives the physical side of the graph:

```text
Home
  -> Floor
  -> Room
  -> Zone
  -> Device
  -> Capability
  -> Observation
  -> DataAttribute
  -> Provenance
```

GAIA should model the world-state and physical context, including:

- device location;
- zone sensitivity;
- device class;
- sensor and actuator capability;
- observed event class;
- endpoint or integration evidence where available;
- spatial context such as indoor, outdoor, entryway, bedroom, nursery, bathroom, kitchen, or shared area.

GAIA must not treat all data attributes as equivalent. A video stream from a doorbell camera and a video stream from a baby monitor are the same abstract data attribute but not the same privacy situation. The difference is spatial, embodied, and contextual. GAIA is where that difference is modeled.

### GAIA examples

```text
DoorLock at Entryway
  emits LockStatus
  implies ScheduleInferenceRisk and OccupancyInferenceRisk

BabyMonitor at Nursery
  emits VideoStream and AudioStream
  implies ChildSurveillanceRisk

Thermostat at Bedroom
  emits TemperatureState and schedule-like use signals
  implies OccupancyInferenceRisk

WaterSensor at Basement
  emits WaterFlow
  may imply InsuranceRisk
```

## HDT / HolographMe binding

HDT receives the person-centered governance side of the graph:

```text
Person / Household / Role
  -> ConsentBoundary
  -> SensitivityTier
  -> RoutineInferenceRisk
  -> DelegatedAgentPermission
  -> RetentionPreference
  -> SharingBoundary
  -> ProjectionRule
```

HDT should not store raw home telemetry by default. It should store governed boundaries, preferences, roles, consent state, risk posture, and projection rules.

### HDT examples

```text
Child subject context
  -> high sensitivity
  -> cloud retention denied by default
  -> explicit guardian consent required for sharing

Household routine context
  -> schedule inference sensitive
  -> insurer/landlord/employer disclosure denied by default

Guest context
  -> notice and minimization required
  -> no biometric/profile extension without explicit consent
```

The result is a clean split:

- GAIA says: a device event occurred in physical context.
- HDT says: this event has bounded impact on a governed person or household.
- Policy Fabric says: this crossing is allowed, denied, quarantined, degraded, or requires review.

## Policy Coverage Compiler

The first executable downstream target should be a Policy Coverage Compiler.

Inputs:

- privacy policy text;
- vendor policy location and crawl path;
- vendor product catalog;
- device-type map;
- device capability map;
- physical context assumptions where available;
- HDT consent boundaries where local/user-specific use is involved.

Outputs:

- policy claims;
- evidence records;
- coverage findings;
- risk inferences;
- trust-label fields;
- procurement warnings;
- SourceOS enforcement hints;
- Sherlock-searchable claim/evidence indexes.

### Finding classes

The initial controlled findings reflect the Manandhar et al. findings and make them executable:

- `NoPolicyFinding`: vendor has no accessible privacy policy.
- `NoDevicePolicyFinding`: vendor has a web/app/account policy but no smart-home device policy.
- `PolicyPathObstructedFinding`: policy acquisition requires non-trivial hops, app execution, registration, broken-link workarounds, or unexpected downloads.
- `BroadCollectionFinding`: collection described through broad language such as usage data or sensor information without device/data precision.
- `VagueSharingFinding`: sharing described as PII/personal data without clear inclusion/exclusion of device telemetry.
- `IncompleteCoverageFinding`: policy covers only a subset of device types or data attributes implied by the catalog.
- `IrrelevantTemplateDataFinding`: policy mentions data attributes not supported by the vendor catalog, suggesting template residue or stale policy text.
- `ContextCollapseFinding`: policy treats similar data attributes as equal despite different physical contexts, such as doorbell video versus nursery video.

## Sherlock binding

Sherlock should index both documents and compiled claims.

Search surfaces:

- vendor;
- device type;
- data attribute;
- physical context;
- finding type;
- claim type;
- sharing destination;
- policy hash;
- crawl path;
- jurisdiction text;
- risk inference;
- consent boundary.

Target queries:

- show vendors with baby monitors whose policies omit audio/video claims;
- show policies that discuss personal data but not device data;
- show policies with unknown sharing destinations;
- show vendor claims contradicted by observed endpoints;
- show devices in child-sensitive contexts with vague retention terms;
- show policy paths that require app registration before purchase-time disclosure.

## SourceOS binding

SourceOS should act as the local observation and enforcement plane.

First local observations do not require invasive packet inspection. Useful evidence includes:

- mDNS/SSDP/Matter/Thread/Wi-Fi discovery metadata;
- device class and vendor strings;
- companion app identifiers;
- DNS and endpoint metadata where lawfully visible;
- firmware/update endpoints;
- cloud-contact timing;
- integration relationships with Alexa, Google, Home Assistant, IFTTT, SmartThings, HomeKit, or Matter ecosystems;
- policy-vs-observed drift.

`sourceos-syncd` should carry local-first evidence receipts and mesh state, not raw uncontrolled surveillance streams.

## ProCybernetica binding

ProCybernetica should own threat-model and adversarial governance packs for:

- insurer profiling;
- landlord surveillance;
- law-enforcement request ambiguity;
- child surveillance;
- hidden third-party sharing;
- template-policy laundering;
- post-cloud exfiltration beyond local network evidence;
- cross-device routine reconstruction;
- consent revocation failure.

## Sociosphere binding

Sociosphere should expose the public/private trust graph:

```text
/vendor/{vendor}/policy
/vendor/{vendor}/findings
/device/{device-type}/data-attributes
/context/{physical-context}/risks
/policy-gap/{finding-type}
/smart-home/privacy
```

Public surfaces should use evidence-tiering. Private local evidence from SourceOS must not be published unless the user explicitly chooses to contribute it.

## Policy Fabric binding

Policy Fabric should translate claims and risks into controls:

- allow;
- warn;
- require explicit consent;
- deny cloud retention;
- quarantine device;
- require local-only mode;
- suppress agent access;
- require procurement review;
- generate vendor disclosure notice.

Example decision:

```text
Input:
  device = BabyMonitor
  context = NurseryContext
  data = VideoStream + AudioStream
  policy finding = VagueSharingFinding
  HDT boundary = no cloud retention without guardian consent

Decision:
  allow local stream
  deny cloud retention
  require guardian consent for sharing
  raise high-sensitivity warning
  preserve evidence receipt
```

## Implementation order

### Tranche 1 — Ontogenesis domain pack

Status: started in this branch.

Deliverables:

- `Domains/smart-home-privacy.ttl`
- `shapes/smart-home-privacy.shacl.ttl`
- `catalog/smart_home_privacy_registry.ttl`
- bridge spec
- JSON-LD context and examples

### Tranche 2 — GAIA adapter

Add GAIA context mapping for:

- Home / room / zone / device;
- device capability;
- data attribute;
- physical context sensitivity;
- observation provenance;
- policy/evidence cross references.

### Tranche 3 — HDT adapter

Add HDT consent/impact mapping for:

- household role;
- child/guest/elder/worker context;
- consent scope;
- retention boundary;
- sharing boundary;
- delegated-agent access to home context.

### Tranche 4 — Sherlock compiled evidence index

Create claim/evidence index types and query affordances.

### Tranche 5 — SourceOS local observation receipts

Define local evidence receipts and drift checks, then keep user-private evidence private by default.

## Validation posture

Initial SHACL gates are intentionally minimal. They enforce:

- devices bind to vendors and device types;
- analyzed policy documents emit claims;
- claims preserve evidence;
- coverage findings preserve affected subject, finding type, and bounded confidence;
- evidence timestamps use `xsd:dateTime`.

Next SHACL tranche should add:

- high-sensitivity physical contexts require a consent boundary before downstream action;
- camera/baby-monitor device types imply video and possibly audio attributes unless explicitly disabled;
- negative collection claims require behavioral caveats when remote access or third-party integration is present;
- sharing claims require destination granularity or a finding is emitted;
- coverage completeness checks require vendor-device map lineage.

## Product outputs

This bridge unlocks three products:

1. **SocioProphet Home Trust Graph** — public/vendor/policy intelligence and evidence-tiered smart-home trust labels.
2. **SourceOS Home Trust Gateway** — local-first observation, receipts, and enforcement for user-owned connected environments.
3. **HDT Privacy Boundary Engine** — person-centered consent, projection, retention, and sharing controls for home-derived signals.

## Open questions

1. Should `SmartHomeDevice` ultimately live in GAIA with this module acting only as the privacy overlay, or should Ontogenesis retain the canonical device class and GAIA import it?
2. Should `ConsentBoundary` align directly to HolographMe consent-policy schemas, or should it remain a looser ontology class with JSON Schema projection downstream?
3. Should SourceOS publish anonymized endpoint/finding evidence into Sociosphere by default, or require explicit contribution per evidence bundle?
4. What is the first public vendor subset for the initial demo: cameras/baby monitors only, or a mixed set of top device classes?

## Decision

Proceed with Ontogenesis as the canonical semantic source. Bind GAIA for physical context. Bind HDT for personal consent and impact. Treat Sherlock, SourceOS, Sociosphere, ProCybernetica, and Policy Fabric as downstream consumers of the same ontology-backed claim/evidence model.
