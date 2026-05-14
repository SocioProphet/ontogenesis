# Ontogenesis

[![CI](https://github.com/SocioProphet/ontogenesis/actions/workflows/ci.yml/badge.svg)](https://github.com/SocioProphet/ontogenesis/actions/workflows/ci.yml)
[![Validation](https://github.com/SocioProphet/ontogenesis/actions/workflows/validate.yml/badge.svg)](https://github.com/SocioProphet/ontogenesis/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**Ontogenesis** is an auditable, policy-gated ontology engineering framework for RDF/OWL/JSON-LD assets used across the SocioProphet stack.

It supports ontology creation, linking, validation, and lifecycle governance across layered semantic modules.

## Quick start

```bash
make venv
make deps
make all
```

This runs:
- RDF parse validation
- SHACL gates
- JSON-LD roundtrip checks
- dist build
- ledger build + verification
- SPDX SBOM generation

## Complies with Standards

This repository provides ontology governance for SocioProphet standards and contract surfaces:

- `SocioProphet/socioprophet-standards-knowledge` — Knowledge Context v1 contracts, Avro Path-A protocols, JSON-LD overlays, fixtures, and lifecycle events.
- `SocioProphet/socioprophet-standards-storage/docs/standards/070-graph-rdf-hypergraph.md` — graph/RDF/property/hypergraph storage guidance consumed by ontology-governed modules.
- `SocioProphet/socioprophet-standards-storage/docs/standards/080-knowledge-context.md` — platform pointer that delegates detailed Knowledge Context standards to the standards-knowledge package.
- `Platform/knowledge-context.ttl` — Ontogenesis semantic governance module for Knowledge Context v1 artifacts.
- `shapes/knowledge-context.shacl.ttl` — SHACL promotion gate for Knowledge Context semantic artifacts.

## What’s in this repository

- `Upper/`, `Middle/`, `Lower/` — layered ontology modules
- `Domains/` — domain ontologies
- `Platform/` — platform-level ontology modules
- `prophet/`, `epi/` — product-specific ontology modules and shapes
- `shapes/` — SHACL constraints and promotion gates
- `examples/` — example instance graphs and JSON-LD inputs
- `catalog/registry.ttl` — module index with layer, path, SemVer, and base IRI metadata
- `scripts/` — validation, dist, ledger, signing, and SBOM utilities
- `docs/` — specifications, onboarding, architecture notes, and diagrams

## Documentation index

Start here:
- [`docs/README.md`](docs/README.md) — documentation hub
- [`docs/how-to-add-a-module.md`](docs/how-to-add-a-module.md) — module authoring workflow
- [`docs/module-map.md`](docs/module-map.md) — current module layout
- [`docs/specs/namespaces.md`](docs/specs/namespaces.md) — canonical namespace references

## Validation and release discipline

`make all` runs the full local verification pipeline:

1. `make validate`
2. `make shacl`
3. `make jsonld`
4. `make build`
5. `make ledger`
6. `make verify`
7. `make sbom`

On release tags (`v*`), CI performs deterministic dist builds, validation, ledger generation/verification, detached signatures, and SPDX SBOM emission.

## Repository policies

- `dist/` and `audit/` are **generated-only**.
- Changes under `Upper/`, `Middle/`, `Lower/`, `Domains/`, `Platform/`, `prophet/`, and `epi/` should include regenerated derived outputs where policy requires.
- Promotion gates are enforced through SHACL bundles in `shapes/`.

## Metadata

- Base namespace references: [`docs/specs/namespaces.md`](docs/specs/namespaces.md)
- Module metadata: [`catalog/registry.ttl`](catalog/registry.ttl)
- Project version: [`VERSION`](VERSION)
- Citation metadata: [`CITATION.cff`](CITATION.cff)

## Contributing and governance

- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Code of conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- Support: [`SUPPORT.md`](SUPPORT.md)

## Keywords

ontology, RDF, OWL, SHACL, JSON-LD, semantic web, knowledge graph, provenance, supply-chain integrity, governance

## License

MIT. See [`LICENSE`](LICENSE).
