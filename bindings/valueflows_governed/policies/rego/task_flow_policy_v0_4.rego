package socioprophet.valueflows.taskflow.v4

default allow := false

action := input.action

active_membership(actor_id, group_id) if {
  some m in input.memberships
  m.actor_id == actor_id
  m.group_id == group_id
  m.status == "active"
}

has_role(actor_id, group_id, wanted) if {
  some m in input.memberships
  m.actor_id == actor_id
  m.group_id == group_id
  m.status == "active"
  some r in m.role_ids
  r == wanted
}

process_creator_or_coordinator(actor_id, group_id) if {
  active_membership(actor_id, group_id)
  has_role(actor_id, group_id, "role:coordinator")
}

process_creator_or_coordinator(actor_id, group_id) if {
  active_membership(actor_id, group_id)
  input.process_run.created_by == actor_id
}

active_delegation(actor_id, group_id, process_run_id, task_id) if {
  some d in input.delegations
  d.status == "active"
  d.grantee_actor_id == actor_id
  d.group_id == group_id
  d.process_run_id == process_run_id
  d.task_id == null
}

active_delegation(actor_id, group_id, process_run_id, task_id) if {
  some d in input.delegations
  d.status == "active"
  d.grantee_actor_id == actor_id
  d.group_id == group_id
  d.process_run_id == process_run_id
  d.task_id == task_id
}

active_capability(actor_id, capability, group_id, process_run_id, task_id) if {
  some g in input.capability_grants
  g.status == "active"
  g.grantee_actor_id == actor_id
  g.capability == capability
  g.group_id == group_id
  g.process_run_id == process_run_id
  g.task_id == null
  active_delegation(actor_id, group_id, process_run_id, task_id)
}

active_capability(actor_id, capability, group_id, process_run_id, task_id) if {
  some g in input.capability_grants
  g.status == "active"
  g.grantee_actor_id == actor_id
  g.capability == capability
  g.group_id == group_id
  g.process_run_id == process_run_id
  g.task_id == task_id
  active_delegation(actor_id, group_id, process_run_id, task_id)
}

allow if {
  action == "processrun.create"
  active_membership(input.actor_id, input.process_run.group_id)
  has_role(input.actor_id, input.process_run.group_id, "role:coordinator")
}

allow if {
  action == "delegation.issue"
  process_creator_or_coordinator(input.actor_id, input.delegation.group_id)
  input.delegation.grantor_actor_id == input.actor_id
  input.process_run.status == "active"
  input.delegation.process_run_id == input.process_run.object_id
}

allow if {
  action == "capabilitygrant.issue"
  process_creator_or_coordinator(input.actor_id, input.capability_grant.group_id)
  input.capability_grant.grantor_actor_id == input.actor_id
  input.process_run.status == "active"
  input.capability_grant.process_run_id == input.process_run.object_id
}

allow if {
  action == "task.offer"
  input.task.status == "offered"
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  active_membership(input.actor_id, input.task.group_id)
  (process_creator_or_coordinator(input.actor_id, input.task.group_id) or
   active_capability(input.actor_id, "task.offer", input.task.group_id, input.process_run.object_id, input.task.object_id))
}

allow if {
  action == "commitment.accept"
  input.task.status == "offered"
  input.task.accepted_by == null
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  active_membership(input.actor_id, input.task.group_id)
}

allow if {
  action == "task.assignment_override"
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  active_capability(input.actor_id, "task.assignment.override", input.task.group_id, input.process_run.object_id, input.task.object_id)
}

allow if {
  action == "task.progress_update"
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  input.actor_id == input.task.accepted_by
  input.payload.progress_percent >= 0
  input.payload.progress_percent <= 100
}

allow if {
  action == "task.complete"
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  input.actor_id == input.task.accepted_by
  input.payload.completion_mode == "normal"
}

allow if {
  action == "task.complete"
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  input.payload.completion_mode == "override"
  active_capability(input.actor_id, "task.complete.override", input.task.group_id, input.process_run.object_id, input.task.object_id)
}

deny_reasons contains "actor lacks active membership" if {
  some group_id
  group_id := object.get(input.task, "group_id", object.get(input.process_run, "group_id", null))
  group_id != null
  not active_membership(input.actor_id, group_id)
}

deny_reasons contains "process run is not active" if {
  action != "processrun.create"
  input.process_run.status != "active"
}

deny_reasons contains "actor lacks delegated task.offer capability" if {
  action == "task.offer"
  input.task.process_run_id == input.process_run.object_id
  input.process_run.status == "active"
  active_membership(input.actor_id, input.task.group_id)
  not process_creator_or_coordinator(input.actor_id, input.task.group_id)
  not active_capability(input.actor_id, "task.offer", input.task.group_id, input.process_run.object_id, input.task.object_id)
}

deny_reasons contains "actor lacks task.assignment.override capability grant" if {
  action == "task.assignment_override"
  not active_capability(input.actor_id, "task.assignment.override", input.task.group_id, input.process_run.object_id, input.task.object_id)
}

deny_reasons contains "actor lacks completion authority" if {
  action == "task.complete"
  input.payload.completion_mode == "override"
  not active_capability(input.actor_id, "task.complete.override", input.task.group_id, input.process_run.object_id, input.task.object_id)
}
