#!/usr/bin/env python3
import argparse
import hashlib
import json
import pathlib
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / 'compact-bundle.v1.json'
SCHEMA_ROOT = ROOT / 'schemas'
DATA_ROOT = ROOT / 'data'
PROJECTION_NAME = 'authoritative_projection_v2'
EVENT_SCHEMAS = {
    'processrun.created.v1': 'processrun.created.v1.payload.schema.json',
    'delegation.issued.v1': 'delegation.issued.v1.payload.schema.json',
    'capabilitygrant.issued.v1': 'capabilitygrant.issued.v1.payload.schema.json',
    'task.offered.v1': 'task.offered.v1.payload.schema.json',
    'commitment.accepted.v1': 'commitment.accepted.v1.payload.schema.json',
    'task.progress_updated.v1': 'task.progress_updated.v1.payload.schema.json',
    'task.assignment_overridden.v1': 'task.assignment_overridden.v1.payload.schema.json',
    'task.completed.v1': 'task.completed.v1.payload.schema.json',
    'checkpoint.created.v1': 'checkpoint.created.v1.payload.schema.json',
}

def load_bundle():
    return json.loads(BUNDLE_PATH.read_text()) if BUNDLE_PATH.exists() else None

BUNDLE = load_bundle()
ENV_SCHEMA = BUNDLE['schemas']['event_envelope'] if BUNDLE else json.loads((SCHEMA_ROOT / 'event-envelope.v1.schema.json').read_text())
ENV_VALIDATOR = Draft202012Validator(ENV_SCHEMA)

def load_payload_validator(event_type: str):
    if BUNDLE:
        schema = BUNDLE['schemas']['event_payloads'][EVENT_SCHEMAS[event_type]]
    else:
        schema = json.loads((SCHEMA_ROOT / 'event-payload-schemas.v1.json').read_text())[EVENT_SCHEMAS[event_type]]
    return Draft202012Validator(schema)

def load_events(path: pathlib.Path):
    if path.exists():
        text = path.read_text()
    elif BUNDLE and path.name in BUNDLE['fixtures']:
        text = BUNDLE['fixtures'][path.name]
    else:
        raise FileNotFoundError(path)
    events = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events

def load_context():
    if BUNDLE:
        return BUNDLE['data']['memberships']
    return json.loads((DATA_ROOT / 'memberships.json').read_text())

def validate_event(event):
    errors = []
    for e in ENV_VALIDATOR.iter_errors(event):
        errors.append(f'envelope: {e.message}')
    if event.get('type') in EVENT_SCHEMAS:
        pv = load_payload_validator(event['type'])
        for e in pv.iter_errors(event.get('payload', {})):
            errors.append(f'payload: {e.message}')
    else:
        errors.append(f"payload: unsupported type {event.get('type')!r}")
    return errors

def active_member(memberships, actor_id: str, group_id: str) -> bool:
    return any(m.get('actor_id') == actor_id and m.get('group_id') == group_id and m.get('status') == 'active' for m in memberships)

def has_role(memberships, actor_id: str, group_id: str, wanted: str) -> bool:
    return any(m.get('actor_id') == actor_id and m.get('group_id') == group_id and m.get('status') == 'active' and wanted in m.get('role_ids', []) for m in memberships)

def iso_in_window(when: str, start: str, end):
    if when < start:
        return False
    if end is not None and when > end:
        return False
    return True

def active_capability(state, actor_id: str, capability: str, group_id: str, process_run_id: str, when: str, task_id=None):
    for grant in state['capability_grants'].values():
        if grant['status'] != 'active':
            continue
        if grant['grantee_actor_id'] != actor_id:
            continue
        if grant['capability'] != capability:
            continue
        if grant['group_id'] != group_id or grant['process_run_id'] != process_run_id:
            continue
        if grant.get('task_id') not in (None, task_id):
            continue
        if not iso_in_window(when, grant['valid_from'], grant.get('valid_until')):
            continue
        delegation = state['delegations'].get(grant['delegation_id'])
        if not delegation or delegation['status'] != 'active':
            continue
        if delegation['grantee_actor_id'] != actor_id:
            continue
        if delegation['group_id'] != group_id or delegation['process_run_id'] != process_run_id:
            continue
        if delegation.get('task_id') not in (None, task_id):
            continue
        if not iso_in_window(when, delegation['valid_from'], delegation.get('valid_until')):
            continue
        return True
    return False

def projection_v2(state):
    return {
        'process_run': state['process_run'],
        'task': state['task'],
        'commitments': state['commitments'],
        'delegations': state['delegations'],
        'capability_grants': state['capability_grants'],
        'divergences': state['divergences'],
    }

def hash_projection(projection) -> str:
    data = json.dumps(projection, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return 'sha256:' + hashlib.sha256(data).hexdigest()

def record_divergence(state, event_id, reason, details):
    state['divergences'].append({'event_id': event_id, 'reason': reason, 'details': details})

def reduce_events(events):
    memberships = load_context()
    state = {'process_run': None, 'task': None, 'commitments': {}, 'delegations': {}, 'capability_grants': {}, 'checkpoints': [], 'divergences': []}
    applied = []
    for event in events:
        errs = validate_event(event)
        if errs:
            record_divergence(state, event.get('event_id'), 'validation_error', errs)
            continue
        et = event['type']; p = event['payload']; actor = event.get('actor_id'); when = event['time']
        if et == 'processrun.created.v1':
            if not active_member(memberships, actor, p['group_id']) or not has_role(memberships, actor, p['group_id'], 'role:coordinator'):
                record_divergence(state, event['event_id'], 'policy_denied', 'only active coordinators may create process runs'); continue
            if state['process_run'] is not None:
                record_divergence(state, event['event_id'], 'duplicate_process_run', state['process_run']['object_id']); continue
            state['process_run'] = {'object_id': p['process_run_id'], 'group_id': p['group_id'], 'title': p['title'], 'process_kind': p['process_kind'], 'status': 'active', 'created_by': p['created_by'], 'started_at': p['started_at'], 'planned_end_at': p['planned_end_at'], 'completed_at': None, 'task_ids': []}; applied.append(event['event_id'])
        elif et == 'delegation.issued.v1':
            if state['process_run'] is None or state['process_run']['object_id'] != p['process_run_id'] or state['process_run']['status'] != 'active':
                record_divergence(state, event['event_id'], 'wrong_process', 'delegation must reference an active process run'); continue
            if actor != p['grantor_actor_id']:
                record_divergence(state, event['event_id'], 'wrong_actor', 'event actor must match delegation grantor'); continue
            if not active_member(memberships, actor, p['group_id']) or not (has_role(memberships, actor, p['group_id'], 'role:coordinator') or actor == state['process_run']['created_by']):
                record_divergence(state, event['event_id'], 'policy_denied', 'only process creator or coordinator may issue delegations'); continue
            state['delegations'][p['delegation_id']] = {'object_id': p['delegation_id'], 'grantor_actor_id': p['grantor_actor_id'], 'grantee_actor_id': p['grantee_actor_id'], 'group_id': p['group_id'], 'process_run_id': p['process_run_id'], 'delegation_kind': p['delegation_kind'], 'capability_scope': p['capability_scope'], 'task_id': p['task_id'], 'valid_from': p['valid_from'], 'valid_until': p['valid_until'], 'purpose': p['purpose'], 'status': 'active'}; applied.append(event['event_id'])
        elif et == 'capabilitygrant.issued.v1':
            if state['process_run'] is None or state['process_run']['object_id'] != p['process_run_id'] or state['process_run']['status'] != 'active':
                record_divergence(state, event['event_id'], 'wrong_process', 'capability grant must reference an active process run'); continue
            if actor != p['grantor_actor_id']:
                record_divergence(state, event['event_id'], 'wrong_actor', 'event actor must match capability grantor'); continue
            if not active_member(memberships, actor, p['group_id']) or not (has_role(memberships, actor, p['group_id'], 'role:coordinator') or actor == state['process_run']['created_by']):
                record_divergence(state, event['event_id'], 'policy_denied', 'only process creator or coordinator may issue capability grants'); continue
            delegation = state['delegations'].get(p['delegation_id'])
            if delegation is None or delegation['status'] != 'active':
                record_divergence(state, event['event_id'], 'missing_delegation', 'capability grant requires an active delegation'); continue
            if delegation['grantee_actor_id'] != p['grantee_actor_id'] or delegation['group_id'] != p['group_id'] or delegation['process_run_id'] != p['process_run_id'] or delegation.get('task_id') not in (None, p['task_id']):
                record_divergence(state, event['event_id'], 'delegation_mismatch', 'capability grant scope differs from delegation'); continue
            state['capability_grants'][p['capability_grant_id']] = {'object_id': p['capability_grant_id'], 'delegation_id': p['delegation_id'], 'grantor_actor_id': p['grantor_actor_id'], 'grantee_actor_id': p['grantee_actor_id'], 'group_id': p['group_id'], 'process_run_id': p['process_run_id'], 'task_id': p['task_id'], 'capability': p['capability'], 'valid_from': p['valid_from'], 'valid_until': p['valid_until'], 'status': 'active'}; applied.append(event['event_id'])
        elif et == 'task.offered.v1':
            if state['process_run'] is None or state['process_run']['object_id'] != p['process_run_id'] or state['process_run']['status'] != 'active':
                record_divergence(state, event['event_id'], 'wrong_process', 'task must reference an active process run'); continue
            if not active_member(memberships, actor, p['group_id']):
                record_divergence(state, event['event_id'], 'policy_denied', 'actor lacks active membership'); continue
            base_authority = has_role(memberships, actor, p['group_id'], 'role:coordinator') or actor == state['process_run']['created_by']
            delegated_authority = active_capability(state, actor, 'task.offer', p['group_id'], p['process_run_id'], when, p['task_id'])
            if not (base_authority or delegated_authority):
                record_divergence(state, event['event_id'], 'policy_denied', 'actor lacks coordinator/process authority or task.offer capability grant'); continue
            state['task'] = {'object_id': p['task_id'], 'group_id': p['group_id'], 'process_run_id': p['process_run_id'], 'offered_by': p['offered_by'], 'accepted_by': None, 'status': 'offered', 'due_at': p['due_at'], 'started_at': None, 'completed_at': None}; state['process_run']['task_ids'].append(p['task_id']); applied.append(event['event_id'])
        elif et == 'commitment.accepted.v1':
            if state['task'] is None: record_divergence(state, event['event_id'], 'missing_task', 'cannot accept before task exists'); continue
            if state['process_run'] is None or state['task']['process_run_id'] != state['process_run']['object_id'] or state['process_run']['status'] != 'active': record_divergence(state, event['event_id'], 'wrong_process', 'task must remain inside an active process run'); continue
            if state['task']['accepted_by'] is not None: record_divergence(state, event['event_id'], 'double_accept', {'existing': state['task']['accepted_by'], 'attempted': p['accepted_by']}); continue
            if not active_member(memberships, p['accepted_by'], state['task']['group_id']): record_divergence(state, event['event_id'], 'policy_denied', 'accepting actor lacks active membership'); continue
            state['task']['accepted_by'] = p['accepted_by']; state['task']['status'] = 'accepted'; state['commitments'][p['commitment_id']] = {'object_id': p['commitment_id'], 'task_id': p['task_id'], 'debtor_actor_id': p['accepted_by'], 'status': 'accepted', 'progress_percent': 0, 'satisfaction_ref': None}; applied.append(event['event_id'])
        elif et == 'task.progress_updated.v1':
            if state['task'] is None: record_divergence(state, event['event_id'], 'missing_task', 'cannot progress before task exists'); continue
            if state['process_run'] is None or state['task']['process_run_id'] != state['process_run']['object_id'] or state['process_run']['status'] != 'active': record_divergence(state, event['event_id'], 'wrong_process', 'task must remain inside an active process run'); continue
            if state['task']['accepted_by'] != p['updated_by']: record_divergence(state, event['event_id'], 'wrong_actor', {'authoritative_assignee': state['task']['accepted_by'], 'attempted_actor': p['updated_by']}); continue
            if state['task']['status'] == 'completed': record_divergence(state, event['event_id'], 'illegal_transition', 'cannot progress a completed task'); continue
            state['task']['status'] = p['resulting_task_status'];
            if state['task']['started_at'] is None: state['task']['started_at'] = event['time']
            cid = p['commitment_id']
            if cid in state['commitments']:
                state['commitments'][cid]['status'] = 'in_progress'; state['commitments'][cid]['progress_percent'] = p['progress_percent']
            applied.append(event['event_id'])
        elif et == 'task.assignment_overridden.v1':
            if state['task'] is None: record_divergence(state, event['event_id'], 'missing_task', 'cannot override assignment before task exists'); continue
            if state['process_run'] is None or state['task']['process_run_id'] != state['process_run']['object_id'] or state['process_run']['status'] != 'active': record_divergence(state, event['event_id'], 'wrong_process', 'task must remain inside an active process run'); continue
            if not active_capability(state, actor, 'task.assignment.override', state['task']['group_id'], state['task']['process_run_id'], when, state['task']['object_id']): record_divergence(state, event['event_id'], 'policy_denied', 'actor lacks task.assignment.override capability grant'); continue
            if state['task']['accepted_by'] != p['prior_assignee']: record_divergence(state, event['event_id'], 'assignee_mismatch', {'authoritative_assignee': state['task']['accepted_by'], 'prior_assignee': p['prior_assignee']}); continue
            if not active_member(memberships, p['new_assignee'], state['task']['group_id']): record_divergence(state, event['event_id'], 'policy_denied', 'new assignee lacks active membership'); continue
            prior_cid = p['prior_commitment_id']
            if prior_cid in state['commitments']:
                state['commitments'][prior_cid]['status'] = 'reassigned'; state['commitments'][prior_cid]['satisfaction_ref'] = 'override:reassigned'
            state['task']['accepted_by'] = p['new_assignee']; state['task']['status'] = 'accepted'; state['commitments'][p['new_commitment_id']] = {'object_id': p['new_commitment_id'], 'task_id': p['task_id'], 'debtor_actor_id': p['new_assignee'], 'status': 'accepted', 'progress_percent': 0, 'satisfaction_ref': None}; applied.append(event['event_id'])
        elif et == 'task.completed.v1':
            if state['task'] is None: record_divergence(state, event['event_id'], 'missing_task', 'cannot complete before task exists'); continue
            if state['process_run'] is None or state['task']['process_run_id'] != state['process_run']['object_id'] or state['process_run']['status'] != 'active': record_divergence(state, event['event_id'], 'wrong_process', 'task must remain inside an active process run'); continue
            normal_authority = state['task']['accepted_by'] == p['completed_by']
            override_authority = active_capability(state, actor, 'task.complete.override', state['task']['group_id'], state['task']['process_run_id'], when, state['task']['object_id'])
            if not (normal_authority or override_authority): record_divergence(state, event['event_id'], 'policy_denied', 'actor lacks normal completion authority or task.complete.override capability grant'); continue
            if state['task']['status'] == 'completed': record_divergence(state, event['event_id'], 'duplicate_completion', None); continue
            if p.get('completion_mode') == 'override' and not override_authority: record_divergence(state, event['event_id'], 'policy_denied', 'override completion requested without override capability'); continue
            if p.get('completion_mode') == 'normal' and not normal_authority: record_divergence(state, event['event_id'], 'wrong_actor', {'authoritative_assignee': state['task']['accepted_by'], 'attempted_actor': p['completed_by']}); continue
            state['task']['status'] = 'completed'
            if state['task']['started_at'] is None: state['task']['started_at'] = event['time']
            state['task']['completed_at'] = p['completed_at']
            cid = p['commitment_id']
            if cid in state['commitments']:
                if p.get('completion_mode') == 'override' and p['completed_by'] != state['task']['accepted_by']:
                    state['commitments'][cid]['status'] = 'released'; state['commitments'][cid]['satisfaction_ref'] = f"override:{p['outcome_ref']}" if p['outcome_ref'] else 'override'
                else:
                    state['commitments'][cid]['status'] = 'fulfilled'; state['commitments'][cid]['progress_percent'] = 100; state['commitments'][cid]['satisfaction_ref'] = p['outcome_ref']
            applied.append(event['event_id'])
        elif et == 'checkpoint.created.v1':
            expected_hash = hash_projection(projection_v2(state))
            if p['state_projection_name'] != PROJECTION_NAME: record_divergence(state, event['event_id'], 'checkpoint_hash_mismatch', {'reason':'projection_name_mismatch','expected':PROJECTION_NAME,'received':p['state_projection_name']}); continue
            if p['materialized_state_hash'] != expected_hash: record_divergence(state, event['event_id'], 'checkpoint_hash_mismatch', {'expected_hash': expected_hash, 'received_hash': p['materialized_state_hash']}); continue
            state['checkpoints'].append({'checkpoint_id': p['checkpoint_id'], 'state_projection_name': p['state_projection_name'], 'materialized_state_hash': p['materialized_state_hash'], 'reason': p['reason']}); applied.append(event['event_id'])
    report = {'events_applied': applied, 'state_projection_name': PROJECTION_NAME, 'authoritative_state': state, 'checkpoint_refs': state['checkpoints'], 'divergences': state['divergences']}
    report['state_hash'] = hash_projection(projection_v2(state))
    report['checkpoint_hash_consistent'] = None if not state['checkpoints'] else all(cp['materialized_state_hash'] == report['state_hash'] and cp['state_projection_name'] == PROJECTION_NAME for cp in state['checkpoints'])
    return report

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', required=True); ap.add_argument('--out', required=False); args = ap.parse_args()
    events = load_events(pathlib.Path(args.events)); report = reduce_events(events); data = json.dumps(report, indent=2) + '\n'
    if args.out:
        out_path = pathlib.Path(args.out); out_path.parent.mkdir(parents=True, exist_ok=True); out_path.write_text(data)
    print(data)

if __name__ == '__main__':
    main()
