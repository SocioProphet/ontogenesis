.PHONY: venv deps validate shacl jsonld build ledger verify sbom all

venv:
	python -m venv .venv

deps:
	. .venv/bin/activate && pip install -r requirements-dev.txt

validate:
	python scripts/validate_rdf.py

shacl:
	python scripts/shacl_gate.py

jsonld:
	python scripts/jsonld_roundtrip.py

build:
	python scripts/build_dist.py

ledger:
	python scripts/ledger_build.py

verify:
	python scripts/ledger_verify.py

sbom:
	python scripts/spdx_emit.py

all: validate shacl jsonld build ledger verify sbom
