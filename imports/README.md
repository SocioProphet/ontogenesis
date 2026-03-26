# imports/

This folder holds the **pin-and-fetch** manifest for external ontologies and shapes.

Policy:
- We do not blindly vendor third-party ontologies into this repo unless licensing permits.
- Instead we maintain a manifest with:
  - canonical IRI / download URL
  - license expectations
  - pinned digest (sha256) once fetched
  - local vendored path if we choose to vendor

Use:
- `python scripts/fetch_imports.py --manifest imports/ontologies.yaml --out third_party/`

