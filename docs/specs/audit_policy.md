# Audit & supply-chain policy

This repo is intended to be **boring** in the best way:

- Deterministic build output.
- Cryptographic hashes for every released artifact.
- Artifact signing (detached signatures in this repo; COSE Sign1 recommended in production).
- SHACL promotion gates to prevent silent semantic drift.

## Generated directories

- `dist/` — distribution surface
- `audit/` — build metadata, manifests, SHACL reports
- `ledger/` — checksums + signature pointers
- `signatures/` — detached signatures

Policy:
- Do not edit `dist/` or `audit/` by hand.
- Modify ontology sources, then run build scripts.
- CI reproduces outputs on tags.

## Determinism

CI should set `SOURCE_DATE_EPOCH` (recommended) and run:

- `scripts/build_dist.py` (copy + manifest)
- `scripts/ledger_build.py` (ledger)
- `scripts/sign_dist.py` (signature pointers)
- `scripts/spdx_emit.py` (SBOM)

## Promotion gates (SHACL)

SHACL bundles in `shapes/` and module-local shapes (e.g., `prophet/shapes/`) encode:
- required fields
- opt-in for hardware usage
- minimal invariants (e.g., a capability must declare plane + verb)

