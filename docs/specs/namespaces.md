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
- `oq:` `https://socioprophet.github.io/ontogenesis/platform/oq#`
- `clink:` `https://socioprophet.github.io/ontogenesis/candidate-link#`

Current platform-family prefixes:

- `parse:` `https://socioprophet.github.io/ontogenesis/Platform/Parsing/core#`
- `plg:` `https://socioprophet.github.io/ontogenesis/Platform/Parsing/link-grammar#`
- `acset:` `https://socioprophet.github.io/ontogenesis/Platform/Parsing/acset-parse#`
- `hgp:` `https://socioprophet.github.io/ontogenesis/Platform/Parsing/hypergraph-promotion#`
- `michael:` `https://socioprophet.github.io/ontogenesis/Platform/Epistemics/michael-core#`
- `hdt:` `https://socioprophet.github.io/ontogenesis/Platform/Twins/human-digital-twin#`
- `vf:` `https://socioprophet.github.io/ontogenesis/bindings/valueflows-governed#`

Guideline:
- Use stable, lowercase file names.
- Use `owl:versionInfo` (SemVer string).
- Prefer adding new terms to new modules rather than expanding old ones without SemVer bump.
- Use the `shir:` namespace for Semantic Hyperknowledge Intermediate Representation terms that preserve context, evidence, temporal scope, policy scope, induction traces, and projection receipts before downstream graph/retrieval/ML lowering.
- Use `oq:` for the governed ontology-query adapter contract. Do not overload `sparql` routing for ontology-query requests.
- Use `clink:` for Candidate Link Intelligence Plane concepts when machine-readable vocabulary is added; until then, `docs/specs/candidate-link-intelligence-plane.md` is the normative prose contract.

