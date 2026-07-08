# Template Usage Guide

This document explains how to reuse this template for a new machine learning or AI project.

The goal is to copy the template safely while renaming project-specific files, package names, configuration values, and documentation.

## Reuse Checklist

When creating a new project from this template, update the following items.

## 1. Repository Folder Name

Rename the copied project folder to match the target project.

Examples:

```text
fraud-detection-platform
credit-risk-platform
patient-readmission
clinical-nlp
customer-churn
support-rag
```

## 2. Python Package Name

Rename the package directory under `src/`.

Example:

```text
src/fraud_detection_platform/
```

becomes:

```text
src/fraud_detection_platform/
```

Use lowercase snake_case for Python package names.

Examples:

```text
fraud_detection_platform
credit_risk_platform
patient_readmission
clinical_nlp
customer_churn
support_rag
```

## 3. Update Python Imports

After renaming the package directory, update imports across the project.

Example:

```python
from fraud_detection_platform.config.settings import load_settings
```

becomes:

```python
from fraud_detection_platform.config.settings import load_settings
```

Also update test imports.

## 4. Update `pyproject.toml`

Update the project metadata.

Example:

```toml
[project]
name = "fraud-detection-platform"
version = "0.1.0"
description = "A production-style real-time fraud detection machine learning platform."
```

Keep the Python version and tool configuration unless the target project requires a change.

## 5. Update Configuration

Update `configs/base.yaml`.

Example:

```yaml
app:
  name: "fraud-detection-platform"
  version: "0.1.0"
```

Environment-specific files such as `development.yaml` and `production.yaml` can usually keep the same structure.

## 6. Update `.env.example`

Update project-specific environment variable values.

Example:

```dotenv
APP_NAME=fraud-detection-platform
MLFLOW_EXPERIMENT_NAME=fraud-detection-platform
```

Do not add real secrets to `.env.example`.

## 7. Update Docker Image Name

When building the Docker image, use the target project name.

Example:

```bash
docker build -t fraud-detection-platform .
docker run --rm fraud-detection-platform
```

## 8. Update README

Update the README title, project goals, target use case, architecture notes, and usage instructions.

The README should describe the specific project, not the generic template.

## 9. Update Tests

Update tests to import the renamed package.

Example:

```python
from fraud_detection_platform import __version__
```

Run the test suite after renaming:

```bash
make quality
```

## 10. Reinitialize Git If Needed

If the copied template should become a new standalone repository, remove the existing Git history and initialize a new repository.

```bash
rm -rf .git
git init
git branch -M main
```

Then create the first commit for the new project:

```bash
git add .
git commit -m "chore: initialize project from ML platform template"
```

## Recommended Naming Map

| Project | Repository Name | Python Package |
|---|---|---|
| Real-Time Fraud Detection Platform | `fraud-detection-platform` | `fraud_detection_platform` |
| Credit Risk Decisioning Platform | `credit-risk-platform` | `credit_risk_platform` |
| Patient Readmission Prediction | `patient-readmission` | `patient_readmission` |
| Clinical NLP Intelligence System | `clinical-nlp` | `clinical_nlp` |
| Customer Churn Intelligence | `customer-churn` | `customer_churn` |
| AI Support Ticket Triage and RAG Assistant | `support-rag` | `support_rag` |

## Principle

A reusable template should provide structure without forcing every project to keep the template identity.

Each copied project should look and behave like an independent production-grade repository.
