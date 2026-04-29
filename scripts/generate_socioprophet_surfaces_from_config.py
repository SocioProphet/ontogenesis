#!/usr/bin/env python3
"""Generate SocioProphet surface TTL from socioprophet/config/surfaces.json.

This is the snake_case-aware generator for the live upstream surface source.
It accepts the current list-shaped config used by SocioProphet/socioprophet and
emits deterministic TTL instance data for the SocioProphet ontology module.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HEADER = '''@prefix sp: <https://socioprophet.com/ontology/v0#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

'''


def qname(value: Any) -> str:
    text = str(value or "").strip()
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in text)
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    if cleaned and cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned or "unnamed"


def literal(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def route_id(path: str) -> str:
    return f"sp:route_{qname(path)}"


def site_id(surface_id: str, index: int) -> str:
    return f"sp:site_{qname(surface_id)}_{index}"


def add_obj(lines: list[str], pred: str, obj: str) -> None:
    lines.append(f"  {pred} {obj} ;")


def add_literal(lines: list[str], pred: str, value: Any) -> None:
    lines.append(f'  {pred} "{literal(value)}" ;')


def emit_surface(node: dict[str, Any]) -> str:
    surface_id = str(node.get("id") or node.get("slug") or node.get("label") or "surface")
    subject = f"sp:surface_{qname(surface_id)}"
    lines = [f"{subject} a sp:Surface ;"]
    add_literal(lines, "rdfs:label", node.get("label") or surface_id)

    scalar_literals = {
        "description": "sp:descriptionText",
        "next_action": "sp:nextActionText",
    }
    for key, pred in scalar_literals.items():
        if node.get(key) not in (None, ""):
            add_literal(lines, pred, node[key])

    if "homepage_visible" in node:
        lines.append(f"  sp:homepageVisible {'true' if bool(node['homepage_visible']) else 'false'} ;")

    if node.get("category"):
        add_obj(lines, "sp:hasCategory", f"sp:cat_{qname(node['category'])}")
    if node.get("status"):
        add_obj(lines, "sp:hasStatus", f"sp:status_{qname(node['status'])}")

    for audience in node.get("audiences", []) or []:
        add_obj(lines, "sp:hasAudience", f"sp:aud_{qname(audience)}")
    for topic in node.get("topic_constituents", []) or []:
        add_obj(lines, "sp:hasTopic", f"sp:topic_{qname(topic)}")
    for topic in node.get("normalized_topics", []) or []:
        add_obj(lines, "sp:hasNormalizedTopic", f"sp:topic_{qname(topic)}")

    overlay = node.get("investor_overlay") or {}
    if isinstance(overlay, dict) and overlay.get("lens"):
        add_obj(lines, "sp:hasInvestorLens", f"sp:lens_{qname(overlay['lens'])}")

    route_fields = {
        "landing_page": "sp:landingRoute",
        "survey_page": "sp:surveyRoute",
        "docs_path": "sp:docsRoute",
    }
    for key, pred in route_fields.items():
        path = node.get(key)
        if path:
            add_obj(lines, pred, route_id(path))

    for related in node.get("related_surfaces", []) or []:
        add_obj(lines, "sp:relatedSurface", f"sp:surface_{qname(related)}")
    for idx, site in enumerate(node.get("related_sites", []) or [], start=1):
        add_obj(lines, "sp:relatedSite", site_id(surface_id, idx))

    lines[-1] = lines[-1].rstrip(" ;") + " ."
    return "\n".join(lines) + "\n\n"


def emit_routes_and_sites(surfaces: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    seen_routes: set[str] = set()
    for node in surfaces:
        for key in ("landing_page", "survey_page", "docs_path"):
            path = node.get(key)
            if not path or path in seen_routes:
                continue
            seen_routes.add(path)
            chunks.append(f'{route_id(path)} a sp:Route ;\n  sp:path "{literal(path)}" .\n\n')
        surface_id = str(node.get("id") or node.get("slug") or node.get("label") or "surface")
        for idx, site in enumerate(node.get("related_sites", []) or [], start=1):
            chunks.append(f'{site_id(surface_id, idx)} a sp:Site ;\n  sp:url "{literal(site)}" .\n\n')
    return "".join(chunks)


def load_surfaces(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        surfaces = data.get("surfaces", data)
        if isinstance(surfaces, list):
            return [item for item in surfaces if isinstance(item, dict)]
        if isinstance(surfaces, dict):
            return [dict({"id": key}, **value) for key, value in surfaces.items() if isinstance(value, dict)]
    raise SystemExit(f"Unsupported surfaces JSON shape in {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("surfaces_json")
    parser.add_argument("output_ttl")
    args = parser.parse_args()

    surfaces = load_surfaces(Path(args.surfaces_json))
    chunks = [HEADER]
    chunks.extend(emit_surface(node) for node in surfaces)
    chunks.append(emit_routes_and_sites(surfaces))
    Path(args.output_ttl).write_text("".join(chunks), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
