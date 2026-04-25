#!/usr/bin/env python3
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / 'compact-bundle.v1.json'

def load(path):
    return json.loads(path.read_text())

def load_expected():
    if BUNDLE_PATH.exists():
        return json.loads(BUNDLE_PATH.read_text())['fixtures']['expected.json']
    return load(ROOT / 'fixtures' / 'expected.json')

expected = load_expected()
linear = load(ROOT / 'reports' / 'materialize_linear.json')
assign = load(ROOT / 'reports' / 'materialize_assignment_override.json')
div = load(ROOT / 'reports' / 'materialize_divergence.json')
errors = []
if linear['state_projection_name'] != expected['linear']['state_projection_name'] or linear['state_hash'] != expected['linear']['state_hash'] or not linear['checkpoint_hash_consistent']:
    errors.append('linear fixture report does not match expected hash/projection/consistency')
if assign['state_projection_name'] != expected['assignment_override']['state_projection_name'] or assign['state_hash'] != expected['assignment_override']['state_hash'] or not assign['checkpoint_hash_consistent']:
    errors.append('assignment-override fixture report does not match expected hash/projection/consistency')
if len(div['divergences']) != 1:
    errors.append('divergence fixture should emit exactly one divergence')
else:
    reason = div['divergences'][0]['reason']; detail = div['divergences'][0]['details']
    if reason != expected['divergence']['expected_divergence_reason']:
        errors.append('divergence fixture reason mismatch')
    if detail != expected['divergence']['expected_detail']:
        errors.append('divergence fixture detail mismatch')
if errors:
    print(json.dumps({'ok': False, 'errors': errors}, indent=2)); sys.exit(1)
print(json.dumps({'ok': True}, indent=2))
