#!/usr/bin/env python3
import json
from pathlib import Path

HEADER = '''@prefix sp: <https://socioprophet.com/ontology/v0#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

'''

def qname(value: str) -> str:
    cleaned = ''.join(ch if ch.isalnum() else '_' for ch in value.strip())
    if cleaned and cleaned[0].isdigit():
        cleaned = '_' + cleaned
    return cleaned or 'unnamed'


def emit_surface(key: str, node: dict) -> str:
    lines = []
    subject = f"sp:surface_{qname(key)}"
    lines.append(f"{subject} a sp:Surface ;")
    label = node.get('label') or key
    lines.append(f'  rdfs:label "{label}" ;')
    if 'description' in node:
        desc = str(node['description']).replace('"', '\\"')
        lines.append(f'  sp:descriptionText "{desc}" ;')
    if 'homepageVisible' in node:
        val = 'true' if bool(node['homepageVisible']) else 'false'
        lines.append(f'  sp:homepageVisible {val} ;')
    if 'nextAction' in node:
        nxt = str(node['nextAction']).replace('"', '\\"')
        lines.append(f'  sp:nextActionText "{nxt}" ;')
    if 'category' in node:
        lines.append(f'  sp:hasCategory sp:cat_{qname(str(node["category"]))} ;')
    if 'status' in node:
        lines.append(f'  sp:hasStatus sp:status_{qname(str(node["status"]))} ;')
    for audience in node.get('audiences', []) or []:
        lines.append(f'  sp:hasAudience sp:aud_{qname(str(audience))} ;')
    for topic in node.get('topics', []) or []:
        lines.append(f'  sp:hasTopic sp:topic_{qname(str(topic))} ;')
    for topic in node.get('normalizedTopics', []) or []:
        lines.append(f'  sp:hasNormalizedTopic sp:topic_{qname(str(topic))} ;')
    if 'landingPath' in node:
        lines.append(f'  sp:landingRoute sp:route_{qname(str(node["landingPath"]))} ;')
    if 'docsPath' in node:
        lines.append(f'  sp:docsRoute sp:route_{qname(str(node["docsPath"]))} ;')
    if 'site' in node:
        lines.append(f'  sp:relatedSite sp:site_{qname(str(node["site"]))} ;')
    related = node.get('relatedSurfaces', []) or []
    for rel in related:
        lines.append(f'  sp:relatedSurface sp:surface_{qname(str(rel))} ;')
    lines[-1] = lines[-1].rstrip(' ;') + ' .'
    return '\n'.join(lines) + '\n\n'


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('surfaces_json', help='Path to socioprophet config/surfaces.json')
    parser.add_argument('output_ttl', help='Path to emitted TTL file')
    args = parser.parse_args()

    src = Path(args.surfaces_json)
    out = Path(args.output_ttl)
    data = json.loads(src.read_text())
    if isinstance(data, dict) and 'surfaces' in data:
        surfaces = data['surfaces']
    else:
        surfaces = data

    chunks = [HEADER]
    if isinstance(surfaces, dict):
        for key, node in surfaces.items():
            if isinstance(node, dict):
                chunks.append(emit_surface(key, node))
    elif isinstance(surfaces, list):
        for idx, node in enumerate(surfaces):
            if isinstance(node, dict):
                key = str(node.get('id') or node.get('slug') or node.get('label') or idx)
                chunks.append(emit_surface(key, node))

    out.write_text(''.join(chunks))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
