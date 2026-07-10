# PaySim Enriched Model Results

## 1. Purpose

This document records the second PaySim modeling experiment for the fraud detection platform.

The first PaySim baseline used only the generic platform transaction features. The second experiment adds PaySim-specific financial behavior features to test whether balance movement information improves fraud detection performance.

The goal of this experiment is to answer:

```text
Can PaySim balance movement features reduce false positives while keeping fraud recall strong?
```

---

## 2. Experiment Summary

Two PaySim experiments are compared:

```text
Baseline 1:
    Generic platform features only

Baseline 2:
    Generic platform features + PaySim balance movement features
```

Baseline 1 proved that the platform could train on the full PaySim dataset, but the model was too aggressive. It caught all fraud cases but generated too many false positives.

Baseline 2 tests whether better feature engineering can improve the fraud/non-fraud separation.

---

## 3. Feature Engineering Hypothesis

The hypothesis for this experiment is:

```text
Fraud behavior in PaySim is better explained when the model can see how transaction amounts relate to account balance movement.
```

The first baseline used features such as:

```text
customer_id
transaction_amount
transaction_hour
transaction_day_of_week
transaction_amount_log
merchant_category
payment_channel
```

However, it discarded PaySim balance fields:

```text
oldbalanceOrg
newbalanceOrig
oldbalanceDest
newbalanceDest
```

These fields may contain important fraud signals.

For example, a transaction that drains the sender's account may be more suspicious than a transaction of the same amount from an account with a much larger balance.

---

## 4. New Features Added

The enriched model added the following PaySim-specific financial behavior features:

```text
origin_balance_delta
destination_balance_delta
amount_to_origin_balance_ratio
amount_to_destination_balance_ratio
```

Feature definitions:

```text
origin_balance_delta = oldbalanceOrg - newbalanceOrig

destination_balance_delta = newbalanceDest - oldbalanceDest

amount_to_origin_balance_ratio = amount / oldbalanceOrg

amount_to_destination_balance_ratio = amount / oldbalanceDest
```

These features help the model understand how money moved between accounts, not just the transaction amount and transaction type.

---

## 5. Training Command

The enriched PaySim model was trained using:

```bash
python -m fraud_detection_platform.cli.train_paysim_enriched \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-output-path models/paysim_enriched_fraud_model.joblib
```

The trained model artifact was saved locally to:

```text
models/paysim_enriched_fraud_model.joblib
```

This file is generated locally and should not be committed to Git.

---

## 6. Train/Test Split

The enriched training pipeline produced the following split:

```text
Train rows: 4,771,965
Test rows: 1,590,655
Total rows used: 6,362,620
```

This matches the first PaySim baseline experiment.

---

## 7. Baseline 1 Results

The first PaySim baseline used generic platform features only.

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

Interpretation:

```text
The model caught all fraud cases, but it flagged too many legitimate transactions.
```

---

## 8. Baseline 2 Results

The enriched PaySim model used generic platform features plus PaySim balance movement features.

```text
Precision: 0.0109
Recall: 0.9157
F1: 0.0216
ROC-AUC: 0.9473
PR-AUC: 0.1955
True negatives: 1,418,635
False positives: 169,967
False negatives: 173
True positives: 1,880
```

Interpretation:

```text
The enriched model is more selective. It catches most fraud cases while greatly reducing false positives.
```

---

## 9. Metrics Comparison

| Metric | Baseline 1: Generic Features | Baseline 2: Enriched Features | Change |
|---|---:|---:|---:|
| Precision | 0.0030 | 0.0109 | Improved |
| Recall | 1.0000 | 0.9157 | Lower |
| F1 | 0.0059 | 0.0216 | Improved |
| ROC-AUC | 0.7154 | 0.9473 | Improved |
| PR-AUC | 0.0024 | 0.1955 | Improved |
| False Positives | 690,372 | 169,967 | Improved |
| False Negatives | 0 | 173 | Lower |
| True Positives | 2,053 | 1,880 | Lower |

---

## 10. False Positive Reduction

The largest operational improvement is the reduction in false positives.

```text
Baseline 1 false positives: 690,372
Baseline 2 false positives: 169,967
```

Difference:

```text
690,372 - 169,967 = 520,405 fewer false positives
```

Approximate reduction:

```text
520,405 / 690,372 ≈ 75%
```

This is significant because false positives create customer friction and manual review workload.

---

## 11. Recall Trade-Off

The enriched model reduced false positives, but recall dropped:

```text
Baseline 1 recall: 1.0000
Baseline 2 recall: 0.9157
```

The enriched model missed:

```text
173 fraud cases
```

This is the trade-off:

```text
Baseline 1:
    catches all fraud
    creates too many false alarms

Baseline 2:
    catches most fraud
    greatly reduces false alarms
```

This is a more realistic fraud modeling trade-off.

---

## 12. Business Interpretation

The enriched model is more practical than the first baseline.

The first baseline would overwhelm fraud operations because it flags too many legitimate transactions.

The enriched model reduces the alert volume substantially while still catching most fraud cases.

However, the model still requires threshold tuning before it can be considered operationally useful.

The main business question is now:

```text
What threshold gives the best balance between fraud capture and false positive cost?
```

Different risk policies may prefer different outcomes:

```text
High fraud-loss environment:
    prioritize recall

High customer-friction environment:
    prioritize precision

Manual review workflow:
    balance alert volume against review team capacity
```

---

## 13. Why PR-AUC Matters

The PR-AUC improved from:

```text
0.0024 → 0.1955
```

This is important because fraud detection is highly imbalanced.

In imbalanced classification, PR-AUC is often more informative than accuracy because it focuses on performance for the positive class.

The improvement suggests that the enriched features help the model rank fraudulent transactions much better than the generic baseline.

---

## 14. Engineering Interpretation

This experiment supports the feature engineering hypothesis.

The model did not improve because we changed to a more complex algorithm. It improved because we gave the model more meaningful fraud signals.

This is a key tabular ML lesson:

```text
Better features can matter more than a more complex model.
```

The enriched features helped the model understand balance movement behavior, which is highly relevant in financial fraud.

---

## 15. Current Limitations

The enriched model is better, but it is still not final.

Current limitations include:

1. The model still uses a random train/test split.
2. The classification threshold is still fixed at 0.5.
3. Precision is improved but still low.
4. False positives are lower but still operationally large.
5. False negatives now exist and need business review.
6. The model is still a Random Forest baseline.
7. There is no threshold tuning report yet.
8. There is no cost-sensitive evaluation yet.
9. There is no feature importance or explainability report yet.
10. There is no time-based validation yet.

---

## 16. Recommended Next Step: Threshold Tuning

The next experiment should tune the fraud score threshold.

Current threshold:

```text
0.5
```

Recommended thresholds to test:

```text
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
```

For each threshold, evaluate:

```text
precision
recall
F1
false positives
false negatives
true positives
manual review volume
recommended_action distribution
```

The goal is to find a threshold that is operationally useful, not just statistically interesting.

---

## 17. Recommended Experiment Plan

The next experiment should produce a threshold comparison table.

Example format:

| Threshold | Precision | Recall | F1 | False Positives | False Negatives | True Positives |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.2 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.3 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.4 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.5 | 0.0109 | 0.9157 | 0.0216 | 169,967 | 173 | 1,880 |
| 0.6 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.7 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.8 | TBD | TBD | TBD | TBD | TBD | TBD |
| 0.9 | TBD | TBD | TBD | TBD | TBD | TBD |

---

## 18. Portfolio Interpretation

This experiment is a strong portfolio milestone because it shows a complete ML improvement cycle:

```text
1. Build a baseline.
2. Measure performance.
3. Identify a weakness.
4. Form a feature engineering hypothesis.
5. Add targeted features.
6. Retrain the model.
7. Compare metrics.
8. Interpret the business trade-off.
9. Define the next experiment.
```

This demonstrates engineering maturity and practical machine learning judgment.

---

## 19. Summary

The PaySim-enriched model substantially improved performance compared with the generic baseline.

Key outcomes:

```text
False positives reduced by about 75%.
ROC-AUC improved from 0.7154 to 0.9473.
PR-AUC improved from 0.0024 to 0.1955.
Precision improved from 0.0030 to 0.0109.
Recall decreased from 1.0000 to 0.9157.
The model now has a more realistic precision-recall trade-off.
```

The enriched model is not final, but it is clearly better than the first baseline and provides a stronger foundation for threshold tuning.
