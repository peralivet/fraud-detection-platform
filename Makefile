.PHONY: install install-all lint format test type-check quality clean

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev,config]"

install-all:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev,config,ml,api,monitoring]"

lint:
	ruff check .

format:
	ruff format .

test:
	pytest

type-check:
	mypy src tests

quality: lint test type-check

clean:
	rm -rf build dist
	rm -rf *.egg-info src/*.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
