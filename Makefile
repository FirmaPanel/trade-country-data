PYTHON ?= python3

.PHONY: build check validate validate-schemas

build:
	$(PYTHON) scripts/build_csv.py

validate:
	$(PYTHON) scripts/validate.py

validate-schemas:
	$(PYTHON) scripts/validate_schemas.py

check:
	$(PYTHON) scripts/build_csv.py --check
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/validate_schemas.py
