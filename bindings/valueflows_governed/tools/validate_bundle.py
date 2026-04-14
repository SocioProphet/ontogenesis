#!/usr/bin/env python3
import json
import pathlib
import sys
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / 'schemas'
DATA_ROOT = ROOT / 'data'
FIXTURE_ROOT = ROOT / 'fixtures'

CANONICAL = json.loads((SCHEMA_ROOT / 'canonical-schemas.v1.json').read_text())
ENV_SCHEMA = json.loads((SCHEMA_ROOT / 'event-envelope.v1.schema.json').read_text())
EVENT_PAYLOADS = json.loads((SCHEMA_ROOT / 'event-payload-schemas.v1.json').read_text())
ENV_VALIDATOR = Draft202012Validator(ENV_SCHEMA)

EVENT_MAP = {
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

def validate_object(item):
    source = item['source']
    data = item['data']
    errs = []
    schema_name = {
        'Actor': 'actor.v1.schema.json',
        'Group': 'group.v1.schema.json',
        'Role': 'role.v1.schema.json',
        'Membership': 'membership.v1.schema.json',
        'ProcessRun': 'process-run.v1.schema.json',
        'Task': 'task.v1.schema.json',
        'Commitment': 'commitment.v1.schema.json',
        'Delegation': 'delegation.v1.schema.json',
        'CapabilityGrant': 'capability-grant.v1.schema.json',
        'PolicyDecision': 'policy-decision.v1.schema.json',
        'EvidencePack': 'evidence-pack.v1.schema.json',
        'CairnCheckpoint': 'cairn-checkpoint.v1.schema.json',
    }.get(data.get('object_type'))
    if not schema_name:
        errs.append({'where':'dispatch','message':f"unknown object_type {data.get('object_type')!r}"})
        return source, errs
    schema = CANONICAL[schema_name]
    for e in Draft202012Validator(schema).iter_errors(data):
        errs.append({'where': data.get('object_type'), 'message': e.message})
    return source, errs

def validate_event(event, source):
    errs = []
    for e in ENV_VALIDATOR.iter_errors(event):
        errs.append({'where':'envelope','message':e.message})
    payload_schema_name = EVENT_MAP.get(event.get('type'))
    if payload_schema_name is None:
        errs.append({'where':'payload','message':f"unsupported event type {event.get('type')!r}"})
    else:
        payload_schema = EVENT_PAYLOADS[payload_schema_name]
        for e in Draft202012Validator(payload_schema).iter_errors(event.get('payload', {})):
            errs.append({'where':'payload','message':e.message})
    return source, errs

def main():
    results=[]
    failures=0
    for item in json.loads((DATA_ROOT/'reference_objects.json').read_text()):
        source, errs = validate_object(item)
        results.append({'file': source, 'ok': not errs, 'errors': errs})
        failures += bool(errs)
    for name in ['linear.events.ndjson','assignment_override.events.ndjson','divergence.events.ndjson']:
        for idx, line in enumerate((FIXTURE_ROOT/name).read_text().splitlines(), start=1):
            line=line.strip()
            if not line:
                continue
            event = json.loads(line)
            source = f"{name}:{idx}"
            source, errs = validate_event(event, source)
            results.append({'file': source, 'ok': not errs, 'errors': errs})
            failures += bool(errs)
    out={'checked':len(results),'failures':failures,'results':results}
    rp=ROOT/'reports'; rp.mkdir(exist_ok=True)
    (rp/'validation_report.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
    sys.exit(1 if failures else 0)

if __name__ == '__main__':
    main()
