# Fraud Detection Platform: Data Ingestion Strategy

## 1. Purpose

This document explains the data strategy for the fraud detection platform.

The platform currently uses synthetic sample data for local development. That is useful for engineering, but it is not enough to demonstrate realistic fraud modeling.

The next stage is to keep synthetic data for fast testing while adding support for a more realistic public fraud dataset.

The recommended first realistic dataset is **PaySim**, a synthetic mobile money transaction dataset commonly used for fraud detection experimentation. PaySim simulates mobile money transactions, and its Kaggle dataset description notes that each simulation step represents one hour.  [oai_citation:0‡Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1?utm_source=chatgpt.com)

---

## 2. Why Keep Synthetic Data?

The current synthetic data generator should remain in the project.

It is useful for:

```text
unit tests
local smoke tests
CLI validation
pipeline validation
fast development
CI checks
```

Synthetic test data should be:

```text
small
deterministic
fast to generate
easy to understand
safe to commit as code logic, not raw data
```

The current generator gives us exactly that.

However, this data is intentionally simple. Fraud rows have obvious patterns, so the model can achieve perfect scores. That is useful for proving that the system works end to end, but it is not useful for proving realistic modeling performance.

---

## 3. Why Add a Realistic Public Dataset?

A portfolio fraud project needs two separate stories:

```text
Engineering story:
    Can the platform load data, train models, save artifacts, run inference, and pass tests?

Modeling story:
    Can the platform handle realistic fraud patterns, class imbalance, and imperfect metrics?
```

The current synthetic data supports the engineering story.

A public fraud dataset improves the modeling story.

A more realistic dataset will help us demonstrate:

```text
class imbalance
precision-recall trade-offs
false positives
false negatives
threshold tuning
business risk policy
model comparison
feature importance
monitoring readiness
```

---

## 4. Why PaySim First?

PaySim is a good next dataset because its columns are business-readable.

Many fraud datasets, such as the popular credit card fraud dataset, contain anonymized PCA-transformed features. Those are useful for modeling, but they are harder to explain in a portfolio because the feature meanings are hidden.

PaySim has understandable transaction fields such as transaction type, amount, origin customer, destination customer, balance information, and fraud labels. Public examples and dataset summaries commonly show columns such as `type`, `amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, and `isFraud`.  [oai_citation:1‡GitHub](https://github.com/elangovana/PaySim-Synthetic-Dataset-Fraud-Detection/blob/master/PaySim%20Synthetic%20Dataset%20Fraud%20Detection.ipynb?utm_source=chatgpt.com)

This makes PaySim easier to connect to real fraud product thinking.

---

## 5. PaySim to Platform Schema Mapping

The platform has its own internal transaction schema:

```text
transaction_id
customer_id
transaction_amount
transaction_time
merchant_category
payment_channel
is_fraud
```

PaySim does not match this schema exactly, so we need an ingestion layer that transforms PaySim into the platform schema.

Recommended mapping:

```text
PaySim column              Platform column
-----------------------------------------------------
generated row id           transaction_id
nameOrig                   customer_id
amount                     transaction_amount
step                       transaction_time
type                       payment_channel
type                       merchant_category
isFraud                    is_fraud
```

The `step` column in PaySim represents simulation time. Since each step represents an hour, we can convert it into a timestamp relative to a chosen start date.  [oai_citation:2‡Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1?utm_source=chatgpt.com)

Example:

```text
step = 1
start_time = 2026-01-01 00:00:00
transaction_time = 2026-01-01 01:00:00
```

---

## 6. Why Use an Ingestion Layer?

We should not force the rest of the platform to understand every external dataset format.

Instead, external datasets should be transformed into the internal platform schema.

This gives us a clean architecture:

```text
external dataset
        ↓
dataset-specific ingestion layer
        ↓
internal transaction schema
        ↓
existing feature engineering
        ↓
existing training pipeline
        ↓
existing evaluation and inference workflows
```

This means the model pipeline does not need to know whether the data came from:

```text
our synthetic generator
PaySim
a future Kaggle dataset
a future production database
```

It only needs data that matches the platform schema.

---

## 7. Proposed PaySim Module

Recommended file:

```text
src/fraud_detection_platform/data/paysim.py
```

Recommended responsibilities:

```text
load raw PaySim CSV
validate PaySim-specific columns
transform PaySim columns into the platform schema
optionally sample rows for local development
write transformed data to CSV
```

Recommended functions:

```text
validate_paysim_columns()
transform_paysim_to_platform_schema()
load_paysim_dataset()
```

Optional later functions:

```text
sample_paysim_dataset()
write_platform_transactions()
```

---

## 8. Testing Strategy

We should not put the full PaySim dataset into Git.

Instead, tests should use tiny in-memory sample DataFrames that mimic PaySim columns.

Tests should verify:

```text
required PaySim columns are validated
missing PaySim columns raise a clear error
PaySim rows are transformed into platform columns
transaction_id is generated correctly
amount maps to transaction_amount
nameOrig maps to customer_id
isFraud maps to is_fraud
step becomes transaction_time
```

This keeps the test suite fast and CI-friendly.

---

## 9. Modeling Strategy After PaySim Ingestion

Once PaySim ingestion exists, the next modeling steps should be:

```text
1. Download PaySim manually outside Git.
2. Transform PaySim into the platform schema.
3. Train the existing baseline model.
4. Compare metrics against synthetic-data metrics.
5. Analyze class imbalance.
6. Tune thresholds using precision, recall, F1, ROC-AUC, and PR-AUC.
7. Evaluate recommended_action distributions.
8. Add feature importance or explainability.
```

The most important change is that we should no longer expect perfect metrics.

With more realistic fraud data, imperfect results are normal and more credible.

---

## 10. Current Limitations of PaySim

PaySim is useful, but it is not perfect.

Important limitations:

```text
it is synthetic, not true production data
it may not capture all real-world fraud behaviors
it may contain simulator-specific patterns
it does not represent every industry or payment system
historical customer behavior may still need feature engineering
```

So PaySim should be treated as a realistic development dataset, not as proof of production fraud accuracy.

---

## 11. Why This Improves the Portfolio

Adding PaySim support improves the project because it shows:

```text
dataset ingestion design
schema normalization
separation between external data and internal contracts
realistic class imbalance handling
better evaluation discipline
business-aware threshold tuning
```

This is stronger than simply training a model on a downloaded CSV.

The platform will show that external data can be adapted into a clean internal ML system.

---

## 12. Recommended Next Implementation Step

The next implementation step is to create:

```text
src/fraud_detection_platform/data/paysim.py
tests/test_paysim.py
```

The first version should focus only on transformation:

```text
PaySim DataFrame
        ↓
platform transaction DataFrame
```

We should not download or commit the full dataset yet.

After the transformation code is tested, we can add a CLI command for local conversion:

```text
python -m fraud_detection_platform.cli.prepare_paysim_data \
  --input-path data/external/paysim.csv \
  --output-path data/raw/paysim_transactions.csv
```

This keeps the project clean, testable, and portfolio-ready.
