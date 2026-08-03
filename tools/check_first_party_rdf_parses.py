#!/usr/bin/env python3
"""Guard: every first-party RDF graph must parse with rdflib -- OFFLINE.

Surfaced by SocioProphet/ontogenesis#132: six first-party JSON-LD files in this
repo (two `catalog/*.jsonld` registries plus four `examples/*.jsonld` demos)
carried an `@context` pointing at a dead remote URL
(`https://socioprophet.github.io/ontogenesis/contexts/...`, HTTP 404) or a bare
context body that is not a valid context document. rdflib therefore failed to
parse them the moment context resolution had to reach the network, which is
exactly what happens in offline CI. The estate rule is "vendor, don't reference
external CDNs": each `@context` now points at the vendored local copy under
`contexts/` (or a proper wrapped context document), so every first-party graph
resolves entirely on disk.

This check closes the hole for good: it rdflib-parses every first-party
`*.ttl`/`*.jsonld` and fails (nonzero exit) on any parse error, so an
unparseable graph -- or a re-introduced dead remote `@context` -- cannot land.
It is fail-closed: it must not reach the network to succeed.

Scope: first-party graphs only. Vendored/external/build trees (`node_modules`,
`third_party`, `vendor*`, `.venv`, `dist`, `.git`, `.claude` worktrees,
`@`-pinned worktree dirs, `*.wt`) are skipped.

Negative fixtures: a fixture that is *intentionally* invalid RDF *syntax* (a
syntax negative) must be listed in NEGATIVE_SYNTAX_FIXTURES with a reason. Such
a file is expected to FAIL to parse; if one ever starts parsing, this check
fails so the declaration stays honest. NOTE: a semantically-negative fixture
(e.g. the `examples/**/invalid/*.invalid.jsonld` files, which model a governance
state that should be blocked downstream) is still syntactically valid JSON-LD
and MUST parse -- it is NOT listed here.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

# File extension -> rdflib parse format.
FORMATS = {".ttl": "turtle", ".jsonld": "json-ld"}

# Directory names that mark vendored / external / build / non-first-party trees.
EXCLUDE_DIR_NAMES = {
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "dist",
    ".claude",
    "third_party",
    "vendor",
    "vendored",
    "site-packages",
}

# Intentional SYNTAX-negative fixtures: expected to fail rdflib parse.
# Map "<relative/path>": "<why it is intentionally invalid>".
# Empty today -- this repo has no RDF-syntax negatives. (The
# `examples/**/invalid/*.invalid.jsonld` fixtures are semantic negatives and
# parse fine.)
NEGATIVE_SYNTAX_FIXTURES: dict[str, str] = {}


def _excluded(path: Path) -> bool:
    for part in path.relative_to(ROOT).parts:
        if part in EXCLUDE_DIR_NAMES:
            return True
        if part.startswith("@"):
            return True
        if part.endswith(".wt"):
            return True
    return False


def _iter_graphs():
    for ext in FORMATS:
        for path in ROOT.rglob(f"*{ext}"):
            if _excluded(path):
                continue
            yield path


def main() -> int:
    from rdflib import Graph  # imported here so a missing dep gives a clear message

    failed = False
    checked = 0
    negatives_seen: set[str] = set()

    for path in sorted(_iter_graphs()):
        rel = path.relative_to(ROOT).as_posix()
        fmt = FORMATS[path.suffix.lower()]
        expected_negative = rel in NEGATIVE_SYNTAX_FIXTURES
        try:
            Graph().parse(str(path), format=fmt)
            parsed = True
            err = ""
        except Exception as exc:  # rdflib raises many parser-specific types
            parsed = False
            err = f"{type(exc).__name__}: {exc}"

        if expected_negative:
            negatives_seen.add(rel)
            if parsed:
                print(
                    f"ERR: {rel} is declared a syntax-negative fixture but now PARSES; "
                    "remove it from NEGATIVE_SYNTAX_FIXTURES or restore its negative intent.",
                    file=sys.stderr,
                )
                failed = True
            continue

        checked += 1
        if not parsed:
            print(f"ERR: {rel} failed to parse ({fmt}): {err}", file=sys.stderr)
            failed = True

    missing = set(NEGATIVE_SYNTAX_FIXTURES) - negatives_seen
    for rel in sorted(missing):
        print(
            f"ERR: declared syntax-negative fixture not found on disk: {rel}",
            file=sys.stderr,
        )
        failed = True

    if failed:
        return 1

    print(
        f"OK: all {checked} first-party RDF graph(s) parse "
        f"({len(negatives_seen)} declared syntax-negative fixture(s) skipped)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
