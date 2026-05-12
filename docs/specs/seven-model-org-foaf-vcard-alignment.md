# Seven-Model Civic Stack × ORG/FOAF/vCard Alignment

Status: draft

Tracking issue: SocioProphet/ontogenesis#80

## Purpose

This specification defines the first governed Ontogenesis tranche for the Seven-Model Civic Operating Architecture. It aligns the whole-of-society reference stack with W3C ORG, FOAF, vCard, PROV-O, TIME, GeoSPARQL, DCAT, and SOSA without surrendering Ontogenesis-local semantic control.

The intent is to make people, organizations, posts, memberships, services, datasets, policies, sites, observations, attestations, and change events auditable in one evidence-ready graph.

## Reference model stack

The civic stack extends enterprise architecture into a multi-scale civic operating model:

| Model | Role |
| --- | --- |
| EnRM | Environmental constraints, exposures, hazards, resource stocks, externalities, and critical infrastructure. |
| CGRM | Civic-governance semantics: jurisdictions, authorities, rights, obligations, policies, permits, sanctions, and lawful bases. |
| PRM+ | Public-value outcomes, performance targets, observations, indicators, equity, resilience, and environmental cost. |
| BRM+ | Actors, value networks, capabilities, processes, value flows, and externality flows. |
| SRM+ | Service components, interfaces, SLAs, lifecycle stages, dependencies, and policy guards. |
| DRM+ | Datasets, records, identifiers, provenance, consent, access basis, and quality metrics. |
| TRM+ | Runtime, workload, trust anchor, attestation, edge node, and observability signal semantics. |

Ontogenesis owns the canonical vocabulary and alignment artifacts. SocioSphere, Delivery Excellence, Gaia, PolicyFabric, AgentPlane, ProCybernetica, HellGraph, Regis, and Prophet Core consume the compiled meanings.

## Alignment rule

External vocabularies are bridge targets, not uncontrolled replacements for Ontogenesis-local terms. The alignment uses mapping assertions and close-match semantics unless exact equivalence is proven.

The minimum external bridge vocabulary set is:

- W3C ORG for organization, unit, collaboration, post, membership, role, site, and change event.
- FOAF for agent/person compatibility.
- vCard for address/contact compatibility.
- PROV-O for attribution, generation, association, and evidence lineage.
- TIME for temporal anchoring.
- GeoSPARQL for site geometry.
- DCAT for dataset publication.
- SOSA for observations and measurements.

## Accountability spine

The first tranche must support this trace:

human/person → membership → role/post → organization/unit → authority/policy → service → dataset → runtime → attestation → observation → public-value score → environmental externality

This trace is the minimum audit chain SocioSphere and Delivery Excellence should be able to project onto governance boards.

## Role, membership, and post distinction

`org:Membership`, `org:Role`, and `org:Post` remain distinct.

- Membership binds an agent to an organization with a role.
- Role names responsibility semantics.
- Post represents an office that can hold authority independently of the current incumbent.

Ontogenesis-local `party:RoleAssignment` is therefore a close operational bridge to ORG membership semantics, not automatically an exact equivalent.

## Civic stack bridge terms

The first tranche introduces a lightweight `cstack:` namespace for bridge terms used before the full EnRM/CGRM/PRM+/SRM+/DRM+/TRM+ domain modules land.

These bridge terms are transitional and should be superseded or refined by later domain modules:

- `cstack:RegulatedService`
- `cstack:RegulatedDataset`
- `cstack:ServiceEvent`
- `cstack:PerformanceObservation`
- `cstack:EnvironmentalExposure`
- `cstack:AttestationEvent`
- `cstack:hasResponsiblePost`
- `cstack:hasLegalBasis`
- `cstack:hasAccessBasis`
- `cstack:hasExternalityVector`
- `cstack:hasEvidenceRef`

## SHACL gate intent

The first SHACL bundle should enforce only the minimum safety rail:

1. Membership must identify one member, one organization, and at least one role.
2. Sites must carry geometry or an address.
3. Regulated services must cite legal basis.
4. Regulated datasets must cite provenance and access basis.
5. Attestation events must cite time, target, and signature/evidence.
6. Change events must cite time and associated agent.

These are guardrails for traceability, not a complete civic policy engine.

## Downstream projection

- SocioSphere consumes the governed object model.
- Delivery Excellence consumes PRM+ score and evidence fields.
- Gaia supplies EnRM facts and externality vectors.
- PolicyFabric evaluates CGRM rules.
- AgentPlane emits runtime evidence.
- ProCybernetica supplies control, incident, and evidence-pack overlays.
- HellGraph stores and queries the combined graph.
- Regis materializes registry entities and relations.

## Non-goals

This tranche does not implement the full domain modules for EnRM, CGRM, PRM+, SRM+, DRM+, and TRM+. Those are tracked separately and should build on this alignment spine.
