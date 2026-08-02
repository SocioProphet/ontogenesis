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

## Not in scope (later increments of #130)
Deeper per-catalog modelling; a governed `Alignments/kko.ttl` of `smap:MappingAssertion`
records; population (prophet-core-catalog extractors → typed instances); and the P3
SPARQL/ShapeQuery agent surface (a real cross-catalog query over real instances = the
"live" proof).
