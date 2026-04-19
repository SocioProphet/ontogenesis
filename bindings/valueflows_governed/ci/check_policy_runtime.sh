#!/usr/bin/env bash
set -euo pipefail
policy="policies/rego/task_flow_policy_v0_4.rego"
raw_eval() {
  local input="$1"
  local query="$2"
  opa eval -d "$policy" -i "$input" --format raw "$query"
}
test "$(raw_eval policies/rego/testdata/allow_task_offer_delegated.json 'data.socioprophet.valueflows.taskflow.v4.allow')" = "true"
test "$(raw_eval policies/rego/testdata/deny_task_offer_no_capability.json 'data.socioprophet.valueflows.taskflow.v4.allow')" = "false"
test "$(raw_eval policies/rego/testdata/allow_assignment_override.json 'data.socioprophet.valueflows.taskflow.v4.allow')" = "true"
test "$(raw_eval policies/rego/testdata/deny_assignment_override_no_capability.json 'data.socioprophet.valueflows.taskflow.v4.allow')" = "false"
test "$(raw_eval policies/rego/testdata/allow_complete_override.json 'data.socioprophet.valueflows.taskflow.v4.allow')" = "true"
echo "OPA policy runtime checks passed."
