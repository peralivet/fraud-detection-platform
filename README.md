# Real-Time Fraud Detection Platform

A production-style machine learning platform for detecting potentially fraudulent financial transactions using batch scoring, real-time inference, monitoring, and cloud-ready engineering practices.

This project is part of a senior-level machine learning engineering portfolio. It is designed to demonstrate how fraud detection systems can be built with reliable software engineering foundations, not just model notebooks.

## Project Goals

This project is designed to support:

- transaction fraud detection
- supervised machine learning model training
- batch fraud scoring
- real-time API-based fraud scoring
- model evaluation and experiment tracking
- monitoring for model quality and data drift
- production-style configuration and logging
- Docker-based runtime portability
- CI/CD-ready development workflows
- future AWS and Databricks deployment paths

## Business Problem

Financial platforms process large volumes of transactions every day. Some transactions may be fraudulent, but fraud is usually rare compared with normal activity.

The business goal is to identify suspicious transactions early while reducing unnecessary false positives that may block legitimate customers.

A practical fraud detection system must balance:

- fraud capture rate
- false positive rate
- customer experience
- model latency
- explainability
- monitoring
- operational reliability

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
│   ├── engineering-journal/
│   └── template-usage.md
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

## Current Foundation

The project currently includes:

- Python 3.12 project setup
- `src/` package layout
- `pyproject.toml` project configuration
- optional dependency groups
- YAML-based configuration management
- reusable logging utilities
- Ruff linting and formatting
- Pytest test suite
- MyPy type checking
- pre-commit hooks
- Makefile automation
- GitHub Actions CI workflow
- Docker runtime support
- documentation structure for architecture notes, ADRs, and engineering journals

## Planned ML Platform Capabilities

This project will evolve to include:

- transaction data ingestion
- exploratory data analysis
- fraud-focused feature engineering
- class imbalance handling
- baseline ML models
- advanced fraud detection models
- model evaluation with fraud-specific metrics
- model explainability
- MLflow experiment tracking
- batch inference pipeline
- FastAPI real-time scoring endpoint
- monitoring for drift and model performance
- Databricks workflow integration
- AWS deployment path
- dashboard/reporting layer

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

## Docker

This project includes a `Dockerfile` so the project can run in a clean Linux container, independent of the local machine setup.

Build the Docker image:

```bash
docker build -t fraud-detection-platform .
```

Run quality checks inside Docker:

```bash
docker run --rm fraud-detection-platform
```

By default, the container runs:

```bash
make quality
```

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

Architecture documentation describes how the fraud detection system is structured and how its components interact.

### Engineering Journal

The engineering journal captures implementation reasoning, lessons learned, debugging notes, and interview-ready explanations.

## Secrets Policy

Never commit real secrets, passwords, API keys, tokens, private keys, or cloud credentials.

Use `.env.example` to document required environment variables, but keep real values in local `.env` files or managed secret stores.

Recommended secret management options include:

- AWS Secrets Manager
- Azure Key Vault
- Databricks Secret Scopes
- GitHub Actions Secrets

## Engineering Principle

The goal of this project is not only to train a fraud model.

The goal is to build a production-style ML system that is reproducible, testable, configurable, observable, and ready to evolve into cloud-based deployment workflows.
