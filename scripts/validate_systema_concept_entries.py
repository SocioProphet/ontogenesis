#!/usr/bin/env python3
"""Teeth for the finance-arc Systema Concept Entry registration.

Deterministic, stdlib-only (json + hashlib) so it cannot flake in CI. It mirrors
the systema:SystemaConceptEntry SHACL shape field-for-field and adds the two
cross-field governance rules the declarative shape cannot express on its own:

  VERIFIES (positives — examples/systema/finance-arc-concepts.example.jsonld):
    * every registered term carries a SourceAnchor (its introducing PR/contract)
      + provenance class + a version + a receipt -> admitted;
    * the receipt recomputes (tamper-evident);
    * a human-authored override supersedes a learned entry AND retains the prior
      ConceptRevision (risk-measure-family: human_authored @ reviewed_definition
      on a manually_reviewed anchor, >= 2 revisions).

  REJECTS (negatives — examples/systema/invalid/*.invalid.jsonld):
    * a bare term with no SourceAnchor  (a word without evidence);
    * a concept promoted past its reviewed state on an unreviewed anchor;
    * a registration with no receipt;
    * a registration with a missing provenance class;
    * a registration whose receipt has been tampered with.

learn-don't-match: admission is grounded in a source anchor + receipt, never in
the word itself.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept_receipt import RECEIPT_FIELD, compute_receipt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
POSITIVES = [
    ROOT / "examples" / "systema" / "finance-arc-concepts.example.jsonld",
    ROOT / "examples" / "systema" / "gaia-value-flow-vocabulary.example.jsonld",
]
INVALID_DIR = ROOT / "examples" / "systema" / "invalid"

PROMOTION_STATES = {
    "observed_term", "extracted_candidate", "source_anchored", "reviewed_definition",
    "operational_definition", "implementation_linked", "tested_doctrine",
    "public_standard", "deprecated", "contested",
}
# States that assert human review; reaching them requires a reviewed anchor.
REVIEWED_OR_BEYOND = {
    "reviewed_definition", "operational_definition", "implementation_linked",
    "tested_doctrine", "public_standard",
}
REVIEWED_ANCHOR_STATES = {"manually_reviewed", "independently_verified"}
REVIEW_STATES = {
    "unreviewed", "candidate", "manually_reviewed", "independently_verified",
    "rejected", "contested",
}
QUOTE_BOUNDARIES = {
    "exact", "near_verbatim", "paraphrase", "operational_translation",
    "analogy", "unsupported",
}
CLAIM_LEVELS = {
    "historical_source_claim", "operational_definition", "design_analogy",
    "formal_claim", "implementation_requirement", "conformance_rule",
}
CONFIDENCE = {"A", "B", "C", "D", "E"}
PROVENANCE = {"learned", "human_authored", "imported"}

# Each negative fixture must trip a recognisable governance signal.
EXPECTED_SIGNALS = {
    "no-source-anchor": "source anchor",
    "promoted-past-review": "promoted past",
    "no-receipt": "receipt",
    "missing-provenance": "provenance",
    "tampered-receipt": "receipt",
}


def entries(doc: dict) -> list[dict]:
    if "@graph" in doc:
        return [e for e in doc["@graph"] if isinstance(e, dict)]
    return [doc]


def _nonempty_str_list(value) -> list:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def check_entry(entry: dict) -> list[str]:
    """Return a list of governance violations; empty list == admitted."""
    v: list[str] = []
    cid = entry.get("conceptId", "<no-conceptId>")

    if not entry.get("conceptId"):
        v.append(f"{cid}: missing conceptId")
    if not entry.get("skos:prefLabel"):
        v.append(f"{cid}: missing prefLabel")

    anchors = _nonempty_str_list(entry.get("sourceAnchor"))
    if not anchors:
        v.append(f"{cid}: no source anchor (a word without evidence is not a concept)")
    for a in anchors:
        if not isinstance(a, dict):
            v.append(f"{cid}: source anchor is not a record")
            continue
        if not a.get("sourceRef"):
            v.append(f"{cid}: source anchor missing sourceRef")
        if not a.get("sourceKind"):
            v.append(f"{cid}: source anchor missing sourceKind")
        if a.get("extractionConfidence") not in CONFIDENCE:
            v.append(f"{cid}: source anchor extractionConfidence invalid")
        if a.get("reviewState") not in REVIEW_STATES:
            v.append(f"{cid}: source anchor reviewState invalid")
        if a.get("quoteBoundary") not in QUOTE_BOUNDARIES:
            v.append(f"{cid}: source anchor quoteBoundary invalid")
        if not a.get("uncertaintyNote"):
            v.append(f"{cid}: source anchor missing uncertaintyNote")

    defs = _nonempty_str_list(entry.get("definition"))
    if not defs:
        v.append(f"{cid}: missing definition")
    for d in defs:
        if isinstance(d, dict):
            if not d.get("definitionText"):
                v.append(f"{cid}: definition missing definitionText")
            if d.get("claimLevel") not in CLAIM_LEVELS:
                v.append(f"{cid}: definition claimLevel invalid")

    if not entry.get("operationalDefinition"):
        v.append(f"{cid}: missing operationalDefinition")
    if not _nonempty_str_list(entry.get("allowedUse")):
        v.append(f"{cid}: missing allowedUse")
    if not _nonempty_str_list(entry.get("forbiddenUse")):
        v.append(f"{cid}: missing forbiddenUse")
    if not _nonempty_str_list(entry.get("implementationSurface")):
        v.append(f"{cid}: missing implementationSurface")
    if not _nonempty_str_list(entry.get("evidenceRequirement")):
        v.append(f"{cid}: missing evidenceRequirement")

    promo = entry.get("promotionState")
    if promo not in PROMOTION_STATES:
        v.append(f"{cid}: promotionState invalid")

    # --- governance provenance (v0.2) ---
    prov = entry.get("provenanceClass")
    if prov not in PROVENANCE:
        v.append(f"{cid}: missing or invalid provenance class")

    ver = entry.get("conceptVersion")
    if not isinstance(ver, str) or not ver:
        v.append(f"{cid}: missing version")

    receipt = entry.get(RECEIPT_FIELD)
    if not isinstance(receipt, str) or not receipt:
        v.append(f"{cid}: no receipt (a registration without a receipt is inadmissible)")
    else:
        want = compute_receipt(entry)
        if receipt != want:
            v.append(f"{cid}: receipt mismatch (tampered) have={receipt} want={want}")

    # --- cross-field: promotion may not outrun anchor review ---
    if promo in REVIEWED_OR_BEYOND:
        reviewed = any(
            isinstance(a, dict) and a.get("reviewState") in REVIEWED_ANCHOR_STATES
            for a in anchors
        )
        if not reviewed:
            v.append(
                f"{cid}: promoted past reviewed state ('{promo}') on an unreviewed anchor"
            )

    return v


def assert_supersede_with_history(pos_entries: list[dict]) -> list[str]:
    """The human-authored override must supersede yet retain the prior revision."""
    problems: list[str] = []
    target = next(
        (e for e in pos_entries if e.get("conceptId") == "systema:concept:risk-measure-family"),
        None,
    )
    if target is None:
        return ["risk-measure-family override fixture missing"]
    if target.get("provenanceClass") != "human_authored":
        problems.append("override: expected provenanceClass human_authored")
    if target.get("promotionState") not in REVIEWED_OR_BEYOND:
        problems.append("override: expected a reviewed-or-beyond promotionState")
    revs = target.get("revision") or []
    if len([r for r in revs if isinstance(r, dict)]) < 2:
        problems.append("override: prior ConceptRevision not retained (need >= 2 revisions)")
    anchors = target.get("sourceAnchor") or []
    if not any(isinstance(a, dict) and a.get("reviewState") in REVIEWED_ANCHOR_STATES for a in anchors):
        problems.append("override: supersede requires a reviewed anchor")
    return problems


def main() -> int:
    failures = 0

    # ---- positives ----
    pos_entries: list[dict] = []
    for path in POSITIVES:
        if not path.exists():
            print(f"[FAIL] positive example missing: {path}")
            return 1
        doc = json.loads(path.read_text(encoding="utf-8"))
        registered = [e for e in entries(doc) if "provenanceClass" in e or "conceptVersion" in e or RECEIPT_FIELD in e]
        if not registered:
            print(f"[FAIL] no registered concept entries in {path.name}")
            return 1
        admitted = 0
        for e in registered:
            viol = check_entry(e)
            if viol:
                failures += 1
                print(f"[FAIL] positive entry rejected: {e.get('conceptId')}")
                for m in viol:
                    print(f"        - {m}")
            else:
                admitted += 1
        print(f"[OK] {admitted}/{len(registered)} concepts admitted (SourceAnchor + provenance + version + receipt): {path.name}")
        pos_entries.extend(registered)

    for m in assert_supersede_with_history(pos_entries):
        failures += 1
        print(f"[FAIL] {m}")
    if not any(assert_supersede_with_history(pos_entries)):
        print("[OK] human-authored override supersedes with prior ConceptRevision retained.")

    # ---- negatives ----
    negatives = sorted(INVALID_DIR.glob("*.invalid.jsonld")) if INVALID_DIR.exists() else []
    if not negatives:
        print(f"[FAIL] no invalid fixtures found in {INVALID_DIR}")
        return 1
    for path in negatives:
        doc = json.loads(path.read_text(encoding="utf-8"))
        viol_all: list[str] = []
        for e in entries(doc):
            viol_all.extend(check_entry(e))
        if not viol_all:
            failures += 1
            print(f"[FAIL] invalid fixture unexpectedly admitted: {path.name}")
            continue
        signal = next((sig for key, sig in EXPECTED_SIGNALS.items() if path.name.startswith(f"finance-arc.{key}")), None)
        blob = " ".join(viol_all).lower()
        if signal and signal.lower() not in blob:
            failures += 1
            print(f"[FAIL] {path.name} rejected but not for expected reason '{signal}': {viol_all}")
        else:
            print(f"[OK] invalid fixture rejected ({signal or 'governance'}): {path.name}")

    if failures:
        print(f"\n{failures} systema concept-entry teeth failure(s).")
        return 1
    print("\nSystema finance-arc concept entries validated (both directions).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
