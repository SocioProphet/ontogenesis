#!/usr/bin/env python3
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(path.read_text())

linear = load(ROOT / 'reports' / 'materialize_linear.json')
linear_expected = load(ROOT / 'fixtures' / 'expected.json')['linear']
assign = load(ROOT / 'reports' / 'materialize_assignment_override.json')
assign_expected = load(ROOT / 'fixtures' / 'expected.json')['assignment_override']
div = load(ROOT / 'reports' / 'materialize_divergence.json')
div_expected = load(ROOT / 'fixtures' / 'expected.json')['divergence']

errors = []
if linear['state_projection_name'] != linear_expected['state_projection_name'] or linear['state_hash'] != linear_expected['state_hash'] or not linear['checkpoint_hash_consistent']:
    errors.append('linear fixture report does not match expected hash/projection/consistency')
if assign['state_projection_name'] != assign_expected['state_projection_name'] or assign['state_hash'] != assign_expected['state_hash'] or not assign['checkpoint_hash_consistent']:
    errors.append('assignment-override fixture report does not match expected hash/projection/consistency')
if len(div['divergences']) != 1:
    errors.append('divergence fixture should emit exactly one divergence')
else:
    reason = div['divergences'][0]['reason']
    detail = div['divergences'][0]['details']
    if reason != div_expected['expected_divergence_reason']:
        errors.append('divergence fixture reason mismatch')
    if detail != div_expected['expected_detail']:
        errors.append('divergence fixture detail mismatch')

if errors:
    print(json.dumps({'ok': False, 'errors': errors}, indent=2))
    sys.exit(1)
print(json.dumps({'ok': True}, indent=2))
