#!/usr/bin/env bash
set -euo pipefail
echo "Python validation and replay checks already executed by make targets."
if command -v opa >/dev/null 2>&1; then
  bash ci/check_policy_runtime.sh
else
  echo "opa binary not found in local sandbox; skipping runtime Rego execution."
fi
