all: flake8 pylint coverage
.PHONY: all

flake8:
	flake8 bin/snapd-wait tests setup.py
.PHONY: flake8

pytest_tests:
	pylint tests --disable=missing-function-docstring,missing-module-docstring
.PHONY: pytest_tests

pytest_script:
	pylint bin/snapd-wait setup.py
.PHONY: pytest_script

pylint: pytest_script pytest_tests
.PHONY: pylint

test:
	PYTHONPPATH=. pytest tests
.PHONY: test

coverage:
	PYTHONPATH=. pytest --cov=script --cov-report=term-missing --cov-fail-under=100 tests
.PHONY: coverage
