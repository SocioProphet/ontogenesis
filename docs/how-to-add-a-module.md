# How to add a module

1. Create a Turtle file in the appropriate layer folder (Upper/Middle/Lower/Domains/Platform/prophet/epi).
2. Add JSON-LD context (optional) under `contexts/` if the module has a JSON-LD surface.
3. Add SHACL shapes under `shapes/` (or module-local `shapes/`) for promotion gates.
4. Register the module in `catalog/registry.ttl` and `catalog/registry.jsonld`.
5. Run:
   - `python scripts/validate_rdf.py`
   - `python scripts/shacl_gate.py`
   - `python scripts/build_dist.py`
   - `python scripts/ledger_build.py`
6. Commit source + generated outputs **except** `dist/` and `audit/` unless your policy is to commit them.
   (Default policy here: generated outputs are CI-only.)

