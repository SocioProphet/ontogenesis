# Action Ontology module note

This note accompanies the bootstrap `Middle/action-ontology.ttl` landing.

## What landed

- `Middle/action-ontology.ttl`
- `shapes/action-ontology.shacl.ttl`
- `contexts/action-ontology.context.jsonld`
- `examples/action_ontology_demo.jsonld`
- temporary registry supplements under `catalog/`

## Why the registry supplements exist

The GitHub path used for this bootstrap tranche made additive landings easier than in-place edits to the existing registry files.

For clean final integration, the `catalog/action-ontology.module.ttl` and `catalog/action-ontology.module.jsonld` entries should be folded into:

- `catalog/registry.ttl`
- `catalog/registry.jsonld`

## Intended module identity

- layer: `Middle`
- path: `Middle/action-ontology.ttl`
- base IRI: `https://socioprophet.github.io/ontogenesis/middle/action#`
- semver: `0.1.0`
- label: `Action ontology`

## Relationship to companion standards pack

The semantic core lives here in `ontogenesis`.
The broader portable bootstrap contracts/examples live in `SocioProphet/socioprophet-standards-storage` so ontology-source discipline remains separate from executable bootstrap standards surfaces.
