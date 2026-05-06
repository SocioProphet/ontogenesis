# Semantic Enterprise v0.1.0 Release Candidate

## Release target

- Release name: `semantic-enterprise-v0.1.0`
- Release base commit: `ce185581234c2b9aca61c1896084cfd27936673f`
- Release status: ready for formal GitHub tag/release after final branch protection checks

## Scope

Semantic Enterprise v0.1.0 stabilizes the Ontogenesis semantic-enterprise tranche as a governed, downstream-readable release line.

It includes:

- semantic-enterprise architecture and lifecycle contract
- knowledge-graph lifecycle, semantic mapping, and named graph governance modules
- external-standard alignment scaffolds for gist, FIBO, UCO/CASE, D3FEND, IOF SCO, and DoDAF/CCO
- sector ontology modules for finance, threat intelligence, investigation, supply chain, and defense/C2
- sector SHACL gates
- cross-sector and deeper scenario fixtures
- read-only SPARQL examples
- named graph governance fixture
- downstream import bridge contract
- semantic import-contract validator and workflow
- downstream-readable v0.1 manifest
- v0.1 rollup registry and release note

## Release artifacts

Canonical RDF rollup:

- `catalog/semantic_enterprise_v0_1_registry.ttl`

Downstream-readable manifest:

- `manifests/semantic_enterprise_v0_1_manifest.json`

Release note:

- `docs/semantic-enterprise/v0.1-release-note.md`

Import bridge:

- `docs/semantic-enterprise/downstream-import-bridge-v0.1.md`

Validation gates:

- `scripts/validate_semantic_import_contract.py`
- `scripts/validate_semantic_manifest.py`
- `.github/workflows/semantic-import-contract.yml`

## Validation checklist

Before cutting the formal GitHub release/tag, verify these checks are green on the target commit:

- `CI`
- `validate`
- `no-raster-images`
- `semantic-import-contract`

The release candidate base commit had all four workflows green before this release-prep file was added.

## Suggested Git tag

```text
semantic-enterprise-v0.1.0
```

## Suggested GitHub Release title

```text
Semantic Enterprise v0.1.0
```

## Suggested GitHub Release notes

Semantic Enterprise v0.1.0 establishes Ontogenesis as the governed source of truth for the semantic-enterprise architecture. It includes lifecycle and named-graph governance vocabulary, sector modules, alignment scaffolds, scenario fixtures, SPARQL examples, downstream import contracts, and manifest validation.

This release is intended for downstream import by Prophet Platform, Sherlock Search, AgentPlane, PolicyFabric, SourceOS, and DeliveryExcellence. Downstream consumers should preserve source path, canonical IRI, registry entry, validation gate, and named-graph governance metadata.

## Non-goals

This release does not define production graph storage, live ingestion, operational response playbooks, incident-response procedures, or access-control implementation. Those remain downstream runtime responsibilities.
