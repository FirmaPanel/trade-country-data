PYTHON ?= python3

.PHONY: build check coverage npm-check npm-pack pypi-build pypi-check report-coverage test validate validate-schemas

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

npm-check:
	cd packages/npm && npm run check

npm-pack:
	cd packages/npm && npm run pack:check

pypi-check:
	cd packages/pypi && $(PYTHON) scripts/build_package.py
	cd packages/pypi && $(PYTHON) scripts/build_package.py --check
	cd packages/pypi && $(PYTHON) scripts/check_version.py
	cd packages/pypi && PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

pypi-build: pypi-check
	cd packages/pypi && $(PYTHON) -m build

check:
	$(PYTHON) scripts/build_csv.py --check
	$(PYTHON) scripts/report_coverage.py --check
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/validate_schemas.py
	$(PYTHON) -m unittest discover -s tests -v
