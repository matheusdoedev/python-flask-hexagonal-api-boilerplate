.PHONY: install run test lint audit

install:
	python -m pip install -e ".[dev]"

run:
	flask --app app:create_app run --debug

test:
	pytest --cov=src --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .
	mypy src

audit:
	pip-audit

create-venv:
	python -m venv .venv

activate:
	. .venv/bin/activate
