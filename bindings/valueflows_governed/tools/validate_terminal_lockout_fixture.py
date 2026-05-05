#!/usr/bin/env python3
"""Validate terminal/revocation lockout behavior for the ValueFlows governed lane.

This is intentionally narrow. It proves that:
- revoking a capability grant blocks delegated task offer;
- revoking the parent delegation closes delegated authority;
- completing a process run blocks later task offer, even from the coordinator.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "terminal_lockout.events.ndjson"
EXPECTED = ROOT / "fixtures" / "terminal_lockout.expected.json"
REPORT = ROOT / "reports" / "terminal_lockout_report.json"
MEMBERSHIPS = [
    {"actor_id": "actor:tibi", "group_id": "group:leaknet", "status": "active", "role_ids": ["role:coordinator"]},
    {"actor_id": "actor:worker-1", "group_id": "group:leaknet", "status": "active", "role_ids": ["role:contributor"]},
    {"actor_id": "actor:worker-2", "group_id": "group:leaknet", "status": "active", "role_ids": ["role:contributor"]},
]

def load_ndjson(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def active_member(actor_id, group_id):
    return any(m["actor_id"] == actor_id and m["group_id"] == group_id and m["status"] == "active" for m in MEMBERSHIPS)

def has_role(actor_id, group_id, role):
    return any(m["actor_id"] == actor_id and m["group_id"] == group_id and m["status"] == "active" and role in m.get("role_ids", []) for m in MEMBERSHIPS)

def in_window(when, start, end):
    return when >= start and (end is None or when <= end)

def reduce(events):
    state = {"process_run": None, "delegations": {}, "capability_grants": {}, "divergences": []}
    applied = []

    def divergence(event, reason, details):
        state["divergences"].append({"event_id": event["event_id"], "reason": reason, "details": details})

    def active_capability(actor_id, capability, group_id, process_run_id, when, task_id=None):
        for grant in state["capability_grants"].values():
            if grant["status"] != "active":
                continue
            if grant["grantee_actor_id"] != actor_id or grant["capability"] != capability:
                continue
            if grant["group_id"] != group_id or grant["process_run_id"] != process_run_id:
                continue
            if grant.get("task_id") not in (None, task_id):
                continue
            if not in_window(when, grant["valid_from"], grant.get("valid_until")):
                continue
            delegation = state["delegations"].get(grant["delegation_id"])
            if not delegation or delegation["status"] != "active":
                continue
            if delegation["grantee_actor_id"] != actor_id:
                continue
            if delegation["group_id"] != group_id or delegation["process_run_id"] != process_run_id:
                continue
            if not in_window(when, delegation["valid_from"], delegation.get("valid_until")):
                continue
            return True
        return False

    for event in events:
        event_type = event["type"]
        actor_id = event["actor_id"]
        when = event["time"]
        payload = event["payload"]
        process_run = state["process_run"]

        if event_type == "processrun.created.v1":
            if not active_member(actor_id, payload["group_id"]) or not has_role(actor_id, payload["group_id"], "role:coordinator"):
                divergence(event, "policy_denied", "only active coordinators may create process runs")
                continue
            state["process_run"] = {
                "object_id": payload["process_run_id"],
                "group_id": payload["group_id"],
                "created_by": payload["created_by"],
                "status": "active",
            }
            applied.append(event["event_id"])

        elif event_type == "delegation.issued.v1":
            if not process_run or process_run["object_id"] != payload["process_run_id"] or process_run["status"] != "active":
                divergence(event, "wrong_process", "delegation must reference an active process run")
                continue
            state["delegations"][payload["delegation_id"]] = {
                "object_id": payload["delegation_id"],
                "grantor_actor_id": payload["grantor_actor_id"],
                "grantee_actor_id": payload["grantee_actor_id"],
                "group_id": payload["group_id"],
                "process_run_id": payload["process_run_id"],
                "valid_from": payload["valid_from"],
                "valid_until": payload.get("valid_until"),
                "status": "active",
            }
            applied.append(event["event_id"])

        elif event_type == "capabilitygrant.issued.v1":
            delegation = state["delegations"].get(payload["delegation_id"])
            if not delegation or delegation["status"] != "active":
                divergence(event, "missing_delegation", "capability grant requires an active delegation")
                continue
            state["capability_grants"][payload["capability_grant_id"]] = {
                "object_id": payload["capability_grant_id"],
                "delegation_id": payload["delegation_id"],
                "grantor_actor_id": payload["grantor_actor_id"],
                "grantee_actor_id": payload["grantee_actor_id"],
                "group_id": payload["group_id"],
                "process_run_id": payload["process_run_id"],
                "task_id": payload.get("task_id"),
                "capability": payload["capability"],
                "valid_from": payload["valid_from"],
                "valid_until": payload.get("valid_until"),
                "status": "active",
            }
            applied.append(event["event_id"])

        elif event_type == "capabilitygrant.revoked.v1":
            grant = state["capability_grants"].get(payload["capability_grant_id"])
            if not grant:
                divergence(event, "missing_capability_grant", "cannot revoke missing capability grant")
                continue
            grant["status"] = "revoked"
            grant["revoked_at"] = payload["revoked_at"]
            grant["revoked_by"] = payload["revoked_by"]
            applied.append(event["event_id"])

        elif event_type == "delegation.revoked.v1":
            delegation = state["delegations"].get(payload["delegation_id"])
            if not delegation:
                divergence(event, "missing_delegation", "cannot revoke missing delegation")
                continue
            delegation["status"] = "revoked"
            delegation["revoked_at"] = payload["revoked_at"]
            delegation["revoked_by"] = payload["revoked_by"]
            applied.append(event["event_id"])

        elif event_type == "processrun.completed.v1":
            if not process_run or process_run["object_id"] != payload["process_run_id"]:
                divergence(event, "wrong_process", "process completion must reference the active process run")
                continue
            process_run["status"] = "completed"
            process_run["completed_at"] = payload["completed_at"]
            applied.append(event["event_id"])

        elif event_type == "task.offered.v1":
            if not process_run or process_run["object_id"] != payload["process_run_id"] or process_run["status"] != "active":
                divergence(event, "wrong_process", "task must reference an active process run")
                continue
            has_base_authority = has_role(actor_id, payload["group_id"], "role:coordinator") or actor_id == process_run["created_by"]
            has_delegated_authority = active_capability(actor_id, "task.offer", payload["group_id"], payload["process_run_id"], when, payload["task_id"])
            if not (has_base_authority or has_delegated_authority):
                divergence(event, "policy_denied", "actor lacks coordinator/process authority or task.offer capability grant")
                continue
            applied.append(event["event_id"])

        else:
            divergence(event, "unsupported_event", event_type)

    return {"events_applied": applied, "terminal_state": state, "divergences": state["divergences"]}

def main():
    expected = json.loads(EXPECTED.read_text())
    report = reduce(load_ndjson(FIXTURE))
    errors = []
    if report["events_applied"] != expected["expected_events_applied"]:
        errors.append({"field": "events_applied", "actual": report["events_applied"], "expected": expected["expected_events_applied"]})
    if report["divergences"] != expected["expected_divergences"]:
        errors.append({"field": "divergences", "actual": report["divergences"], "expected": expected["expected_divergences"]})
    terminal = expected["expected_terminal_state"]
    process_run = report["terminal_state"]["process_run"]
    delegation = report["terminal_state"]["delegations"].get("delegation:tibi-worker2-task-admin")
    grant = report["terminal_state"]["capability_grants"].get("capabilitygrant:worker-2:task-offer")
    if process_run.get("status") != terminal["process_run_status"]:
        errors.append({"field": "process_run.status", "actual": process_run.get("status"), "expected": terminal["process_run_status"]})
    if delegation.get("status") != terminal["delegation_status"]:
        errors.append({"field": "delegation.status", "actual": delegation.get("status"), "expected": terminal["delegation_status"]})
    if grant.get("status") != terminal["capability_grant_status"]:
        errors.append({"field": "capability_grant.status", "actual": grant.get("status"), "expected": terminal["capability_grant_status"]})
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({"ok": not errors, "report": report, "errors": errors}, indent=2) + "\n")
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        sys.exit(1)
    print(json.dumps({"ok": True, "report_path": str(REPORT)}, indent=2))

if __name__ == "__main__":
    main()
