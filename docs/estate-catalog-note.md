# Estate Catalog binding ontology (v0.1)

The estate binding vocabulary — the "language that binds the estate" so agents reason
over a graph instead of reading every repo. Ontogenesis epic #130.

## Not a new catalog — a binding layer
The estate already had the pieces, fragmented: `dom:Catalog`/`dom:Dataset`
(metadata), `drm:Dataset` (data-reference), `srm:Service` (service-reference),
`enrm:CriticalInfrastructure` (environment-reference), `legal:RepositoryAsset`
(org-legal), and the Model Plane `mp:InferenceProvider` (#129). This module does not
re-mint them — it **binds** them under `cat:EstateResource` and supplies the
cross-catalog object properties that are the reasoning fabric. It adds the one
genuinely-new catalog: **Model** (`cat:Model`/`cat:ModelAdapter`), joined to the
Model Plane by `cat:servedBy → mp:InferenceProvider` and `cat:modelDigest`.

## Three layers (dogfooding)
- **KBpedia/KKO** (`http://kbpedia.org/ontologies/kko#`, vendored in HellGraph) = the
  shared upper language. Estate terms align to it (`skos:closeMatch kko:…`) so estate
  and HellGraph share one binding language.
- **ontogenesis** (this module) = the estate binding **TBox** (vocabulary + SHACL).
- **prophet-core-catalog** = the **ABox / population** layer (Source/Dataset/App/Receipt
  manifests + per-repo extractors that read each repo's own README/docs). Its instances
  are typed by this vocabulary. Repo self-docs are the ingestion substrate.

## Reasoning fabric (object properties)
`cat:dependsOn` (root), `cat:runsOn`/`cat:deployedTo`/`cat:storedIn` (→ Infrastructure),
`cat:consumesData`/`cat:producesData` (→ Dataset), `cat:usesModel` (→ Model),
`cat:servedBy` (Model → InferenceProvider), `cat:exposes`, `cat:governedBy`. These make
blast-radius, where-does-it-run, and cross-plane questions graph traversals.

## Enforced (SHACL, verified both ways)
`cat:CatalogEntry` requires `catalogId` + `owner` + `status`∈{active,deprecated,retired};
`cat:Model` requires `modelDigest` (sha256) + SPDX `license` (MIT/Apache-only reasoned
over the graph). Range enforcement (runsOn→Infrastructure etc.) is expressed as
`rdfs:range` for reasoning, **not** as SHACL: the gate runs pyshacl `inference="rdfs"`,
which coerces a ranged object to the range type rather than rejecting it, so an
`sh:class` range check cannot fire. SHACL enforces what inference cannot mask.

## P3 — query surface + governed KKO alignment (this increment)
The agent-facing "reason, don't read" API, as spec-as-code:

- **Versioned SPARQL query surface** — `examples/queries/estate-catalog/*.rq`, each with
  a governed header (queryId, version, parameters, returns, access):
  `resolve-resource` (id → record + resource + owner/status),
  `by-catalog-family` (list a family, incl. bound fragments like `srm:Service`),
  `cross-catalog-lineage` (service → model → provider(+residency/escalation) → infra —
  the join the #130 governance questions are asked over),
  `blast-radius` (transitive `cat:dependsOn+` — "if this breaks, what breaks"),
  `license-compliance` (MIT/Apache-only reasoned over the graph).
- **Runnable test with teeth both ways** — `scripts/validate_estate_catalog_queries.py`
  runs every query against the TBox + a tiny ABox fixture
  (`tests/estate-catalog/mini-estate.ttl`) and asserts the **exact** rows, so a query
  that drops a real dependent or sweeps in a wrong one both fail. Two checks are
  deliberately negative (a leaf has an empty blast radius; the Apache model is absent
  from the licence result). Wired into `make validate`
  (`validate-estate-catalog-queries`).
- **Governed `Alignments/kko.ttl`** — the inline `skos:closeMatch kko:…` grounding
  carried by the TBox, promoted to reviewable `smap:MappingAssertion` records (same
  convention as `Alignments/fibo.ttl`), pinned to the estate's sovereign KBpedia fork
  (byte-identical to HellGraph's vendored `kko-2.10.n3`). The same validator checks the
  alignment **resolves**: every cat: class that grounds into KKO has a matching governed
  assertion (and vice versa — no orphans), each `mapsFrom` resolves to a declared TBox
  class, each `mapsTo` is a KKO IRI. KKO is CC-BY-4.0 — this asserts alignments only and
  vendors no KKO content.

## Not in scope (later increments of #130)
Deeper per-catalog modelling; wiring the query surface into the Lattice
`oq:ShapeQuery`/FederatedQueryPlane envelope; running these queries over the **real**
prophet-core-catalog estate graph (P2/P3 population, already live there) in CI rather
than the illustrative fixture; and full KBpedia (not just KKO-upper) alignment.
