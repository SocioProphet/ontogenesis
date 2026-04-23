# Contributing to Ontogenesis

Thanks for contributing.

## Development setup

```bash
make venv
make deps
```

## Required validation before opening a PR

Run the full pipeline locally:

```bash
make all
```

## Change scope and generated artifacts

- Source ontology changes typically happen under:
  - `Upper/`, `Middle/`, `Lower/`, `Domains/`, `Platform/`, `prophet/`, `epi/`
- `dist/` and `audit/` are generated-only.
- Keep changes focused and minimal; avoid unrelated refactors.

## Documentation expectations

- Update `README.md` and/or docs in `docs/` when behavior, workflows, or module surfaces change.
- Prefer adding docs close to the affected module and linking from `docs/README.md`.

## Pull requests

- Use a clear title and include a concise summary of:
  - what changed
  - why it changed
  - how it was validated (`make all` output)
- Link related issues when applicable.

## Coding and repository standards

- Follow existing file naming and ontology namespace conventions.
- Keep metadata synchronized when adding modules (for example registry entries and namespace docs where relevant).

