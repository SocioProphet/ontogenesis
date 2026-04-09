.PHONY: venv deps validate shacl jsonld build ledger verify sbom all

venv:
	python -m venv .venv

deps:
	.venv/bin/pip install -r requirements-dev.txt

validate:
	.venv/bin/python scripts/validate_rdf.py

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

all: validate shacl jsonld build ledger verify sbom
