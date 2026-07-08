# Fraud Detection Modeling Strategy

## Overview

This document defines the initial modeling strategy for the fraud detection platform.

The goal is to build fraud models in a way that is measurable, explainable, reproducible, and suitable for future production workflows.

## Prediction Task

The initial machine learning task is binary classification.

For each transaction, the model should predict whether the transaction is likely to be fraudulent.

Target variable:

```text
is_fraud
```

Class labels:

```text
0 = legitimate transaction
1 = fraudulent transaction
```

## Model Output

The model should produce a fraud probability score.

Example:

```text
fraud_probability = 0.82
```

This score can then be mapped to a risk level or business action.

Example:

| Fraud Probability | Risk Level | Example Action |
|---|---|---|
| 0.00 - 0.30 | Low | Allow transaction |
| 0.30 - 0.70 | Medium | Step-up verification or manual review |
| 0.70 - 1.00 | High | Block, hold, or investigate transaction |

The model score should support business decisioning, not replace all policy logic.

## Baseline Modeling Approach

The first modeling version should start simple.

Recommended baseline models:

1. Logistic Regression
2. Random Forest
3. Gradient Boosting model

A simple baseline is important because it gives the project a measurable starting point.

The baseline should answer:

```text
Can we predict fraud better than random guessing or simple rules?
```

## Why Start With Baselines

Baseline models help establish:

- initial model performance
- feature usefulness
- data quality issues
- class imbalance impact
- evaluation workflow
- reproducible training process

Starting with advanced models too early can hide data problems and make debugging harder.

## Fraud-Specific Evaluation Metrics

Accuracy should not be the primary metric because fraud is usually rare.

For example, if only 1% of transactions are fraudulent, a model that predicts every transaction as legitimate can be 99% accurate but useless.

Better metrics include:

- precision
- recall
- F1 score
- PR-AUC
- ROC-AUC
- confusion matrix
- false positive rate
- false negative rate

## Primary Metric

The initial primary metric should be:

```text
PR-AUC
```

PR-AUC is useful for imbalanced classification because it focuses on precision and recall for the positive fraud class.

## Secondary Metrics

Secondary metrics should include:

- recall for fraud cases
- precision for fraud alerts
- F1 score
- ROC-AUC
- false positive rate
- confusion matrix

## Threshold Strategy

The model should output probabilities, but business decisions require thresholds.

A threshold converts a score into a class or action.

Example:

```text
fraud_probability >= 0.70 -> high risk
```

The threshold should not be chosen randomly. It should be tuned based on business priorities.

Examples:

- If fraud losses are very costly, choose a lower threshold to catch more fraud.
- If customer friction is very costly, choose a higher threshold to reduce false positives.
- If manual review capacity is limited, choose a threshold that controls review volume.

## Class Imbalance Strategy

Fraud datasets are usually imbalanced.

Possible techniques include:

- stratified train/test split
- class weights
- oversampling the minority class
- undersampling the majority class
- threshold tuning
- anomaly detection for comparison

The first version should prefer simple, explainable methods such as stratified splitting and class weights.

## Explainability Strategy

Fraud systems often need explanations for operational review and governance.

Initial explainability methods may include:

- feature importance
- coefficients for linear models
- permutation importance
- SHAP values in later versions

The system should be able to explain why a transaction was scored as risky.

## Experiment Tracking

The project should eventually track experiments using MLflow.

Useful tracked artifacts include:

- model parameters
- evaluation metrics
- confusion matrix
- precision-recall curve
- ROC curve
- trained model artifact
- preprocessing configuration
- dataset version or input path

Experiment tracking helps compare models and reproduce results.

## Model Validation Risks

Fraud modeling has several risks.

### Data Leakage

The model must not use fields that are only known after fraud investigation or transaction settlement.

### Overfitting

A model may memorize historical fraud patterns that do not generalize to future fraud behavior.

### Drift

Fraud patterns change over time, so model performance can degrade.

### Bias and Fairness

Fraud models may affect customer access to financial services. Features and policies should be reviewed for unfair or inappropriate impact.

### Operational Latency

Real-time fraud scoring must be fast enough to support transaction decisions.

## Initial Modeling Scope

The first modeling implementation should include:

1. Load prepared transaction data.
2. Validate the target column.
3. Split data into training and test sets.
4. Train a simple baseline model.
5. Evaluate using fraud-appropriate metrics.
6. Save metrics and model artifacts.
7. Document results.

Later versions can add:

- MLflow experiment tracking
- multiple model comparison
- threshold optimization
- explainability reports
- batch scoring
- real-time API scoring
- monitoring and drift detection

## Principle

The goal is not only to train a high-scoring model.

The goal is to create a modeling workflow that is measurable, explainable, reproducible, and ready to evolve into a production fraud detection system.
