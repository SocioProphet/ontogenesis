#!/usr/bin/env python3
"""Deterministic registration-receipt canonicalization for Systema Concept Entries.

A registration receipt is a content hash over the *canonical* concept entry with
the ``receipt`` field removed. It is tamper-evident: any later edit to the entry
changes the hash, so a stale or forged receipt is detectable. Pure stdlib
(json + hashlib) so the value is byte-for-byte reproducible in CI on any host.

This module is shared by ``mint_concept_receipts.py`` (writes receipts) and
``validate_systema_concept_entries.py`` (recomputes + checks them), so mint and
verify can never drift apart.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

RECEIPT_FIELD = "receipt"
RECEIPT_PREFIX = "sha256:"


def canonical_bytes(entry: dict[str, Any]) -> bytes:
    """Canonical JSON of an entry with the receipt field removed.

    Keys sorted, tight separators, UTF-8, no NaN. Order-independent and
    whitespace-independent so the digest depends only on content.
    """
    body = {k: v for k, v in entry.items() if k != RECEIPT_FIELD}
    return json.dumps(
        body,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def compute_receipt(entry: dict[str, Any]) -> str:
    """Return ``sha256:<hex>`` over the canonical entry (receipt excluded)."""
    return RECEIPT_PREFIX + hashlib.sha256(canonical_bytes(entry)).hexdigest()
