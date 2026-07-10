# PaySim Threshold Tuning Results

## 1. Purpose

This document records the threshold tuning experiment for the PaySim-enriched fraud detection model.

The enriched model improved ranking performance compared with the generic PaySim baseline, but the default classification threshold of `0.5` may not be the best business threshold.

The goal of this experiment is to answer:

```text
Which fraud score threshold creates the best operational trade-off between fraud capture and false positive volume?
```

---

## 2. Background

The PaySim-enriched model was trained using generic transaction features plus PaySim-specific balance movement features.

The enriched model produced the following baseline result at threshold `0.5`:

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

The model showed strong ranking ability:

```text
ROC-AUC: 0.9473
PR-AUC: 0.1955
```

However, fraud detection is not only a ranking problem. The business also needs a decision threshold that determines which transactions are approved, reviewed, or blocked.

---

## 3. Why Threshold Tuning Matters

A model outputs a fraud score, but the business must decide how to act on that score.

For example:

```text
fraud_score = 0.50
```

could mean:

```text
approve
manual review
block
```

depending on the business policy.

Lower thresholds usually produce:

```text
higher recall
more fraud caught
more false positives
larger review workload
more customer friction
```

Higher thresholds usually produce:

```text
higher precision
fewer false positives
smaller review workload
more missed fraud
```

The best threshold depends on business priorities, including:

```text
fraud loss cost
manual review capacity
customer friction
regulatory requirements
false negative risk
false positive risk
```

---

## 4. Threshold Evaluation Method

The enriched training pipeline exported test-set scores to:

```text
reports/paysim_enriched_test_scores.csv
```

The score file contains:

```text
is_fraud
fraud_score
fraud_prediction
```

The threshold evaluation CLI was then used to generate reports.

Broad threshold report command:

```bash
python -m fraud_detection_platform.cli.evaluate_thresholds \
  --scores-path reports/paysim_enriched_test_scores.csv \
  --output-path reports/paysim_threshold_report.csv
```

Fine threshold report command:

```bash
python -m fraud_detection_platform.cli.evaluate_thresholds \
  --scores-path reports/paysim_enriched_test_scores.csv \
  --output-path reports/paysim_threshold_report_fine.csv \
  --thresholds 0.41 0.42 0.43 0.44 0.45 0.46 0.47 0.48 0.49 0.50 0.51 0.52 0.53 0.54 0.55 0.56 0.57 0.58 0.59
```

---

## 5. Broad Threshold Results

| Threshold | Precision | Recall | F1 | False Positives | False Negatives | True Positives |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.2 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.3 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.4 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.5 | 0.010940 | 0.915733 | 0.021622 | 169,967 | 173 | 1,880 |
| 0.6 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.7 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.8 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.9 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |

---

## 6. Broad Threshold Interpretation

The broad threshold report shows that the useful decision boundary is not spread evenly from `0.1` to `0.9`.

Instead, model behavior changes sharply around `0.5`.

At thresholds `0.1` through `0.4`, the model predicts every transaction as fraud:

```text
True negatives: 0
False positives: 1,588,602
False negatives: 0
True positives: 2,053
```

This catches all fraud, but it is operationally unusable because it sends every legitimate transaction to fraud review.

At thresholds `0.6` through `0.9`, the model predicts no transactions as fraud:

```text
True negatives: 1,588,602
False positives: 0
False negatives: 2,053
True positives: 0
```

This avoids false positives, but it misses every fraud case.

Therefore, the useful threshold range is concentrated between:

```text
0.49 and 0.51
```

---

## 7. Fine Threshold Results

| Threshold | Precision | Recall | F1 | False Positives | False Negatives | True Positives |
|---:|---:|---:|---:|---:|---:|---:|
| 0.41 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.42 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.43 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.44 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.45 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.46 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.47 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.48 | 0.001291 | 1.000000 | 0.002578 | 1,588,602 | 0 | 2,053 |
| 0.49 | 0.001914 | 1.000000 | 0.003820 | 1,070,812 | 0 | 2,053 |
| 0.50 | 0.010940 | 0.915733 | 0.021622 | 169,967 | 173 | 1,880 |
| 0.51 | 0.091921 | 0.410132 | 0.150183 | 8,318 | 1,211 | 842 |
| 0.52 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.53 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.54 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.55 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.56 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.57 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.58 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.59 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |

---

## 8. Fine Threshold Interpretation

The fine threshold report confirms that the model score distribution is highly concentrated.

The most important thresholds are:

```text
0.49
0.50
0.51
0.52
```

At threshold `0.49`, the model still catches all fraud cases, but false positives remain extremely high:

```text
False positives: 1,070,812
False negatives: 0
True positives: 2,053
```

At threshold `0.50`, the model catches most fraud cases and greatly reduces false positives:

```text
False positives: 169,967
False negatives: 173
True positives: 1,880
```

At threshold `0.51`, the model produces a much smaller review queue but misses more fraud:

```text
False positives: 8,318
False negatives: 1,211
True positives: 842
```

At threshold `0.52`, the model catches no fraud:

```text
False positives: 0
False negatives: 2,053
True positives: 0
```

This means the model is not well-calibrated as a probability estimator. Its scores are useful for ranking, but small changes in threshold cause large operational changes.

---

## 9. Candidate Operating Thresholds

### Candidate 1: High-Recall Threshold

Recommended threshold:

```text
0.50
```

Performance:

```text
Precision: 0.0109
Recall: 0.9157
False positives: 169,967
False negatives: 173
True positives: 1,880
```

This threshold is appropriate when the business prioritizes fraud capture and can tolerate a large manual review queue.

Advantages:

```text
catches most fraud cases
misses relatively few fraud transactions
strong fraud prevention posture
```

Disadvantages:

```text
large false positive volume
high manual review workload
higher customer friction
```

---

### Candidate 2: Operationally Practical Threshold

Recommended threshold:

```text
0.51
```

Performance:

```text
Precision: 0.0919
Recall: 0.4101
False positives: 8,318
False negatives: 1,211
True positives: 842
```

This threshold is appropriate when the business needs a smaller, more realistic review queue.

Advantages:

```text
substantially fewer false positives
higher precision
more manageable review workload
less customer friction
```

Disadvantages:

```text
misses more fraud cases
lower recall
requires business acceptance of higher fraud leakage
```

---

## 10. Trade-Off Between 0.50 and 0.51

Moving from threshold `0.50` to `0.51` changes the model behavior significantly.

False positives:

```text
169,967 → 8,318
```

Reduction:

```text
161,649 fewer false positives
```

True positives:

```text
1,880 → 842
```

Reduction:

```text
1,038 fewer fraud cases caught
```

False negatives:

```text
173 → 1,211
```

Increase:

```text
1,038 more missed fraud cases
```

This is the central business trade-off:

```text
Threshold 0.50:
    better fraud capture

Threshold 0.51:
    better operational practicality
```

---

## 11. Recommendation

For this portfolio project, both thresholds should be presented as valid operating candidates.

Recommended framing:

```text
Threshold 0.50 is the high-recall fraud prevention threshold.
Threshold 0.51 is the operationally practical manual-review threshold.
```

The final production threshold should depend on business costs.

If the cost of missed fraud is high, choose threshold `0.50`.

If the cost of false positives and manual review is high, choose threshold `0.51`.

Without explicit business cost assumptions, threshold `0.51` may be more operationally realistic because it reduces false positives from `169,967` to `8,318`.

However, threshold `0.50` is safer from a fraud prevention perspective because it catches `1,880` of `2,053` fraud cases.

---

## 12. Why ROC-AUC and PR-AUC Do Not Change by Threshold

ROC-AUC and PR-AUC remain constant across the threshold table:

```text
ROC-AUC: 0.947274
PR-AUC: 0.195480
```

This is expected.

ROC-AUC and PR-AUC measure ranking quality across the full range of possible thresholds.

Threshold-specific metrics include:

```text
precision
recall
F1
false positives
false negatives
true positives
true negatives
```

These metrics change when the threshold changes.

Therefore, the model can have strong ROC-AUC and PR-AUC while still requiring careful threshold tuning for operational use.

---

## 13. Modeling Insight: Score Clustering

The threshold results show that the Random Forest model produces clustered fraud scores.

This is visible because:

```text
thresholds below 0.49 flag nearly everything
threshold 0.50 creates a large behavior shift
threshold 0.51 creates another large behavior shift
threshold 0.52 flags nothing
```

This suggests the model ranking is useful, but the probability scores are not smoothly calibrated.

This is common for tree-based models such as Random Forests.

The model can rank fraud risk well, but the predicted probabilities should not yet be interpreted as perfectly calibrated fraud probabilities.

---

## 14. Recommended Next Improvement

The next improvement should be probability calibration and score distribution analysis.

Recommended next experiments:

```text
1. Score distribution report
2. Probability calibration using CalibratedClassifierCV
3. Cost-sensitive threshold selection
4. Precision-recall curve export
5. Business cost simulation
```

The immediate next step should be a score distribution report to understand how fraud and non-fraud scores are distributed.

This would help explain why tiny threshold changes between `0.49` and `0.52` produce large operational changes.

---

## 15. Portfolio Interpretation

This threshold tuning experiment strengthens the project because it shows that model evaluation is not limited to one default threshold.

The project now demonstrates:

```text
baseline modeling
feature engineering
real dataset ingestion
model comparison
threshold tuning
business trade-off analysis
operational decision framing
```

This is closer to how fraud models are evaluated in real financial systems.

---

## 16. Summary

The threshold tuning experiment found that the PaySim-enriched model has a narrow useful threshold range.

Key findings:

```text
Thresholds 0.1 to 0.48 flag nearly all transactions.
Threshold 0.49 catches all fraud but creates over 1 million false positives.
Threshold 0.50 catches most fraud but creates 169,967 false positives.
Threshold 0.51 greatly reduces false positives to 8,318 but catches fewer fraud cases.
Thresholds 0.52 and above catch no fraud.
```

Recommended operating candidates:

```text
0.50 for high-recall fraud prevention
0.51 for operationally practical manual review
```

The next modeling improvement should focus on score distribution analysis and probability calibration.
