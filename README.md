# Fraud Detection Platform

A production-style machine learning platform for detecting potentially fraudulent financial transactions.

This project is designed to demonstrate more than model training. It shows how a fraud detection system can be structured as a modular ML product with data validation, feature engineering, training, evaluation, model persistence, batch inference, business decision policy, automated tests, and command-line workflows.

---

## Overview

Fraud detection is not only a classification problem. In a real business setting, the system must help teams decide what action to take on a transaction.

This platform separates three important concepts:

```text
fraud_score
    The model's probability-like estimate of fraud risk.

fraud_prediction
    The binary model output after applying a classification threshold.

recommended_action
    The business-facing decision produced by the risk policy.
```

Example:

```text
fraud_score = 0.87
fraud_prediction = 1
recommended_action = block
```

This separation makes the system more production-oriented because the model and business rules can evolve independently.

---

## Why This Project Matters

Many machine learning projects stop at notebooks and metrics. This project focuses on the engineering structure around the model.

The goal is to build the foundation for a fraud detection platform that can eventually support:

```text
batch scoring
real-time API scoring
model tracking
model monitoring
cloud deployment
business decision policies
data drift detection
```

The current version runs locally, but it is structured with production-readiness in mind.

---

## Current Capabilities

The platform currently supports:

- Synthetic transaction data generation.
- Transaction data validation.
- Feature engineering.
- Baseline fraud model training.
- Fraud-focused classification metrics.
- Model artifact saving and loading.
- Batch inference using a saved model.
- Labeled and unlabeled inference data.
- Risk decision policy for business actions.
- Configurable review and block thresholds.
- Command-line workflows.
- Automated tests with Pytest.
- Static type checking with MyPy.
- Linting and formatting with Ruff.
- Pre-commit quality checks.

---

## Current End-to-End Workflow

```text
generate sample transaction data
        ↓
train baseline fraud model
        ↓
evaluate model performance
        ↓
save trained model artifact
        ↓
load model for batch inference
        ↓
score transactions
        ↓
apply risk decision policy
        ↓
write fraud predictions to CSV
```

---

## Architecture

The project uses a modular `src/` layout.

```text
src/fraud_detection_platform/
├── api/
├── cli/
├── config/
├── data/
├── evaluation/
├── features/
├── logging/
├── models/
├── monitoring/
├── pipelines/
├── risk/
└── utils/
```

### Data Layer

Location:

```text
src/fraud_detection_platform/data/
```

Responsibilities:

- Define transaction schemas.
- Load transaction data.
- Validate required columns.
- Support training and inference data contracts.
- Generate synthetic sample data.

Important files:

```text
schema.py
loader.py
sample_generator.py
```

The platform separates training and inference schemas:

```text
Training data:
    requires is_fraud

Inference data:
    does not require is_fraud
```

This matters because production scoring data usually does not have the true fraud label yet.

---

### Feature Engineering Layer

Location:

```text
src/fraud_detection_platform/features/
```

Responsibilities:

- Convert raw transaction data into model-ready features.
- Extract time-based features.
- Create amount-based features.

Current engineered features include:

```text
transaction_hour
transaction_day_of_week
transaction_amount_log
```

The same feature logic is used during training and inference to prevent training-serving skew.

---

### Model Layer

Location:

```text
src/fraud_detection_platform/models/
```

Responsibilities:

- Build the baseline model.
- Train the model.
- Save trained model artifacts.
- Load saved model artifacts.

The current baseline model is a scikit-learn pipeline using:

```text
ColumnTransformer
OneHotEncoder
RandomForestClassifier
```

The model handles both categorical and numeric transaction features.

---

### Evaluation Layer

Location:

```text
src/fraud_detection_platform/evaluation/
```

Responsibilities:

- Calculate fraud-focused classification metrics.
- Return structured metric results.

Current metrics include:

```text
precision
recall
f1
roc_auc
pr_auc
true_negatives
false_positives
false_negatives
true_positives
```

Accuracy is not the main metric because fraud detection is usually highly imbalanced.

---

### Training Pipeline

Location:

```text
src/fraud_detection_platform/pipelines/training.py
```

Responsibilities:

- Load labeled transaction data.
- Build the feature table.
- Split data into training and test sets.
- Train the baseline fraud model.
- Generate fraud scores.
- Convert scores into binary predictions.
- Calculate evaluation metrics.
- Optionally save the trained model artifact.

---

### Batch Inference Pipeline

Location:

```text
src/fraud_detection_platform/pipelines/batch_inference.py
```

Responsibilities:

- Load transaction data for inference.
- Support unlabeled production-style input data.
- Apply feature engineering.
- Load a saved model artifact.
- Generate fraud scores.
- Convert scores into predictions.
- Apply business decision policy.
- Write prediction results to CSV.

For labeled input data, the prediction output contains:

```text
transaction_id
fraud_score
fraud_prediction
recommended_action
is_fraud
```

For unlabeled input data, the prediction output contains:

```text
transaction_id
fraud_score
fraud_prediction
recommended_action
```

---

### Risk Decision Policy Layer

Location:

```text
src/fraud_detection_platform/risk/decision_policy.py
```

Responsibilities:

- Convert fraud scores into business-facing actions.
- Keep business rules separate from model logic.

Current default policy:

```text
fraud_score < 0.50        → approve
fraud_score >= 0.50       → manual_review
fraud_score >= 0.80       → block
```

Supported actions:

```text
approve
manual_review
block
```

This makes the platform more realistic because fraud teams often tune business thresholds without retraining the model.

---

## Project Structure

```text
fraud-detection-platform/
├── configs/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── architecture/
│   ├── engineering-journal/
│   └── ml-system/
├── models/
├── src/
│   └── fraud_detection_platform/
│       ├── api/
│       ├── cli/
│       ├── config/
│       ├── data/
│       ├── evaluation/
│       ├── features/
│       ├── logging/
│       ├── models/
│       ├── monitoring/
│       ├── pipelines/
│       ├── risk/
│       └── utils/
├── tests/
├── Makefile
├── pyproject.toml
└── README.md
```

Generated files under `data/`, `models/`, `build/`, and local environment folders are not intended to be committed.

---

## Setup

Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install ".[dev,config,ml,api,monitoring]"
```

Install pre-commit hooks:

```bash
pre-commit install
```

---

## Quickstart

### 1. Generate Sample Transaction Data

```bash
python -m fraud_detection_platform.cli.generate_sample_data \
  --output-path data/raw/sample_transactions.csv \
  --row-count 100
```

This creates a local synthetic dataset for development and testing.

---

### 2. Train and Save the Model

```bash
python -m fraud_detection_platform.cli.train \
  --data-path data/raw/sample_transactions.csv \
  --model-output-path models/baseline_fraud_model.joblib
```

Example output:

```text
Fraud detection training completed
Train rows: 75
Test rows: 25
Precision: 1.0000
Recall: 1.0000
F1: 1.0000
ROC-AUC: 1.0000
PR-AUC: 1.0000
True negatives: 20
False positives: 0
False negatives: 0
True positives: 5
```

The perfect metrics are expected for the current toy synthetic data because the fraud patterns are intentionally simple.

---

### 3. Run Batch Inference

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/sample_transactions.csv \
  --model-path models/baseline_fraud_model.joblib \
  --output-path data/processed/fraud_predictions.csv
```

Example output:

```text
Fraud batch inference completed
Scored rows: 100
Predictions written to: data/processed/fraud_predictions.csv
```

---

### 4. Run Batch Inference with Custom Risk Thresholds

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/sample_transactions.csv \
  --model-path models/baseline_fraud_model.joblib \
  --output-path data/processed/fraud_predictions.csv \
  --threshold 0.5 \
  --review-threshold 0.4 \
  --block-threshold 0.85
```

Threshold meanings:

```text
--threshold
    Controls the binary fraud_prediction.

--review-threshold
    Controls when a transaction should be sent to manual review.

--block-threshold
    Controls when a transaction should be blocked.
```

---

## Quality Checks

Run all quality checks:

```bash
make quality
```

This runs:

```text
ruff check .
pytest
mypy src tests
```

Run pre-commit checks:

```bash
pre-commit run --all-files
```

---

## Testing

Run the test suite:

```bash
pytest
```

The tests cover:

- Package import validation.
- Settings loading.
- Logging utilities.
- Data loading and validation.
- Feature engineering.
- Classification metrics.
- Baseline model training.
- Model persistence.
- Training pipeline.
- Batch inference pipeline.
- CLI argument parsing.
- Risk decision policy.
- Labeled and unlabeled inference data.

---

## Data Strategy

The project currently uses synthetic data for local engineering development.

This synthetic data is useful for:

```text
unit tests
pipeline validation
CLI testing
local smoke tests
```

However, it is intentionally simple and should not be treated as realistic fraud data.

Planned data improvements:

1. Keep the current synthetic data generator for fast tests.
2. Add support for a more realistic public fraud dataset.
3. Add dataset-specific ingestion and preprocessing.
4. Evaluate the model on more realistic class imbalance.
5. Improve the model and metrics using realistic fraud patterns.

The next planned dataset direction is PaySim or another public fraud dataset with more realistic transaction behavior.

---

## Using PaySim Data

The project currently includes a small synthetic data generator for fast local testing and CI validation. For more realistic fraud modeling, the next supported dataset is PaySim.

PaySim is a public fraud detection dataset available on Kaggle as:

```text
Synthetic Financial Datasets For Fraud Detection
Kaggle dataset: ealaxi/paysim1
```

The raw PaySim dataset should not be committed to this repository. Download it manually from Kaggle and place it locally under:

```text
data/external/
```

Example expected raw file path:

```text
data/external/PS_20174392719_1491204439457_log.csv
```

The project provides a CLI command to transform raw PaySim data into the platform's internal transaction schema.

```bash
python -m fraud_detection_platform.cli.prepare_paysim_data \
  --input-path data/external/PS_20174392719_1491204439457_log.csv \
  --output-path data/raw/paysim_transactions.csv
```

This converts PaySim columns into the platform schema:

```text
PaySim column              Platform column
-----------------------------------------------------
generated row id           transaction_id
nameOrig                   customer_id
amount                     transaction_amount
step                       transaction_time
type                       merchant_category
type                       payment_channel
isFraud                    is_fraud
```

After conversion, train the baseline model on the PaySim-transformed data:

```bash
python -m fraud_detection_platform.cli.train \
  --data-path data/raw/paysim_transactions.csv \
  --model-output-path models/paysim_baseline_fraud_model.joblib
```

Then run batch inference:

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/paysim_transactions.csv \
  --model-path models/paysim_baseline_fraud_model.joblib \
  --output-path data/processed/paysim_fraud_predictions.csv
```

Generated data files and model artifacts should remain local and should not be committed:

```text
data/external/
data/raw/
data/processed/
models/
```

This keeps the GitHub repository lightweight while still allowing the full data preparation, training, and inference workflow to be reproduced locally.


## Current Limitations

The current platform is an early production-style skeleton. Known limitations include:

1. The current sample data is synthetic and simple.
2. The model performs perfectly on sample data because the fraud patterns are obvious.
3. The training split is random rather than time-based.
4. There is no real-time API endpoint yet.
5. There is no model registry yet.
6. There is no MLflow experiment tracking yet.
7. There is no model explainability layer yet.
8. There is no monitoring or drift detection yet.
9. There is no cloud deployment yet.
10. The baseline model has not yet been trained on realistic public fraud data.

---

## Roadmap

Planned improvements:

```text
1. Push the project to GitHub.
2. Improve README and documentation.
3. Add PaySim data ingestion and preparation workflow.
4. Add dataset ingestion and preprocessing.
5. Improve model evaluation on imbalanced data.
6. Add MLflow experiment tracking.
7. Add FastAPI real-time prediction service.
8. Add request and response schemas.
9. Add model metadata and versioning.
10. Add explainability using feature importance or SHAP.
11. Add monitoring and drift detection.
12. Containerize the API and batch workflows.
13. Prepare AWS and Databricks deployment.
```

---

## Portfolio Talking Points

This project demonstrates:

- Production-style Python project structure.
- Modular ML system design.
- Data validation.
- Training and inference schema separation.
- Feature engineering reuse.
- Model training and evaluation.
- Fraud-focused metrics.
- Model persistence.
- Batch scoring.
- Business decision policy.
- CLI workflow design.
- Automated testing.
- Type checking.
- Linting and formatting.
- Pre-commit quality gates.
- Architecture documentation.

The strongest architectural decision so far is the separation between:

```text
model score
model prediction
business action
```

This separation makes the platform easier to explain, test, tune, and extend.

---

## Engineering Philosophy

This project is intentionally being built as an ML platform, not just a model.

A notebook can show experimentation.

A platform shows engineering maturity.

The goal is to demonstrate the ability to design, test, document, and evolve a machine learning system in a way that is understandable to both technical and business stakeholders.
