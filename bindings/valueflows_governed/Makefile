PYTHON ?= python3

validate-bundle:
	$(PYTHON) tools/validate_bundle.py

replay-linear:
	$(PYTHON) tools/materialize_task_flow.py --events fixtures/linear.events.ndjson --out reports/materialize_linear.json

replay-assignment-override:
	$(PYTHON) tools/materialize_task_flow.py --events fixtures/assignment_override.events.ndjson --out reports/materialize_assignment_override.json

replay-divergence:
	$(PYTHON) tools/materialize_task_flow.py --events fixtures/divergence.events.ndjson --out reports/materialize_divergence.json

check-expected:
	$(PYTHON) tools/check_expected_reports.py

validate-terminal-lockout:
	$(PYTHON) tools/validate_terminal_lockout_fixture.py

ci-local: validate-bundle replay-linear replay-assignment-override replay-divergence check-expected validate-terminal-lockout
	bash ci/run_local_ci.sh
