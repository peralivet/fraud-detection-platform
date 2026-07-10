# Fraud Detection Platform

A production-oriented fraud detection ML platform that turns transaction data into calibrated fraud scores, cost-aware thresholds, operational risk actions, and analyst-ready scoring outputs.

An end-to-end machine learning engineering project for fraud detection.

## Project Highlights

```text
Built an end-to-end fraud detection ML platform using a modular Python package structure.
Ingested and transformed 6.36M+ PaySim transactions.
Engineered PaySim-specific balance movement features for fraud detection.
Reduced false positives by about 75% compared with the generic baseline.
Trained a calibrated fraud model with ROC-AUC of 0.9642 and PR-AUC of 0.2093.
Evaluated thresholds using precision, recall, F1, ROC-AUC, PR-AUC, and confusion matrix metrics.
Added cost-sensitive threshold analysis using configurable false positive, false negative, and review costs.
Compared optimal thresholds across multiple business cost scenarios.
Created risk-band decisioning: approve, manual review, high-risk review, and priority investigation.
Built production-style batch scoring that omits ground-truth labels from scored outputs.
Generated analyst-facing scored transaction CSVs and management-level action summaries.
Created a priority investigation queue representing only 0.027% of transactions with a 75.44% fraud rate.
Added CI quality checks with pytest, ruff, mypy, and pre-commit.
Documented the system architecture, experiments, calibration, cost analysis, and scoring workflow.
```

## How to Review This Project

If you are reviewing this project quickly, start with these files:

```text
README.md
docs/ml-system/architecture-overview.md
docs/ml-system/paysim-calibrated-batch-inference-results.md
docs/ml-system/paysim-cost-scenario-comparison.md
```

Recommended review path:

```text
1. Read the Project Highlights section in README.md.
2. Review the architecture overview to understand the system design.
3. Review the calibrated batch inference results to see the production-style scoring workflow.
4. Review the cost scenario comparison to understand how business assumptions affect threshold selection.
5. Browse the src/fraud_detection_platform package to inspect the tested implementation.
6. Check the tests/ directory to see coverage across data, features, models, evaluation, risk policies, and pipelines.
```

The most important takeaway is that this project is not just a fraud classification model. It is a production-oriented ML decisioning workflow that connects model scores to risk actions, cost trade-offs, analyst outputs, and management summaries.

This project demonstrates how to move beyond a notebook model into a production-style fraud detection workflow with:

```text
data ingestion
feature engineering
model training
model evaluation
probability calibration
threshold tuning
cost-sensitive evaluation
cost scenario comparison
risk-band decisioning
batch scoring
production-style analyst output
management summary reporting
```

The goal is not only to predict fraud, but to show how fraud scores can support real operational decisions.

---

## Project Overview

Fraud detection is a rare-event classification problem. Fraud cases are usually a tiny percentage of all transactions, which makes ordinary accuracy misleading.

This project focuses on practical fraud modeling questions such as:

```text
How do we reduce false positives?
How do we avoid missing too much fraud?
How should thresholds be selected?
How do business costs affect threshold choice?
How do we turn model scores into risk actions?
How do we produce outputs useful to fraud analysts and risk managers?
```

The project uses a modular Python package structure and includes tested components for data preparation, modeling, evaluation, thresholding, calibration, and batch scoring.

---

## Current Capabilities

The platform currently supports:

```text
Synthetic transaction data generation
Generic fraud model training
PaySim dataset ingestion
PaySim-enriched feature engineering
Random Forest baseline modeling
Calibrated fraud modeling
Classification metric evaluation
Threshold tuning
Score distribution analysis
Cost-sensitive threshold evaluation
Cost scenario comparison
Risk-band decision policy
Batch inference
Production-style scoring output
Risk action summary reporting
CI quality checks
Unit tests
```

---

## Dataset Strategy

The project supports two data paths.

### 1. Synthetic Sample Data

Synthetic data is used for fast local development and tests.

This keeps the test suite lightweight and reproducible.

### 2. PaySim Dataset

The main realistic dataset workflow uses the PaySim mobile money simulation dataset.

Raw PaySim data is stored locally and is not committed to Git.

Expected local path:

```text
data/external/PS_20174392719_1491204439457_log.csv
```

Generated data, reports, and model artifacts are intentionally ignored by Git.

---

## Architecture

```text
fraud-detection-platform/
├── src/
│   └── fraud_detection_platform/
│       ├── cli/
│       ├── data/
│       ├── evaluation/
│       ├── features/
│       ├── models/
│       ├── pipelines/
│       └── risk/
├── tests/
├── docs/
│   └── ml-system/
├── .github/
│   └── workflows/
├── Makefile
├── pyproject.toml
└── README.md
```

### Main Package Areas

```text
data:
    Dataset loading, validation, schema management, and PaySim adaptation.

features:
    Generic transaction features and PaySim-specific financial behavior features.

models:
    Baseline Random Forest model, PaySim-enriched model, and calibrated model.

evaluation:
    Classification metrics, threshold analysis, score distribution, cost evaluation,
    cost scenario comparison, and action summaries.

risk:
    Business decision policies that convert fraud scores into recommended actions.

pipelines:
    Training and batch inference workflows.

cli:
    Command-line entry points for running data preparation, training, evaluation,
    scoring, and reporting workflows.
```

---

## Key ML Experiments

### 1. Generic PaySim Baseline

The first PaySim baseline used generic platform features only.

Result:

```text
Precision: 0.0030
Recall: 1.0000
F1: 0.0059
ROC-AUC: 0.7154
PR-AUC: 0.0024
False positives: 690,372
False negatives: 0
True positives: 2,053
```

Interpretation:

```text
The model caught all fraud cases but produced too many false positives.
```

---

### 2. PaySim-Enriched Model

The enriched model added PaySim balance movement features:

```text
origin_balance_delta
destination_balance_delta
amount_to_origin_balance_ratio
amount_to_destination_balance_ratio
```

Result:

```text
Precision: 0.0109
Recall: 0.9157
F1: 0.0216
ROC-AUC: 0.9473
PR-AUC: 0.1955
False positives: 169,967
False negatives: 173
True positives: 1,880
```

Interpretation:

```text
Feature engineering reduced false positives by about 75% while keeping strong fraud recall.
```

---

### 3. Threshold Tuning

Threshold tuning showed that the uncalibrated model scores were compressed around `0.50`.

Useful thresholds were concentrated around:

```text
0.50 to 0.51
```

This revealed that the model ranked fraud risk well, but its probability scores were poorly calibrated.

---

### 4. Probability Calibration

A calibrated PaySim-enriched model was trained using sigmoid calibration.

Comparison:

| Metric | Uncalibrated Enriched Model | Calibrated Enriched Model |
|---|---:|---:|
| ROC-AUC | 0.9473 | 0.9642 |
| PR-AUC | 0.1955 | 0.2093 |

Calibration changed score behavior from compressed around `0.50` to a more realistic rare-event probability range.

Calibrated score distribution:

```text
Non-fraud mean score: 0.001240
Fraud mean score:     0.038846
```

Interpretation:

```text
The calibrated model produced more useful scores for thresholding and risk decisioning.
```

---

### 5. Cost-Sensitive Threshold Evaluation

Using cost assumptions:

```text
False positive cost: $5
False negative cost: $500
Manual review cost: $2
```

The cost-optimal threshold was:

```text
0.010
```

At threshold `0.010`:

```text
False positives: 27,273
False negatives: 932
Review volume: 28,394
Total estimated cost: $659,153
```

Interpretation:

```text
Threshold 0.010 produced the best estimated cost trade-off under the stated assumptions.
```

---

### 6. Cost Scenario Comparison

The project also compares optimal thresholds under different business cost assumptions.

| Scenario | Best Threshold |
|---|---:|
| balanced_operations | 0.010 |
| high_fraud_loss | 0.010 |
| high_customer_friction | 0.075 |
| high_review_cost | 0.075 |

Interpretation:

```text
There is no universal best threshold. The best threshold depends on business priorities.
```

---

## Risk-Band Decision Policy

The calibrated model supports operational risk bands:

```text
fraud_score < 0.010:
    approve

0.010 ≤ fraud_score < 0.075:
    manual_review

0.075 ≤ fraud_score < 0.100:
    high_risk_review

fraud_score ≥ 0.100:
    priority_investigation
```

This converts model scores into business-ready recommended actions.

---

## Batch Scoring Output

The calibrated batch inference pipeline produces an analyst-facing scored transaction file.

Example output columns:

```text
transaction_id
customer_id
transaction_time
transaction_amount
merchant_category
payment_channel
fraud_score
fraud_prediction
recommended_action
```

In evaluation mode, the output can also include:

```text
is_fraud
```

In production mode, labels are omitted because true fraud outcomes are not known at scoring time.

---

## Production Scoring Mode

Production-style scoring can be run with:

```bash
python -m fraud_detection_platform.cli.paysim_batch_inference \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-path models/paysim_calibrated_fraud_model.joblib \
  --output-path reports/paysim_calibrated_scored_transactions_production.csv \
  --threshold 0.010 \
  --review-threshold 0.010 \
  --high-risk-threshold 0.075 \
  --priority-threshold 0.100 \
  --production-mode
```

Production output intentionally excludes `is_fraud`.

This makes the file realistic for fraud analysts or risk managers.

---

## Risk Action Summary

The action summary report aggregates scored transactions by recommended action.

Observed action distribution:

| Recommended Action | Transaction Count | Percentage of Total | Fraud Rate |
|---|---:|---:|---:|
| approve | 6,248,594 | 98.21% | 0.0545% |
| manual_review | 110,088 | 1.73% | 2.77% |
| high_risk_review | 2,252 | 0.035% | 21.71% |
| priority_investigation | 1,686 | 0.027% | 75.44% |

Interpretation:

```text
Fraud concentration increases sharply as action severity increases.
The priority investigation queue contains only 0.027% of transactions but has a 75.44% fraud rate.
```

This is a strong operational result.

---

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project with all development and ML dependencies:

```bash
python -m pip install ".[dev,config,ml,api,monitoring]"
```

---

## Quality Checks

Run all quality checks:

```bash
make quality
```

This runs:

```text
ruff linting
ruff formatting check
pytest
mypy
```

Run pre-commit hooks:

```bash
pre-commit run --all-files
```

---

## Example Workflows

### Generate Synthetic Sample Data

```bash
python -m fraud_detection_platform.cli.generate_sample_data \
  --output-path data/raw/sample_transactions.csv \
  --row-count 100
```

---

### Prepare PaySim Data

```bash
python -m fraud_detection_platform.cli.prepare_paysim_data \
  --input-path data/external/PS_20174392719_1491204439457_log.csv \
  --output-path data/raw/paysim_transactions.csv
```

---

### Train Generic Baseline

```bash
python -m fraud_detection_platform.cli.train \
  --data-path data/raw/paysim_transactions.csv \
  --model-output-path models/paysim_baseline_fraud_model.joblib
```

---

### Train PaySim-Enriched Model

```bash
python -m fraud_detection_platform.cli.train_paysim_enriched \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-output-path models/paysim_enriched_fraud_model.joblib \
  --scores-output-path reports/paysim_enriched_test_scores.csv
```

---

### Train Calibrated PaySim Model

```bash
python -m fraud_detection_platform.cli.train_paysim_enriched \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-type calibrated \
  --model-output-path models/paysim_calibrated_fraud_model.joblib \
  --scores-output-path reports/paysim_calibrated_test_scores.csv
```

---

### Evaluate Thresholds

```bash
python -m fraud_detection_platform.cli.evaluate_thresholds \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_calibrated_threshold_report.csv \
  --thresholds 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.075 0.10 0.15 0.20
```

---

### Analyze Score Distribution

```bash
python -m fraud_detection_platform.cli.analyze_score_distribution \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_calibrated_score_distribution_report.csv
```

---

### Evaluate Threshold Costs

```bash
python -m fraud_detection_platform.cli.evaluate_threshold_costs \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_calibrated_cost_report.csv \
  --thresholds 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.075 0.10 0.15 0.20 \
  --false-positive-cost 5 \
  --false-negative-cost 500 \
  --manual-review-cost 2
```

---

### Compare Cost Scenarios

```bash
python -m fraud_detection_platform.cli.evaluate_cost_scenarios \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_cost_scenario_report.csv \
  --best-output-path reports/paysim_cost_scenario_best_thresholds.csv \
  --thresholds 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.075 0.10 0.15 0.20
```

---

### Run Production-Style Batch Scoring

```bash
python -m fraud_detection_platform.cli.paysim_batch_inference \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-path models/paysim_calibrated_fraud_model.joblib \
  --output-path reports/paysim_calibrated_scored_transactions_production.csv \
  --threshold 0.010 \
  --review-threshold 0.010 \
  --high-risk-threshold 0.075 \
  --priority-threshold 0.100 \
  --production-mode
```

---

### Summarize Risk Actions

```bash
python -m fraud_detection_platform.cli.summarize_actions \
  --scored-path reports/paysim_calibrated_scored_transactions.csv \
  --output-path reports/paysim_action_summary.csv
```

---

## Documentation

Detailed experiment notes are stored in:

```text
docs/ml-system/
```

Important documents include:

```text
architecture-overview.md
data-ingestion-strategy.md
paysim-baseline-results.md
paysim-enriched-results.md
paysim-threshold-tuning-results.md
paysim-score-distribution-analysis.md
paysim-calibration-results.md
paysim-cost-sensitive-threshold-results.md
paysim-cost-scenario-comparison.md
paysim-calibrated-batch-inference-results.md
fraud-platform-case-study.md
```

---

## What This Project Demonstrates

This project demonstrates practical ML engineering skills:

```text
clean Python package design
test-driven development
data validation
feature engineering
model training pipelines
evaluation pipelines
probability calibration
threshold tuning
business-cost evaluation
risk-band policy design
batch inference
production-style scoring output
CI quality checks
documentation
```

It also demonstrates business judgment:

```text
fraud detection is not just about ROC-AUC
thresholds are business decisions
calibration matters for decisioning
false positives and false negatives have different costs
risk managers need actionable outputs, not just model metrics
```

---

## Current Limitations

Current limitations include:

```text
PaySim is simulated data
random train/test split is used
no time-based validation yet
no real-time API endpoint yet
no dashboard yet
no model explainability layer yet
no drift monitoring yet
no analyst feedback loop yet
no deployment infrastructure yet
```

---

## Roadmap

Planned improvements:

```text
Add time-based validation
Add model explainability for high-risk transactions
Add feature importance reporting
Add API endpoint for real-time scoring
Add dashboard for action distribution monitoring
Add drift monitoring for fraud scores and action bands
Add analyst feedback loop
Compare calibrated Random Forest with gradient boosting models
Add transaction-amount-based loss modeling
Add review capacity constraints
```

---

## Portfolio Summary

This project shows an end-to-end fraud detection system that moves from model training to business decisioning.

The strongest project milestones are:

```text
PaySim-enriched features reduced false positives by about 75%.
Calibration improved ROC-AUC to 0.9642 and PR-AUC to 0.2093.
Cost-sensitive evaluation selected threshold 0.010 under balanced assumptions.
Cost scenario comparison showed threshold choice depends on business priorities.
Risk-band scoring created approve, manual review, high-risk review, and priority investigation queues.
The priority investigation queue represented only 0.027% of transactions but had a 75.44% fraud rate.
Production scoring mode generates an analyst-facing CSV without ground-truth labels.
```

This demonstrates a production-oriented fraud ML workflow rather than a simple classification notebook.
