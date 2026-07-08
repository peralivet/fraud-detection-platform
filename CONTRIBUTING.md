# Contributing Guide

This project follows a production-style development workflow for machine learning and AI systems.

The goal is to keep the project reproducible, testable, maintainable, and safe to evolve.

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

This project uses a `Makefile` to standardize common workflows.

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

## Pre-commit Hooks

This project uses pre-commit hooks to catch formatting and quality issues before commits are created.

Install the hooks:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

If pre-commit modifies files, review the changes, stage the files again, and recommit.

## Git Commit Style

Use clear, conventional commit messages.

Examples:

```text
feat: add configuration management
fix: correct logging setup
docs: update README
test: add model validation tests
build: add Docker runtime
ci: add GitHub Actions workflow
chore: clean generated files
```

Keep commits focused. Each commit should represent one meaningful change.

## Branching

For feature work, create a branch:

```bash
git checkout -b feat/my-feature
```

Avoid doing major feature work directly on `main` once the project is pushed to GitHub.

## Secrets

Never commit secrets, passwords, API keys, tokens, private keys, or cloud credentials.

Use secure secret management tools such as:

- `.env` files for local development
- AWS Secrets Manager
- Azure Key Vault
- Databricks Secret Scopes
- GitHub Actions Secrets

The repository should include `.env.example`, but never a real `.env` file.

## Generated Files

Do not commit generated or local-only artifacts such as:

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
- local environment files

These files should be ignored through `.gitignore`.

## Docker Workflow

Build the Docker image:

```bash
docker build -t fraud-detection-platform .
```

Run the default quality checks inside Docker:

```bash
docker run --rm fraud-detection-platform
```

Docker should not copy the local `.venv` into the image. The container installs its own dependencies because the container itself provides isolation.

## Pull Request Expectations

Before opening a pull request:

1. Run `make quality`.
2. Ensure tests pass.
3. Update documentation if behavior changed.
4. Keep the pull request focused.
5. Explain what changed and why.

## Engineering Principles

This project follows these principles:

- Design before implementation.
- Separate code from configuration.
- Keep secrets out of source control.
- Automate repeatable workflows.
- Test important behavior.
- Prefer clear structure over clever code.
- Make the correct workflow easy to follow.
- Document decisions, not just code.
