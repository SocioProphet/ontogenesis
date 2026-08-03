# Finance-arc concept registration (Systema Concept Entries v0.2)

Status: draft v0.2
Owner repository: `SocioProphet/ontogenesis`
Closes the ontogenesis half of `[[feedback_bind_upward_worldmodel_ontogenesis]]` for the
2026-08-03 economic/risk ("finance arc").

## Why

The economic/risk work shipped on 2026-08-03 (the omnirisk/EP financial spine,
regime/process taxonomy, Jacob's-ladder asset ontology, and the welfare-annealing
stack) governed its new vocabulary only as *local contract schema*. Each term was
constrained inside its own JSON schema, but the terms were **not** registered as
versioned, receipted, source-anchored concepts in the ontogenesis concept
lifecycle. This tranche closes that gap: it routes the new terms through the
Systema Concept Entry model as governed `ConceptEntry` / `ConceptRevision`
records — consume-not-fork, contract-with-teeth.

It does **not** redefine value, risk, or the concept model. It binds:

- **down/across** to the introducing PR/contract of each term (the `SourceAnchor`);
- **up** to the world model via the sibling PR
  [`gaia-world-model#41`](https://github.com/SocioProphet/gaia-world-model/pull/41)
  (*"economic spine as the world-model value-flow subsystem"*), which is the
  **consumer** of this governed vocabulary.

## Model extension (v0.1 → v0.2, additive, not a fork)

Three per-entry governance fields were added to the canonical model in place
(`Platform/Systema/systema-concept-entry.ttl`, `shapes/systema_concept_entry.shacl.ttl`,
`contexts/systema-concept.context.jsonld`):

- `systema:provenanceClass` — `learned | human_authored | imported`;
- `systema:conceptVersion` — SemVer of the concept record;
- `systema:receipt` — content-hash registration receipt `sha256:<hex>` over the
  canonical entry (receipt field excluded); tamper-evident.

## What was registered

| Domain | Count | Graph |
|---|---|---|
| Risk/EP | 11 | `examples/systema/finance-arc-concepts.example.jsonld` |
| Regime/process | 5 | `examples/systema/finance-arc-concepts.example.jsonld` |
| Asset ontology | 2 | `examples/systema/finance-arc-concepts.example.jsonld` |
| Welfare/value | 5 | `examples/systema/finance-arc-concepts.example.jsonld` |
| GAIA value-flow vocabulary | 11 | `examples/systema/gaia-value-flow-vocabulary.example.jsonld` |
| **Total** | **34** | |

Each entry carries a definition, a `SourceAnchor` (its introducing PR/contract),
a provenance class, a version, a receipt, a promotion state, and a revision
history. Finance-arc terms merged on `main` are anchored to their economic-prophet
PR (#42–#54); welfare/value terms are anchored to the in-flight WEA-1 contract
(`feat/welfare-annealing`) and stay `source_anchored`/`candidate` until it merges;
the memory-regime taxonomy is cited to its canonical producer (`memory-mesh#50`)
per the financial-spine anti-fragmentation index, with economic-prophet #46/#54 as
consumers.

## GAIA value-flow vocabulary — stable concept IDs

`gaia-world-model#41` currently uses these as bare enum strings / fields. It should
reference the governed concept IDs below instead. IDs are stable.

| Bare token (gaia #41) | Governed concept ID | Also anchored to |
|---|---|---|
| `carrying_capacity` | `systema:concept:carrying-capacity` | WorldModelSubstrate W read |
| `natural_capital` | `systema:concept:natural-capital` | economic-prophet#52 ALC-1 |
| `extractive_nonrenewable` | `systema:concept:extractive-nonrenewable` | economic-prophet#52 ALC-1 |
| `renewable_harvest` | `systema:concept:renewable-harvest` | economic-prophet#52 ALC-1 |
| `qol_index` | `systema:concept:qol-index` | WEA-1 `welfare_annealing/qol.py` |
| `qol_index.life_length` | `systema:concept:qol-dim-life-length` | human-digital-twin state |
| `qol_index.health` | `systema:concept:qol-dim-health` | human-digital-twin state |
| `qol_index.education` | `systema:concept:qol-dim-education` | human-digital-twin state |
| `galactic_space_twin` | `systema:concept:galactic-space-twin` | twin hierarchy (outer) |
| `world_economic_twin` | `systema:concept:world-economic-twin` | twin hierarchy (middle) |
| `human_digital_twin` | `systema:concept:human-digital-twin` | twin hierarchy (inner) |

## Teeth (both directions)

Executable, deterministic, stdlib-only:
`scripts/validate_systema_concept_entries.py` (wired into `make validate`), plus
the declarative SHACL shape. Receipts are minted/verified by
`scripts/mint_concept_receipts.py` + `scripts/concept_receipt.py`.

**VERIFIES (admitted):** a term registered *with* a `SourceAnchor` (its introducing
PR/contract) + provenance class + version + receipt is admitted; a `human_authored`
override supersedes a prior `learned` entry while retaining the prior
`ConceptRevision` (`systema:concept:risk-measure-family`, promoted to
`reviewed_definition` on a `manually_reviewed` anchor, two revisions).

**REJECTS:**

- a bare term with no `SourceAnchor` (a word without evidence — learn-don't-match);
- a concept promoted past its reviewed state on an unreviewed anchor;
- a registration with no receipt;
- a registration with a tampered receipt (hash mismatch);
- a registration missing a provenance class.

## Ownership boundary

Ontogenesis owns the machine-readable concept model and these registrations.
economic-prophet / memory-mesh / gaia-world-model own their contracts and are
referenced by `SourceAnchor`, never forked. The KE workbench (prophet-workspace)
and the client-vue Knowledge Studio bind dictionaries to these concept IDs by
reference.
