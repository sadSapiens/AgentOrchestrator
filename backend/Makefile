.PHONY: test lint format install

install:
	pip install -r requirements.txt

test:
	pytest

lint:
	flake8 .
	black . --check
	isort . --check-only

format:
	black .
	isort .
