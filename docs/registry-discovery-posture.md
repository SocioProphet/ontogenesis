# Registry Discovery Posture

Status: v0.1 operational posture

Related issue: #93

## Decision

Ontogenesis currently uses a hybrid registry discovery model.

`catalog/registry.ttl` remains the primary registry, but supplemental registry files under `catalog/` are first-class discovery inputs while the ontology estate is being normalized.

Consumers must not assume that `catalog/registry.ttl` alone contains every module.

## Discovery rule

A registry consumer should read:

1. `catalog/registry.ttl`
2. every Turtle registry file under `catalog/` matching either:
   - `*registry*.ttl`
   - `*.registry.ttl`

A registry file contributes module records when it contains subjects typed as `og:Module`.

Each `og:Module` record must declare at least one `og:path`.

## Current registry classes

The current repo includes the primary registry plus multiple supplemental registry tranches for modules that were merged through consolidation and later schema-family work.

Supplemental registries are not abandoned sidecars. They are part of the current discovery surface until a later normalization PR either folds them into `catalog/registry.ttl` or formalizes the hybrid model permanently.

## Validation

The hybrid posture is validated by:

```bash
make validate-registry-discovery
```

This target runs:

```bash
python scripts/validate_registry_discovery.py
```

The validator checks that:

- registry-like Turtle files under `catalog/` parse;
- at least one registry file with `og:Module` records is discovered;
- at least one `og:Module` record is discovered;
- every discovered `og:Module` record declares at least one `og:path`.

The target is included in:

```bash
make validate
```

## Release guidance

Until registry normalization is complete, release notes must say that consumers should read the primary registry and supplemental registry files.

A future release may choose one of these postures:

1. Central registry only: fold all supplemental module records into `catalog/registry.ttl`.
2. Hybrid registry model: keep supplemental registries as canonical and document the discovery algorithm permanently.

The current v0.1 posture is hybrid-discovery-now, normalization-decision-later.

## Non-goals

This document does not require removing supplemental registries.
It does not claim that supplemental registries are historical-only.
It does not define runtime graph loading, package publishing, or downstream API behavior.
