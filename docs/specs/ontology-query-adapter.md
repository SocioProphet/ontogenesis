# Ontology-Query Adapter — Contract Specification

**Version:** 0.1.0  
**Status:** draft  
**Location:** `Platform/lattice-ontology-query.ttl`, `shapes/ontology-query.shacl.ttl`

---

## 1. Purpose and Scope

This document defines the **ontology-query adapter contract** for
Ontogenesis and the Lattice FederatedQueryPlane.

Lattice treats `ontology-query` as a **distinct query plane** from `sparql`.
The distinction is intentional and governance-critical:

| Plane | Language | What it evaluates | Reasoner required |
|---|---|---|---|
| `sparql` | SPARQL 1.1 | Triple-pattern matching over a named graph | No |
| `ontology-query` | OWL / SHACL | Class hierarchies, shapes, constraints, schema alignment, inferred triples | Yes (OWL2-RL, RDFS, or SHACL-AF) |

Because ontology-query involves reasoning, SHACL shape evaluation, schema
alignment, and constraint checking, it carries **explicit governance
requirements** beyond what a triple-pattern query needs: policy authorisation,
catalog-scope resolution, and replayable evidence trails.

---

## 2. Namespace

| Prefix | IRI |
|---|---|
| `oq:` | `https://socioprophet.github.io/ontogenesis/platform/oq#` |

Source file: `Platform/lattice-ontology-query.ttl`

---

## 3. Query Types

All query types are subclasses of `oq:OntologyQuery` and inherit the
**request envelope** defined in §4.

### 3.1 `oq:ClassQuery`

Queries OWL class membership, subclass hierarchies, or equivalent-class
relations within a governed ontology scope.

Required additional field: `oq:targetClass` (exactly 1).

### 3.2 `oq:ShapeQuery`

Queries SHACL shape applicability: which NodeShapes or PropertyShapes target
a given class or individual node, and whether those shapes are satisfied.

Required additional field: at least one of `oq:targetShape` or
`oq:targetNode`.

### 3.3 `oq:ConstraintQuery`

Queries for active SHACL constraint violations or constraint-check results
within the resolved catalog scope.

No additional required fields beyond the request envelope; the reasoner
runs over the full catalog scope.

### 3.4 `oq:SchemaAlignmentQuery`

Queries cross-schema or cross-ontology alignment mappings, including
equivalent properties and class-bridge assertions between two ontology
modules.

Required additional fields: `oq:sourceSchema` (exactly 1),
`oq:targetSchema` (exactly 1).

### 3.5 `oq:ReasoningResultQuery`

Queries the outcome of a reasoner run: inferred triples, class
subsumptions, or property entailments over the catalog scope.

Required additional field: `oq:reasonerProfile` (e.g. `"OWL2-RL"`,
`"RDFS"`, `"SHACL-AF"`).

---

## 4. Request Envelope

Every `oq:OntologyQuery` (and all subtypes) must carry:

| Property | Range | Description |
|---|---|---|
| `oq:queryId` | `xsd:string` | Unique, stable identifier (e.g. UUID) |
| `oq:queryVersion` | `xsd:string` | SemVer of the adapter contract used |
| `oq:catalogScope` | `upper:InformationArtifact` | Restricts reasoning to a catalog, module, or named graph |
| `oq:requestingAgent` | `upper:Agent` | The agent (system or human) submitting the query |
| `oq:governedByPolicy` | `upper:Policy` | The governance policy that authorises this query |
| `oq:isDryRun` | `xsd:boolean` | When `true`, validates without executing the reasoner (see §6) |

---

## 5. Response Envelope

Every `oq:OntologyQueryResponse` must carry:

| Property | Range | Description |
|---|---|---|
| `oq:responseId` | `xsd:string` | Unique response identifier |
| `oq:respondingTo` | `oq:OntologyQuery` | Links back to the originating query |
| `oq:resultStatus` | `xsd:string` | One of: `ok`, `error`, `dry-run-pass`, `dry-run-fail` |
| `oq:resultPayload` | `xsd:string` | Serialised result (JSON-LD fragment, Turtle, or SHACL report IRI); **empty on dry-run** |
| `oq:errorMessage` | `xsd:string` | Human-readable error (present when `resultStatus` is `error` or `dry-run-fail`) |
| `oq:hasEvidence` | `oq:QueryEvidence` | One or more evidence records for audit and replay |

---

## 6. Dry-Run Route Behaviour

When `oq:isDryRun` is `true`:

1. The adapter resolves `oq:catalogScope` and verifies the catalog is
   accessible.
2. The adapter evaluates `oq:governedByPolicy` to determine whether the
   requesting agent is authorised to issue this query type.
3. **The reasoner or SHACL engine is NOT invoked.**
4. `oq:resultPayload` is empty.
5. The response is either:
   - `oq:DryRunPassResponse` with `resultStatus "dry-run-pass"` if both
     checks succeed.
   - `oq:DryRunFailResponse` with `resultStatus "dry-run-fail"` plus an
     `oq:errorMessage` if either check fails.
6. At least one `oq:QueryEvidence` record with
   `oq:evidenceKind "dry-run-check"` must be attached.

---

## 7. Evidence Fields (Sherlock / Sociosphere)

Each `oq:QueryEvidence` instance provides a single governance step or
decision record for audit and replay by the Sherlock diagnostics engine and
Sociosphere governance layer.

| Property | Range | Allowed values | Description |
|---|---|---|---|
| `oq:evidenceKind` | `xsd:string` | `policy-check`, `catalog-check`, `reasoning-trace`, `dry-run-check` | Category of evidence |
| `oq:evidenceTimestamp` | `xsd:dateTime` | ISO-8601 UTC | When the evidence was created |
| `oq:evidenceSource` | `xsd:string` | — | Component ID that produced this evidence |
| `oq:evidenceText` | `xsd:string` | — | Human-readable decision or finding |
| `oq:policyDecision` | `xsd:string` | `allow`, `deny`, `conditional` | Authorisation outcome |

---

## 8. Lattice FederatedQueryPlane Binding

An `oq:LatticeQueryPlaneBinding` instance declares how the adapter
maps to the Lattice FederatedQueryPlane routing layer:

```turtle
oq:MyBinding a oq:LatticeQueryPlaneBinding ;
  oq:latticeQueryLanguage "ontology-query" ;   # MUST be this exact string
  oq:distinguishedFrom     "sparql" ;           # explicit non-SPARQL marker
  oq:bindsQuery            oq:MyQuery .
```

The `oq:latticeQueryLanguage "ontology-query"` value is the canonical
discriminator used by the FederatedQueryPlane router to select this adapter
over the SPARQL plane.

---

## 9. SHACL Shapes

SHACL shapes for all types are in `shapes/ontology-query.shacl.ttl`.
The shapes enforce:

- All request-envelope required fields (`oq:OntologyQueryShape`)
- Per-type additional required fields (`oq:ClassQueryShape`, etc.)
- Response envelope including `resultStatus` value constraint
- Dry-run response constraints (evidence required, correct status)
- Evidence record constraints
- Lattice binding constraints (`latticeQueryLanguage` and
  `distinguishedFrom` values pinned)

---

## 10. Example Fixtures

`examples/ontology-query-demo.ttl` contains one valid instance of each
query type plus a dry-run pass example and the Lattice binding declaration.

---

## 11. Conformance Tests

`tests/ontology-query-integrity.rq` — SPARQL invariant (must return 0 rows):

> Every `oq:OntologyQueryResponse` must link back to an originating
> `oq:OntologyQuery` via `oq:respondingTo`. Responses without this link
> violate the adapter contract.

Run with: `make validate` (or `make venv && make deps && make validate`).

---

## 12. Governance Notes

- **ontology-query ≠ SPARQL**: the two planes differ in what they evaluate,
  which engine they invoke, and the governance they require.
- Dry-run is a first-class operation to support policy pre-flight without
  triggering expensive reasoner calls.
- All query responses carry replayable evidence trails; these are required
  fields, not optional annotations.
- The `oq:catalogScope` field is mandatory to prevent unbounded cross-graph
  reasoning without explicit governance sign-off.
