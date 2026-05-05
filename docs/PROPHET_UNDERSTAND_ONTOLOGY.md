# Prophet Understand Ontology

## Purpose

Ontogenesis is the normative ontology and validation home for Prophet Understand / Repo Intelligence v0.

The platform artifact is `prophet-understanding.v0`. Smart Tree emits it, Lampstand indexes it, Sherlock searches it, AgentPlane consumes it for work orders, Policy Fabric gates it, and Delivery Excellence measures it.

## Core classes

- `RepoArtifact`: the complete graph artifact for one repository at one commit.
- `RepoNode`: a typed entity in the repository graph.
- `RepoEdge`: a typed relationship between two nodes.
- `SourceAnchor`: a repo-relative path and line range with content hash.
- `ProvenanceReceipt`: evidence describing how a graph claim was produced.
- `ValidationResult`: a machine-readable validation outcome.
- `PolicyStatus`: policy state and policy checks over the artifact.
- `GuidedTour`: ordered graph explanation for onboarding, architecture, dependency, policy, or PR impact flows.
- `DiffImpactSet`: changed paths mapped to affected nodes, edges, tests, docs, and policies.

## Minimum node taxonomy

`repo`, `directory`, `file`, `module`, `package`, `service`, `endpoint`, `schema`, `contract`, `document`, `workflow`, `test`, `config`, `runtime`, `policy`, `domain`, `concept`, `validator`.

## Minimum edge taxonomy

`contains`, `imports`, `depends_on`, `defines`, `documents`, `tests`, `configures`, `calls`, `owns`, `generates`, `validates`, `governed_by`, `impacted_by`, `related_to`.

## URI shape

Recommended URI forms:

```text
repo://<owner>/<repo>#<commit>
repo-node://<owner>/<repo>/<node-kind>/<repo-relative-path-or-symbol>#<commit>
repo-edge://<owner>/<repo>/<edge-kind>/<source-id>/<target-id>#<commit>
repo-receipt://<owner>/<repo>/<receipt-id>#<commit>
```

IDs inside JSON artifacts remain compact stable IDs. Ontogenesis mappings should expand them to URI form when publishing JSON-LD, RDF, SHACL, or TriTRPC-compatible contracts.

## Validation constraints

Required constraints:

- every node has stable `id`, `kind`, `label`, `confidence`, metadata, and provenance receipt references
- every non-repo and non-directory factual node has a `SourceAnchor` unless explicitly marked inferred
- every edge references existing source and target nodes
- every edge has provenance receipt references
- every policy check references evidence receipts
- every diff impact set references existing affected nodes and edges
- every guided tour step references existing nodes and optionally existing edges
- every validation result references a known target or the artifact itself

## Provenance stance

Plain-English summaries are derived claims, not primary evidence. They must reference provenance receipts. Inferred claims must carry lower confidence and cannot become mutation authority.

## SHACL-style gates

The first SHACL-style gates should cover:

- `RepoNodeRequiresProvenance`
- `RepoEdgeRequiresEndpoints`
- `FactualNodeRequiresSourceAnchor`
- `PolicyCheckRequiresEvidence`
- `DiffImpactReferencesExistingGraphFacts`
- `TourReferencesExistingGraphFacts`
- `StableIdShape`

## Non-goals

Ontogenesis must not depend on a single parser implementation. It defines the semantic contract. Smart Tree and future scanners implement producers.
