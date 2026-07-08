# Fraud Detection Data Strategy

## Overview

This document defines the initial data strategy for the fraud detection platform.

The goal is to describe the expected data, target variable, feature categories, data quality risks, and how the project will prepare data for machine learning workflows.

## Data Objective

The data should support supervised fraud classification.

Each transaction record should contain information that helps estimate whether the transaction is likely to be fraudulent.

The expected prediction target is:

```text
is_fraud
```

where:

```text
0 = legitimate transaction
1 = fraudulent transaction
```

## Expected Dataset Shape

The initial dataset should represent transaction-level records.

Each row should represent one transaction.

Each column should describe transaction attributes, customer behavior, merchant information, device signals, location signals, or historical activity.

Example structure:

```text
transaction_id | customer_id | transaction_amount | merchant_category | transaction_time | device_type | location | is_fraud
```

## Candidate Feature Groups

Useful fraud detection features may include the following groups.

### Transaction Features

Examples:

- transaction amount
- transaction currency
- transaction timestamp
- transaction hour
- day of week
- merchant category
- payment channel
- card-present or card-not-present indicator

### Customer Features

Examples:

- customer account age
- historical transaction count
- average transaction amount
- previous fraud history
- typical transaction locations
- typical merchant categories

### Behavioral Features

Examples:

- transaction velocity
- number of transactions in the last hour
- number of merchants used in the last day
- amount spent in the last day
- deviation from normal customer spending

### Merchant Features

Examples:

- merchant category
- merchant country
- merchant historical fraud rate
- merchant transaction volume

### Device and Location Features

Examples:

- device type
- device fingerprint
- IP country
- billing country
- shipping country
- distance from usual customer location
- mismatch between customer country and transaction country

## Data Quality Risks

Fraud data can have several quality challenges.

### Class Imbalance

Fraud is usually rare compared with legitimate transactions. This means accuracy alone can be misleading.

The project should use fraud-appropriate metrics such as precision, recall, F1 score, PR-AUC, and confusion matrix analysis.

### Delayed Labels

Fraud labels may not be available immediately. A transaction may only be confirmed as fraudulent after a dispute, chargeback, investigation, or customer report.

This creates a gap between prediction time and label availability.

### Label Noise

Some transactions may be incorrectly labeled.

Examples:

- fraudulent transactions not reported
- legitimate transactions incorrectly disputed
- investigation outcomes changed later

### Data Leakage

Features must not include information that would only be known after the transaction decision.

Examples of leakage risks:

- chargeback status
- investigation outcome
- final fraud decision
- post-transaction dispute information

### Missing Values

Some fields may be missing due to system limitations, optional user inputs, device privacy settings, or integration issues.

The project should handle missing values explicitly.

### Drift

Fraud patterns change over time. A model trained on older data may become less effective as attackers adapt.

Monitoring should track feature drift, score drift, and performance drift.

## Initial Data Handling Approach

The first version of the project should:

1. Load transaction data from a local or sample dataset.
2. Validate expected columns.
3. Separate features from the target.
4. Split data into train and test sets.
5. Preserve class distribution during splitting when possible.
6. Apply preprocessing consistently.
7. Train baseline models.
8. Evaluate using fraud-appropriate metrics.

## Data Splitting Strategy

For the initial baseline, the project may use a stratified train/test split to preserve fraud class distribution.

For a more realistic fraud system, a time-based split is preferred because production models predict future transactions using past data.

Recommended progression:

```text
Version 1: stratified train/test split
Version 2: time-based train/test split
Version 3: rolling validation window
```

## Feature Engineering Strategy

Initial feature engineering should focus on simple, explainable features:

- transaction amount transformations
- transaction hour
- day of week
- categorical encoding
- missing value indicators
- simple customer behavior aggregates if available

Advanced versions can add:

- velocity features
- rolling customer aggregates
- merchant-level risk features
- graph-based fraud features
- device and IP risk features
- embedding-based features

## Data Storage Strategy

Initial local development can use:

- CSV files for sample data
- Parquet files for processed data
- local folders excluded from Git

Recommended local folder structure:

```text
data/
├── raw/
├── interim/
├── processed/
└── external/
```

Raw and processed datasets should not be committed to Git.

Future cloud versions can use:

- Amazon S3 for object storage
- Databricks Delta tables for managed analytical datasets
- MLflow artifacts for model outputs
- feature store tables for reusable features

## Security and Privacy Considerations

Fraud detection data can contain sensitive customer and financial information.

The project should avoid committing real customer data.

Production systems should consider:

- encryption at rest
- encryption in transit
- access controls
- audit logs
- tokenization or masking of sensitive fields
- least-privilege access
- secure secret management

## Principle

The data strategy should prevent leakage, preserve reproducibility, support meaningful model evaluation, and prepare the project for future batch, real-time, and cloud workflows.
