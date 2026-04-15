# Diagrams

These diagrams are narrative entry points into ontogenesis as a framework for ontology genesis, linking, policy-aware evidence flow, and application-specific bindings.

## Agentic Flow Architecture
- Maps: Intent → Context → Agent Identity → Policy → Evidence
- Read this as a generic scaffold for ontology-mediated interaction, not as a claim that every deployment has the same subject, substrate, or boundary conditions.
- Ontogenesis tie-ins:
  - `ontogenesis.ttl`: core classes and lifecycle semantics
  - `shapes/ontogenesis.shacl.ttl`: constraints (what *must* be present)
  - `context.jsonld`: JSON-LD surface for emitted evidence
  - `mappings/*.ttl`: boundary mappings into external semantic systems

## Agentic Flow Architecture — Human Interface Example
- This diagram is one application-specific framing, not the full scope of ontogenesis.
- In the Human Digital Twin use case, the human subject is the moral + authorization anchor.
- Memory and Cognition are typed subsystems rather than hand-wavy metaphors:
  - Memory = retrieval + provenance + access control
  - Cognition = planning over Intent DAG under policy gates
- This framing is useful for modeling human-facing measurements, wearables, embodied observations, consent-bound exports, and bounded digital representation.

## Layered Mapping Interpretation
- Lower-layer bindings connect local observations, sensors, devices, and immediate state representations into graph structure.
- Middle-layer bindings connect claims, workflows, policies, evaluations, and interactions between agents and environments.
- Upper-layer bindings connect local and middle structures to broader world models, reference ontologies, and shared semantic anchors.

## Asset provenance
Images provided by user via chat; treat as documentation assets.
