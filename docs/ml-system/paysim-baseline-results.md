# PaySim Baseline Model Results

## 1. Purpose

This document records the first baseline model results after running the fraud detection platform on the PaySim dataset.

The goal of this baseline is not to produce the final model. The goal is to establish a first realistic benchmark using a large fraud dataset and understand how the current platform behaves beyond the small synthetic sample data.

This report captures:

```text
dataset size
fraud rate
training and test split
classification metrics
confusion matrix
business interpretation
current limitations
recommended next improvements
```

---

## 2. Dataset

The model was trained on the transformed PaySim dataset.

The raw PaySim data was first converted into the platform's internal transaction schema using:

```bash
python -m fraud_detection_platform.cli.prepare_paysim_data \
  --input-path data/external/PS_20174392719_1491204439457_log.csv \
  --output-path data/raw/paysim_transactions.csv
```

The transformed platform schema contains:

```text
transaction_id
customer_id
transaction_amount
transaction_time
merchant_category
payment_channel
is_fraud
```

The current PaySim adapter maps the external PaySim dataset into the platform schema so the existing training and inference pipelines can run without dataset-specific changes.

---

## 3. Training Command

The baseline model was trained using:

```bash
python -m fraud_detection_platform.cli.train \
  --data-path data/raw/paysim_transactions.csv \
  --model-output-path models/paysim_baseline_fraud_model.joblib
```

The trained model artifact was saved locally to:

```text
models/paysim_baseline_fraud_model.joblib
```

This model artifact is generated locally and should not be committed to Git.

---

## 4. Batch Inference Command

Batch inference was run using:

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/paysim_transactions.csv \
  --model-path models/paysim_baseline_fraud_model.joblib \
  --output-path data/processed/paysim_fraud_predictions.csv
```

The prediction output was saved locally to:

```text
data/processed/paysim_fraud_predictions.csv
```

This generated prediction file should not be committed to Git.

---

## 5. Train/Test Split

The training pipeline produced the following split:

```text
Train rows: 4,771,965
Test rows: 1,590,655
Total rows used: 6,362,620
```

The current training pipeline uses a random train/test split with stratification.

A time-based split should be added later because fraud detection is a time-sensitive problem. In production, models are usually trained on earlier transactions and evaluated on later transactions.

---

## 6. Fraud Rate in the Test Set

The test-set confusion matrix shows:

```text
True negatives: 898,230
False positives: 690,372
False negatives: 0
True positives: 2,053
```

Total fraud cases in the test set:

```text
true positives + false negatives = 2,053 + 0 = 2,053
```

Total test rows:

```text
1,590,655
```

Approximate fraud rate:

```text
2,053 / 1,590,655 ≈ 0.00129
```

So the test-set fraud rate is approximately:

```text
0.129%
```

This means there is roughly:

```text
1 fraud transaction per 775 transactions
```

This confirms that the dataset is highly imbalanced.

---

## 7. Baseline Metrics

The baseline model produced the following metrics:

```text
Precision: 0.0030
Recall: 1.0000
F1: 0.0059
ROC-AUC: 0.7154
PR-AUC: 0.0024
True negatives: 898,230
False positives: 690,372
False negatives: 0
True positives: 2,053
```

---

## 8. Confusion Matrix Interpretation

The confusion matrix can be interpreted as:

```text
True negatives:
    898,230 legitimate transactions correctly classified as non-fraud.

False positives:
    690,372 legitimate transactions incorrectly flagged as fraud.

False negatives:
    0 fraudulent transactions missed by the model.

True positives:
    2,053 fraudulent transactions correctly flagged as fraud.
```

The model caught all fraud cases in the test set:

```text
Recall = 1.0000
False negatives = 0
```

However, the model also flagged a very large number of legitimate transactions:

```text
False positives = 690,372
```

This explains the very low precision:

```text
Precision = 0.0030
```

In plain language:

```text
The model is extremely aggressive.
It catches all fraud cases, but it creates too many false alarms.
```

---

## 9. Business Interpretation

The current baseline model should not be used as an automatic blocking model.

If used directly for blocking, it would incorrectly block many legitimate customers.

The model may be more suitable as an early screening system if suspicious transactions are routed to manual review rather than automatically blocked.

This result highlights why the platform separates:

```text
fraud_score
fraud_prediction
recommended_action
```

The model provides a score and prediction, but the risk decision policy determines the operational action.

For example:

```text
Low score       → approve
Medium score    → manual_review
High score      → block
```

This separation is important because fraud teams can tune business thresholds without retraining the model.

---

## 10. Why Accuracy Is Not Enough

Fraud detection is a highly imbalanced classification problem.

Because the fraud rate is very low, a model can achieve high accuracy by predicting nearly everything as non-fraud.

For this reason, the platform focuses on fraud-relevant metrics such as:

```text
precision
recall
F1
ROC-AUC
PR-AUC
confusion matrix
false positives
false negatives
```

For this baseline, recall is excellent, but precision is poor.

That means the model is good at catching fraud but poor at avoiding false alarms.

---

## 11. Current Model Limitations

The current baseline has several limitations.

### 11.1 Limited Feature Set

The current PaySim adapter maps PaySim into the platform's basic transaction schema.

Current platform features include:

```text
customer_id
transaction_amount
transaction_hour
transaction_day_of_week
transaction_amount_log
merchant_category
payment_channel
```

However, PaySim contains additional financial behavior fields that are not yet used:

```text
oldbalanceOrg
newbalanceOrig
oldbalanceDest
newbalanceDest
```

These fields may contain important fraud signals.

---

### 11.2 Loss of PaySim-Specific Financial Information

The current adapter keeps the platform schema simple, but it discards balance movement information.

This means the model cannot yet learn patterns such as:

```text
large transfer drains origin account
destination balance changes unexpectedly
transaction amount is close to available balance
balance values do not reconcile with transaction amount
```

These may be important fraud indicators.

---

### 11.3 Random Split Instead of Time-Based Split

The current pipeline uses a random train/test split.

For fraud detection, a time-based split is usually more realistic because production models are trained on historical transactions and evaluated on future transactions.

A future version should support:

```text
train on earlier transaction_time values
test on later transaction_time values
```

---

### 11.4 Threshold Not Tuned

The current fraud prediction threshold is:

```text
0.5
```

This threshold may be too aggressive or poorly calibrated for the PaySim dataset.

Future work should evaluate multiple thresholds and compare:

```text
precision
recall
false positives
false negatives
manual review volume
block volume
```

---

### 11.5 Baseline Model Only

The current model is a Random Forest baseline.

It is useful as a starting point, but future experiments should compare:

```text
logistic regression
random forest with tuned parameters
gradient boosting
class imbalance strategies
threshold tuning
cost-sensitive learning
```

---

## 12. Recommended Next Improvements

The next improvement should be PaySim-aware feature engineering.

Recommended new features:

```text
origin_balance_delta
destination_balance_delta
amount_to_origin_balance_ratio
amount_to_destination_balance_ratio
is_transfer
is_cash_out
is_payment
is_debit
is_cash_in
```

Possible definitions:

```text
origin_balance_delta = oldbalanceOrg - newbalanceOrig

destination_balance_delta = newbalanceDest - oldbalanceDest

amount_to_origin_balance_ratio = amount / oldbalanceOrg

amount_to_destination_balance_ratio = amount / oldbalanceDest
```

These features may help the model distinguish normal transactions from suspicious balance behavior.

---

## 13. Recommended Experiment Plan

The next experiment should compare two versions:

```text
Baseline 1:
    current platform schema features

Baseline 2:
    PaySim-aware financial behavior features
```

Comparison metrics:

```text
precision
recall
F1
ROC-AUC
PR-AUC
false positives
false negatives
recommended_action distribution
```

The key question should be:

```text
Can additional PaySim financial features reduce false positives while maintaining strong recall?
```

---

## 14. Portfolio Interpretation

This result is useful even though the baseline metrics are not ideal.

A strong portfolio project should not hide weak baseline results. It should explain them and improve them.

This baseline demonstrates:

```text
large dataset ingestion
schema normalization
model training at scale
model persistence
batch inference
fraud-focused evaluation
class imbalance awareness
business interpretation of metrics
```

The next stage will demonstrate iterative model improvement.

---

## 15. Summary

The first PaySim baseline proves that the platform can run on a large fraud dataset.

Key findings:

```text
The pipeline successfully trained on 4.7M+ rows.
The pipeline evaluated on 1.5M+ rows.
The model caught all fraud cases in the test set.
The model generated too many false positives.
Precision is very low.
Recall is very high.
PR-AUC is low.
More feature engineering and threshold tuning are needed.
```

The baseline is not the final model. It is the first benchmark for improving the fraud detection platform.
