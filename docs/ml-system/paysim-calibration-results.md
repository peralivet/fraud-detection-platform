# PaySim Calibration Results

## 1. Purpose

This document records the probability calibration experiment for the PaySim-enriched fraud detection model.

The previous score distribution analysis showed that the uncalibrated Random Forest model produced fraud scores compressed around `0.50`.

The goal of this experiment is to answer:

```text
Can probability calibration produce more useful fraud scores for business thresholding?
```

---

## 2. Background

The PaySim-enriched model improved ranking performance compared with the generic baseline.

However, its score distribution was highly compressed:

```text
Non-fraud score range: 0.486192 → 0.515670
Fraud score range:     0.492208 → 0.515670
```

This caused unstable threshold behavior.

Small threshold changes around `0.50` created very large operational changes.

For example:

```text
Threshold 0.50:
    False positives: 169,967
    True positives: 1,880

Threshold 0.51:
    False positives: 8,318
    True positives: 842

Threshold 0.52:
    False positives: 0
    True positives: 0
```

This showed that the model could rank risk, but its raw probability scores were not well calibrated.

---

## 3. Calibration Method

A calibrated version of the PaySim-enriched Random Forest model was trained using scikit-learn's `CalibratedClassifierCV`.

The calibration method used was:

```text
sigmoid
```

The calibrated model uses the same enriched PaySim features as the uncalibrated model:

```text
customer_id
transaction_amount
transaction_hour
transaction_day_of_week
transaction_amount_log
merchant_category
payment_channel
origin_balance_delta
destination_balance_delta
amount_to_origin_balance_ratio
amount_to_destination_balance_ratio
```

The purpose of calibration is not simply to improve classification accuracy. The main goal is to make fraud scores more useful for thresholding and risk decisioning.

---

## 4. Training Command

The calibrated model was trained using:

```bash
python -m fraud_detection_platform.cli.train_paysim_enriched \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-type calibrated \
  --model-output-path models/paysim_calibrated_fraud_model.joblib \
  --scores-output-path reports/paysim_calibrated_test_scores.csv
```

The generated model and score files are local artifacts and should not be committed to Git.

---

## 5. Calibrated Model Result at Threshold 0.5

At the default threshold of `0.5`, the calibrated model produced:

```text
Precision: 0.0000
Recall: 0.0000
F1: 0.0000
ROC-AUC: 0.9642
PR-AUC: 0.2093
True negatives: 1,588,602
False positives: 0
False negatives: 2,053
True positives: 0
```

At first glance, this looks poor because the model predicts no fraud at threshold `0.5`.

However, this is expected in rare-event fraud detection.

Fraud is rare in the PaySim test set:

```text
2,053 fraud transactions out of 1,590,655 test rows
```

This is approximately:

```text
0.129%
```

A calibrated rare-event model should often produce useful fraud thresholds far below `0.5`.

Therefore, the correct next step was to evaluate lower thresholds.

---

## 6. Ranking Comparison

The calibrated model improved both ROC-AUC and PR-AUC compared with the uncalibrated enriched model.

| Metric | Uncalibrated Enriched Model | Calibrated Enriched Model | Change |
|---|---:|---:|---:|
| ROC-AUC | 0.9473 | 0.9642 | Improved |
| PR-AUC | 0.1955 | 0.2093 | Improved |

This means calibration did not only change the score scale. It also slightly improved ranking quality.

---

## 7. Calibrated Threshold Results

The calibrated score file was evaluated across lower thresholds.

Command:

```bash
python -m fraud_detection_platform.cli.evaluate_thresholds \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_calibrated_threshold_report.csv \
  --thresholds 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.075 0.10 0.15 0.20 0.30 0.40 0.50
```

Results:

| Threshold | Precision | Recall | F1 | False Positives | False Negatives | True Positives |
|---:|---:|---:|---:|---:|---:|---:|
| 0.001 | 0.008813 | 0.964929 | 0.017466 | 222,805 | 72 | 1,981 |
| 0.002 | 0.009382 | 0.934243 | 0.018578 | 202,514 | 135 | 1,918 |
| 0.005 | 0.014119 | 0.786654 | 0.027739 | 112,773 | 438 | 1,615 |
| 0.010 | 0.039480 | 0.546030 | 0.073636 | 27,273 | 932 | 1,121 |
| 0.020 | 0.043130 | 0.400877 | 0.077880 | 18,259 | 1,230 | 823 |
| 0.030 | 0.178109 | 0.221140 | 0.197306 | 2,095 | 1,599 | 454 |
| 0.040 | 0.203931 | 0.202143 | 0.203033 | 1,620 | 1,638 | 415 |
| 0.050 | 0.206570 | 0.202143 | 0.204333 | 1,594 | 1,638 | 415 |
| 0.075 | 0.443966 | 0.200682 | 0.276417 | 516 | 1,641 | 412 |
| 0.100 | 0.725762 | 0.127618 | 0.217067 | 99 | 1,791 | 262 |
| 0.150 | 0.856643 | 0.119338 | 0.209491 | 41 | 1,808 | 245 |
| 0.200 | 0.910448 | 0.029713 | 0.057547 | 6 | 1,992 | 61 |
| 0.300 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.400 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |
| 0.500 | 0.000000 | 0.000000 | 0.000000 | 0 | 2,053 | 0 |

---

## 8. Calibrated Score Distribution

The calibrated score distribution report was generated using:

```bash
python -m fraud_detection_platform.cli.analyze_score_distribution \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_calibrated_score_distribution_report.csv
```

Score distribution:

| Label | Count | Min Score | P01 | P05 | P10 | P25 | Median | P75 | P90 | P95 | P99 | Max Score | Mean Score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1,588,602 | 0.000135 | 0.000135 | 0.000135 | 0.000135 | 0.000250 | 0.000301 | 0.000397 | 0.002687 | 0.006002 | 0.024615 | 0.205730 | 0.001240 |
| 1 | 2,053 | 0.000250 | 0.000397 | 0.001448 | 0.002687 | 0.006878 | 0.011694 | 0.028368 | 0.159990 | 0.159990 | 0.205730 | 0.207924 | 0.038846 |

Label meaning:

```text
0 = non-fraud
1 = fraud
```

---

## 9. Score Distribution Interpretation

Calibration changed the score scale significantly.

Before calibration:

```text
Non-fraud range: 0.486192 → 0.515670
Fraud range:     0.492208 → 0.515670
```

After calibration:

```text
Non-fraud range: 0.000135 → 0.205730
Fraud range:     0.000250 → 0.207924
```

This is much more realistic for rare-event fraud detection.

Most non-fraud scores are very low:

```text
Non-fraud median: 0.000301
Non-fraud mean:   0.001240
Non-fraud p95:    0.006002
```

Fraud scores are still low in absolute terms, but much higher than non-fraud on average:

```text
Fraud median: 0.011694
Fraud mean:   0.038846
Fraud p75:    0.028368
Fraud p90:    0.159990
```

This shows that calibration made the model scores more useful for ranking and threshold selection.

---

## 10. Candidate Operating Thresholds

### Candidate 1: High-Recall Threshold

Threshold:

```text
0.005
```

Performance:

```text
Precision: 0.0141
Recall: 0.7867
False positives: 112,773
False negatives: 438
True positives: 1,615
```

This is useful if the business prioritizes fraud capture and can support a large review queue.

---

### Candidate 2: Balanced Threshold

Threshold:

```text
0.010
```

Performance:

```text
Precision: 0.0395
Recall: 0.5460
False positives: 27,273
False negatives: 932
True positives: 1,121
```

This threshold captures more than half of fraud cases while reducing false positives substantially compared with lower thresholds.

This is a strong candidate for a balanced fraud review policy.

---

### Candidate 3: Operational Review Threshold

Threshold:

```text
0.050
```

Performance:

```text
Precision: 0.2066
Recall: 0.2021
False positives: 1,594
False negatives: 1,638
True positives: 415
```

This threshold creates a much smaller review queue and may be more practical for limited fraud operations capacity.

---

### Candidate 4: Highest-Risk Queue Threshold

Threshold:

```text
0.100
```

Performance:

```text
Precision: 0.7258
Recall: 0.1276
False positives: 99
False negatives: 1,791
True positives: 262
```

This threshold is useful for a high-confidence fraud queue.

It should not be used as the only fraud detection threshold because it misses many fraud cases, but it is valuable for prioritizing the highest-risk transactions.

---

## 11. Recommended Risk Policy

The calibrated model supports a risk-band decision strategy.

A possible policy is:

```text
fraud_score < 0.010:
    approve

0.010 ≤ fraud_score < 0.050:
    manual_review

0.050 ≤ fraud_score < 0.100:
    high_risk_review

fraud_score ≥ 0.100:
    priority_investigation
```

A simpler three-band policy is:

```text
fraud_score < 0.010:
    approve

0.010 ≤ fraud_score < 0.075:
    manual_review

fraud_score ≥ 0.075:
    high_risk_review
```

Automatic blocking is not recommended yet without a business cost model and additional validation.

---

## 12. Comparison With Uncalibrated Thresholding

The uncalibrated model had unstable threshold behavior.

Useful thresholds were concentrated around:

```text
0.50 to 0.51
```

The calibrated model provides a wider and more interpretable threshold range:

```text
0.001 to 0.200
```

This is more useful for business decisioning because the organization can choose thresholds based on review capacity and fraud risk tolerance.

---

## 13. Business Interpretation

The calibrated model provides several operational options.

If the business wants broad fraud capture:

```text
Use threshold 0.005.
```

If the business wants a balanced review queue:

```text
Use threshold 0.010.
```

If the business wants a smaller manual review queue:

```text
Use threshold 0.050 or 0.075.
```

If the business wants a highest-risk priority queue:

```text
Use threshold 0.100 or 0.150.
```

This is more realistic than choosing a single default threshold of `0.5`.

---

## 14. Modeling Interpretation

Calibration improved the usefulness of the fraud score scale.

The model still does not perfectly separate fraud from non-fraud, but it now produces scores that are much easier to reason about.

The calibrated scores better reflect rare-event risk:

```text
Most non-fraud transactions have very low scores.
Fraud transactions have higher scores on average.
The highest-risk transactions are meaningfully separated.
```

This makes downstream thresholding, risk banding, and review prioritization more practical.

---

## 15. Current Limitations

The calibrated model is an improvement, but it is not final.

Current limitations include:

1. The model still uses a random train/test split.
2. The model has not been validated using time-based splitting.
3. The calibrated model uses sigmoid calibration only.
4. Isotonic calibration has not yet been compared.
5. No cost-sensitive threshold optimization has been implemented.
6. No fraud amount or loss-based cost model is included.
7. The model has not been tested for stability across different time windows.
8. Feature importance and explainability have not yet been added.
9. Automatic blocking thresholds have not been validated with business costs.
10. The model still uses Random Forest rather than boosted trees or specialized imbalanced-learning methods.

---

## 16. Recommended Next Improvements

Recommended next experiments:

```text
1. Compare sigmoid calibration with isotonic calibration.
2. Add cost-sensitive threshold evaluation.
3. Add business risk bands to the decision policy.
4. Add precision-recall curve export.
5. Add feature importance analysis.
6. Add time-based validation.
7. Compare Random Forest with gradient boosting models.
```

The most practical next step is cost-sensitive threshold evaluation.

A cost model would allow the project to estimate:

```text
cost of false positives
cost of false negatives
manual review cost
fraud loss avoided
net expected business value
```

---

## 17. Portfolio Interpretation

This calibration experiment strengthens the project significantly.

It shows that the project does not stop at model training. It evaluates whether the model output is usable for business decisions.

This demonstrates practical understanding of:

```text
rare-event fraud detection
probability calibration
threshold tuning
score distribution analysis
business risk bands
model decisioning
operational trade-offs
```

This is a strong machine learning engineering portfolio story.

---

## 18. Summary

The calibrated PaySim-enriched model improved both ranking and score usability.

Key outcomes:

```text
ROC-AUC improved from 0.9473 to 0.9642.
PR-AUC improved from 0.1955 to 0.2093.
Scores changed from compressed around 0.50 to a more realistic rare-event range.
Threshold choices became smoother and more operationally useful.
Threshold 0.010 is a strong balanced candidate.
Threshold 0.050 is a practical manual-review candidate.
Threshold 0.100 is a strong highest-risk queue candidate.
```

The next recommended improvement is cost-sensitive threshold evaluation.
