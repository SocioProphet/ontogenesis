<<<<<<< HEAD
.PHONY: help validate shacl sparql

help:
	@printf "%s\n" \
	  "Targets:" \
	  "  make validate  - run SHACL + SPARQL sanity checks" \
	  "  make shacl     - run SHACL validation (pyshacl)" \
	  "  make sparql    - run SPARQL tests (rdflib)"

validate: shacl sparql

shacl:
	python3 tools/validate.py --shacl

sparql:
	python3 tools/validate.py --sparql
=======
.PHONY: validate shacl venv

venv:
	python3 -m venv .venv
	./.venv/bin/python -m pip install -U pip wheel setuptools
	./.venv/bin/python -m pip install -r requirements.txt

validate:
	./.venv/bin/python tools/validate.py --shacl 2>/dev/null || python3 tools/validate.py --shacl

shacl:
	./.venv/bin/python tools/validate.py --shacl 2>/dev/null || python3 tools/validate.py --shacl
>>>>>>> cbab0fe (init: ontogenesis (ttl+shacl+tests+capd) with venv-aware validate gate)
