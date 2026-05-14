# Knowledge Context module

`Platform/knowledge-context.ttl` is the Ontogenesis semantic governance module for the Knowledge Context v1 standards now carried by `SocioProphet/socioprophet-standards-knowledge`.

The module deliberately separates semantic governance from runtime storage:

- RDF/OWL terms describe canonical artifact classes and relations.
- SHACL shapes define promotion-gate constraints for passages, mentions, embeddings, vector indexes, and context labels.
- JSON-LD context terms provide a stable linked-data interpretation for Knowledge Context artifacts.
- Runtime storage choices remain governed by `SocioProphet/socioprophet-standards-storage`.

## Scope

This module covers:

- `KnowledgeContext`
- `Note`
- `Claim`
- `Annotation`
- `Passage`
- `Entity`
- `Mention`
- `MeriotopographicEdge`
- `ProvenanceRecord`
- `EmbeddingRef`
- `VectorIndexRef`
- `EntityResolutionRecord`

## Contract alignment

The canonical v1 contract labels are represented as data on `kc:KnowledgeContextV1`:

- `KNOWLEDGE_AVRO_v1`
- `KNOWLEDGE_JSONLD_v1`

This keeps ontology governance aligned with the versioned contract labels without embedding Avro payload details into the ontology module.
