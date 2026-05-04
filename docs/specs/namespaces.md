# Namespaces

Base IRI: `https://socioprophet.github.io/ontogenesis/`

Core prefixes used by Ontogenesis:

- `upper:` `https://socioprophet.github.io/ontogenesis/upper#`
- `middle:` `https://socioprophet.github.io/ontogenesis/middle#`
- `lower:` `https://socioprophet.github.io/ontogenesis/lower#`
- `plat:` `https://socioprophet.github.io/ontogenesis/platform#`
- `prop:` `https://socioprophet.github.io/ontogenesis/prophet#`
- `capd:` `https://socioprophet.github.io/ontogenesis/prophet#capd#`
- `nl:` `https://socioprophet.github.io/ontogenesis/noether#`
- `epi:` `https://socioprophet.github.io/ontogenesis/epi#`
- `og:` `https://socioprophet.github.io/ontogenesis/og#`
- `shir:` `https://socioprophet.github.io/ontogenesis/shir#`

Guideline:
- Use stable, lowercase file names.
- Use `owl:versionInfo` (SemVer string).
- Prefer adding new terms to new modules rather than expanding old ones without SemVer bump.
- Use the `shir:` namespace for Semantic Hyperknowledge Intermediate Representation terms that preserve context, evidence, temporal scope, policy scope, induction traces, and projection receipts before downstream graph/retrieval/ML lowering.

