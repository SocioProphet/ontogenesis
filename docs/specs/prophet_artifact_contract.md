# Prophet computational artifact contract

This tranche adds Ontogenesis-native semantics for `ProphetArtifact` records:

- ontology module: `prophet/prophet_artifact.ttl`
- SHACL gates: `prophet/shapes/prophet_artifact.shacl.ttl`
- JSON-LD context: `contexts/prophet-artifact.context.jsonld`
- examples:
  - `examples/prophet_artifact_examples.ttl`
  - `examples/prophet-artifact-gaia-bounded-osm-ingest.example.jsonld`
  - `examples/prophet-artifact-notebook-promotion.example.jsonld`
  - `examples/prophet-artifact-sourceos-image-reproducibility.example.jsonld`

## Downstream consumer contract

- **Prophet Platform** reads `prop:ProphetArtifact`, `prop:hasAction`, and `prop:hasRuntime` to execute governed artifact pipelines.
- **Sociosphere** reads `prop:hasPolicy`, `prop:hasSafetyClass`, and `prop:hasEvidence` to enforce governance and promotion posture.
- **Sherlock/Holmes** read `prop:hasEvidence`, `prop:hasProvenance`, and `prop:hasMetric` for diagnostic traceability and investigation context.
- **Lattice Forge** reads `prop:runtimeSubstrate` and `prop:hasAction` to bind execution to the lattice-forge substrate and approved verbs.
- **GAIA** reads bounded ingest artifact records (`prop:datasetKind`, `prop:bounded`, `prop:fetch`, `prop:validate`) for map-data custody workflows.
- **Delivery Excellence** reads `prop:hasMetric` and `prop:registerDeliveryExcellence` to track promotion KPIs and scoreboard publication.
- **SourceOS** reads runtime and attestation fields (`prop:sourceosSubstrate`, `prop:attest`, provenance + evidence links) for reproducible image build surfaces.
