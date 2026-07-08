# ML Platform Template

A reusable production-ready machine learning project template for building reliable, testable, and maintainable ML and AI systems.

This template provides a standard foundation for future machine learning projects, including configuration management, logging, testing, linting, type checking, Docker support, and CI/CD readiness.

## Project Goals

This template is designed to support machine learning projects that need to be:

- reproducible
- testable
- configurable
- maintainable
- container-ready
- CI/CD-ready
- safe to extend into production workflows

## Project Structure

```text
fraud-detection-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── configs/
│   ├── base.yaml
│   ├── development.yaml
│   ├── production.yaml
│   └── logging.yaml
├── docs/
│   ├── adr/
│   ├── architecture/
│   └── engineering-journal/
├── src/
│   └── fraud_detection_platform/
│       ├── config/
│       │   └── settings.py
│       └── logging/
│           └── logger.py
├── tests/
│   ├── test_logger.py
│   ├── test_package.py
│   └── test_settings.py
├── .dockerignore
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── Dockerfile
├── Makefile
├── README.md
└── pyproject.toml
```

## Core Features

This template includes:

- Python 3.12 project setup
- `src/` package layout
- `pyproject.toml` project configuration
- optional dependency groups
- environment-based YAML configuration
- reusable logging utilities
- Ruff linting and formatting
- Pytest test suite
- MyPy type checking
- pre-commit hooks
- Makefile automation
- GitHub Actions CI workflow
- Docker runtime support
- documentation structure for architecture notes, ADRs, and engineering journals

## Development Setup

Create and activate a Python 3.12 virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
make install
```

## Development Commands

This project uses a `Makefile` to standardize common development workflows.

| Command | Purpose |
|---|---|
| `make install` | Install development and configuration dependencies |
| `make install-all` | Install development, ML, API, and monitoring dependencies |
| `make lint` | Run Ruff linting |
| `make format` | Format Python code with Ruff |
| `make test` | Run the Pytest test suite |
| `make type-check` | Run MyPy type checks |
| `make quality` | Run linting, tests, and type checks |
| `make clean` | Remove generated caches and build artifacts |

Before committing changes, run:

```bash
make quality
```

## Configuration

Configuration files are stored in the `configs/` directory.

```text
configs/
├── base.yaml
├── development.yaml
├── production.yaml
└── logging.yaml
```

The template separates shared configuration from environment-specific overrides.

`base.yaml` contains default project settings.

`development.yaml` contains local development overrides.

`production.yaml` contains production-oriented overrides.

`logging.yaml` contains logging configuration.

Example usage:

```python
from fraud_detection_platform.config.settings import load_settings

settings = load_settings("development")

print(settings.app.name)
print(settings.runtime.environment)
```

## Logging

Reusable logging utilities are available from:

```python
from fraud_detection_platform.logging import get_logger, setup_logging

setup_logging()

logger = get_logger(__name__)
logger.info("Application started")
```

Logging is configured through:

```text
configs/logging.yaml
```

If no logging config file is found, the project falls back to a basic logging setup.

## Quality Checks

Run the full local quality gate:

```bash
make quality
```

This runs:

- Ruff linting
- Pytest tests
- MyPy type checks

The current quality gate should pass before changes are committed.

## Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

Pre-commit helps catch formatting, linting, YAML, TOML, whitespace, and file-ending issues before commits are created.

## Docker

This project includes a `Dockerfile` so the template can run in a clean Linux container, independent of the local machine setup.

### Build the Docker image

```bash
docker build -t fraud-detection-platform .
```

### Run quality checks inside Docker

```bash
docker run --rm fraud-detection-platform
```

By default, the container runs:

```bash
make quality
```

This verifies that linting, tests, and type checks pass inside the Docker environment.

### Why Docker is used

Docker helps ensure the project runs consistently across environments such as:

- local development
- CI/CD runners
- AWS container services
- Databricks-compatible workflows
- future Kubernetes deployments

The local `.venv` is not copied into Docker. The container installs its own dependencies because the container itself provides isolation and runs on Linux.

## CI/CD

The project includes a GitHub Actions workflow at:

```text
.github/workflows/ci.yml
```

The CI workflow runs on pushes to `main` and on pull requests.

It performs the same quality gate used locally:

```bash
make quality
```

This helps ensure that code passing locally also passes in a clean CI environment.

## Documentation

The `docs/` directory is used to capture design decisions and engineering notes.

```text
docs/
├── adr/
├── architecture/
└── engineering-journal/
```

### ADRs

Architecture Decision Records explain important technical decisions, trade-offs, and alternatives considered.

### Architecture Notes

Architecture documentation describes how the system is structured and how its components interact.

### Engineering Journal

The engineering journal captures implementation reasoning, lessons learned, and interview-ready explanations.

## Secrets Policy

Never commit real secrets, passwords, API keys, tokens, private keys, or cloud credentials.

Use `.env.example` to document required environment variables, but keep real values in local `.env` files or managed secret stores.

Recommended secret management options include:

- AWS Secrets Manager
- Azure Key Vault
- Databricks Secret Scopes
- GitHub Actions Secrets

## What Should Not Be Committed

Avoid committing generated or local-only files such as:

- `.venv/`
- `build/`
- `dist/`
- `*.egg-info/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- raw datasets
- model binaries
- logs
- local `.env` files

These should be handled through `.gitignore` and `.dockerignore`.

## Template Usage

This repository is intended to serve as a reusable foundation for multiple machine learning and AI projects.

Future projects can copy this template and then customize:

- package name
- project metadata
- configuration values
- dependencies
- ML pipeline code
- API services
- data processing workflows
- cloud deployment infrastructure
- monitoring and observability components

## Target Project Types

This template can support projects such as:

- real-time fraud detection
- credit risk modeling
- patient readmission prediction
- clinical NLP systems
- customer churn prediction
- AI support ticket triage and RAG assistants

## Engineering Principle

The goal of this template is not only to make code run.

The goal is to create a professional ML engineering foundation that is reproducible, observable, testable, maintainable, and ready to grow into production systems.
