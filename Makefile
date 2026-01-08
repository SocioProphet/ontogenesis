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
