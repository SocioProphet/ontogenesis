.PHONY: venv deps validate validate-corpus-event-semantics validate-registry-discovery validate-privacy-nonlinkability validate-memory-representation-strata validate-adversarial-scenario shacl jsonld build ledger verify sbom svf all

venv:
	python -m venv .venv

deps:
	.venv/bin/pip install -r requirements-dev.txt

validate: validate-corpus-event-semantics validate-registry-discovery validate-privacy-nonlinkability validate-memory-representation-strata validate-adversarial-scenario
	.venv/bin/python scripts/validate_rdf.py

validate-corpus-event-semantics:
	.venv/bin/python scripts/validate_corpus_event_semantics.py

validate-adversarial-scenario:
	.venv/bin/python scripts/validate_adversarial_scenario_examples.py

validate-registry-discovery:
	.venv/bin/python scripts/validate_registry_discovery.py

validate-privacy-nonlinkability:
	.venv/bin/python scripts/validate_privacy_nonlinkability_examples.py

validate-memory-representation-strata:
	.venv/bin/python scripts/validate_memory_representation_strata_examples.py

shacl:
	.venv/bin/python scripts/shacl_gate.py

jsonld:
	.venv/bin/python scripts/jsonld_roundtrip.py

build:
	.venv/bin/python scripts/build_dist.py

ledger:
	.venv/bin/python scripts/ledger_build.py

verify:
	.venv/bin/python scripts/ledger_verify.py

sbom:
	.venv/bin/python scripts/spdx_emit.py

svf:
	.venv/bin/python scripts/validate_svf_contracts.py

all: validate shacl jsonld build ledger verify sbom svf
