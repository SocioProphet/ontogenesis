# Ontogenesis

An auditable, policy-gated, supply-chain–traceable Git repository for RDF/OWL/JSON-LD ontologies and semantic web assets used across the **SocioProphet** stack.

This repo is designed to support:

- **Repeatable builds** of ontology distributions (`dist/`) from source ontologies.
- **Deterministic hashing** + an append-only **ledger** (`ledger/ledger.csv`) for audit.
- **Artifact signing** (COSE_Sign1) for `dist/*` artifacts.
- **SHACL gates** for structural and policy constraints (promotion checks).
- A machine-readable **catalog/registry** that enumerates modules, SemVer, status, and compatibility notes.
- A layered ontology architecture: **Upper**, **Middle**, **Lower**, plus product/platform modules (**Platform / SourceOS / Genesis / Inception / Twin / Mesh**), and the **Prophet CLI ontology**.

Base IRI (recommended): `https://socioprophet.github.io/ontogenesis/`

## Repo layout

- `Upper/` — high-level concepts (foundational primitives and alignments)
- `Middle/` — general concepts (systems, governance, provenance, policy, capabilities)
- `Lower/` — atomic bindings to on-device data/services/IO (files, processes, ports, k8s, packages)
- `Domains/` — domain modules (health/FHIR, cyber, metadata, math, etc.)
- `Platform/` — platform modules (SourceOS, Genesis, Inception, Twin, Mesh)
- `prophet/` — **Prophet CLI & system architecture ontology** + SHACL gates
- `epi/` — **Epi‑Onto‑Learning** (Noetherian + quantum lane + publishing provenance)
- `catalog/` — `registry.ttl` + `registry.jsonld` (machine-readable module index)
- `imports/` — curated external ontologies (pin-and-fetch manifest)
- `shapes/` — SHACL policy bundles (gates)
- `contexts/` — JSON-LD contexts + frames for strict round-trip tests
- `scripts/` — build, audit, sign, verify, SBOM/SPDX
- `dist/` and `audit/` — generated only (CI/build outputs); **no direct edits**

## One-command verification (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

python scripts/validate_rdf.py
python scripts/shacl_gate.py
python scripts/jsonld_roundtrip.py

python scripts/build_dist.py
python scripts/ledger_build.py
python scripts/ledger_verify.py
```

## Release discipline (CI)

On a tag `v*`, CI will:

1. Build `dist/` deterministically (`SOURCE_DATE_EPOCH` fixed).
2. Validate RDF + SHACL gates.
3. Build/verify `ledger/ledger.csv`.
4. COSE-sign each `dist/*` and record signature URIs in the ledger.
5. Emit a minimal SPDX SBOM (`sbom/spdx.json`) with checksums.

## Policy

- `dist/` and `audit/` are **generated only**.
- Changes under `Upper/`, `Middle/`, `Lower/`, `Domains/`, `Platform/`, `prophet/`, `epi/` must be accompanied by `scripts/build_dist.py` + `scripts/ledger_build.py` output changes.
- Promotion gates are enforced via SHACL bundles in `shapes/`.

See `docs/` for the design plan and module map.

