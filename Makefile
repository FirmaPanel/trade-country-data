PYTHON ?= python3

.PHONY: build check coverage report-coverage test validate validate-schemas

build:
	$(PYTHON) scripts/build_csv.py

validate:
	$(PYTHON) scripts/validate.py

validate-schemas:
	$(PYTHON) scripts/validate_schemas.py

report-coverage:
	$(PYTHON) scripts/report_coverage.py

test:
	$(PYTHON) -m unittest discover -s tests -v

coverage:
	$(PYTHON) -m coverage erase
	$(PYTHON) -m coverage run -m unittest discover -s tests -v
	$(PYTHON) -m coverage report

check:
	$(PYTHON) scripts/build_csv.py --check
	$(PYTHON) scripts/report_coverage.py --check
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/validate_schemas.py
	$(PYTHON) -m unittest discover -s tests -v
