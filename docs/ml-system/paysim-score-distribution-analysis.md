# PaySim Score Distribution Analysis

## 1. Purpose

This document records the score distribution analysis for the PaySim-enriched fraud detection model.

The previous threshold tuning experiment showed that small threshold changes around `0.50` caused very large changes in false positives and false negatives.

The goal of this analysis is to understand why that happened by examining how fraud scores are distributed for:

```text
non-fraud transactions
fraud transactions
```

---

## 2. Input Data

The score distribution report was generated from the enriched model test-set score file:

```text
reports/paysim_enriched_test_scores.csv
```

This file contains:

```text
is_fraud
fraud_score
fraud_prediction
```

The report was generated using:

```bash
python -m fraud_detection_platform.cli.analyze_score_distribution \
  --scores-path reports/paysim_enriched_test_scores.csv \
  --output-path reports/paysim_score_distribution_report.csv
```

---

## 3. Score Distribution Report

| Label | Count | Min Score | P01 | P05 | P10 | P25 | Median | P75 | P90 | P95 | P99 | Max Score | Mean Score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1,588,602 | 0.486192 | 0.486192 | 0.486192 | 0.486192 | 0.486192 | 0.492208 | 0.496826 | 0.502124 | 0.504879 | 0.505561 | 0.515670 | 0.493045 |
| 1 | 2,053 | 0.492208 | 0.492208 | 0.496826 | 0.500262 | 0.504879 | 0.505561 | 0.510371 | 0.515670 | 0.515670 | 0.515670 | 0.515670 | 0.506416 |

Label meaning:

```text
0 = non-fraud
1 = fraud
```

---

## 4. Main Finding

The model scores are highly compressed.

Non-fraud transactions fall within this score range:

```text
0.486192 → 0.515670
```

Fraud transactions fall within this score range:

```text
0.492208 → 0.515670
```

This means almost all predictions are squeezed into a narrow band around `0.50`.

The model does separate fraud from non-fraud somewhat, but the score values are not well spread out.

---

## 5. Non-Fraud Score Behavior

For non-fraud transactions:

```text
count:       1,588,602
min score:   0.486192
median:      0.492208
mean score:  0.493045
p95 score:   0.504879
max score:   0.515670
```

Most non-fraud transactions are below `0.50`, but a meaningful number extend above `0.50`.

This explains why threshold `0.50` still produces many false positives.

---

## 6. Fraud Score Behavior

For fraud transactions:

```text
count:       2,053
min score:   0.492208
median:      0.505561
mean score:  0.506416
p25 score:   0.504879
max score:   0.515670
```

Most fraud transactions are slightly above the non-fraud median, but there is still overlap between fraud and non-fraud scores.

This explains why threshold `0.51` reduces false positives but also misses many fraud cases.

---

## 7. Why Threshold Tuning Was So Sensitive

The previous threshold tuning experiment showed:

```text
threshold 0.49:
    catches all fraud but creates over 1 million false positives

threshold 0.50:
    catches most fraud but creates 169,967 false positives

threshold 0.51:
    greatly reduces false positives but misses many fraud cases

threshold 0.52:
    catches no fraud
```

The score distribution explains this behavior.

Most scores are packed between:

```text
0.486 and 0.516
```

Therefore, small threshold changes inside this range move very large groups of transactions from one side of the decision boundary to the other.

---

## 8. Probability Calibration Insight

The enriched model has strong ranking performance:

```text
ROC-AUC: 0.9473
PR-AUC: 0.1955
```

However, the score distribution shows that the fraud scores should not be interpreted as calibrated probabilities.

For example:

```text
fraud_score = 0.51
```

should not be interpreted as:

```text
51% probability of fraud
```

Instead, it should be interpreted as:

```text
higher risk than many transactions, but not a calibrated fraud probability
```

This is an important distinction.

The model can rank fraud risk well while still producing poorly calibrated probability estimates.

---

## 9. Modeling Interpretation

This behavior is common with tree-based models such as Random Forests.

Random Forest probability estimates are based on the proportion of trees voting for each class. In highly imbalanced datasets, those estimates can become compressed and poorly calibrated.

The model is useful for ranking transactions, but the raw score scale is not yet ideal for business decisioning.

---

## 10. Operational Interpretation

The score distribution suggests that threshold selection is fragile.

Because most scores are near `0.50`, a tiny threshold change can dramatically alter:

```text
manual review volume
false positive count
fraud capture rate
customer friction
missed fraud
```

This means a production fraud system should not rely only on the raw Random Forest probability score.

The score should either be calibrated or converted into a business risk band after additional validation.

---

## 11. Recommended Next Improvement

The next modeling improvement should be probability calibration.

Recommended options:

```text
CalibratedClassifierCV with sigmoid calibration
CalibratedClassifierCV with isotonic calibration
logistic regression calibration layer
cost-sensitive threshold selection
precision-recall curve export
score banding into approve / review / block actions
```

The immediate next experiment should compare:

```text
uncalibrated PaySim-enriched Random Forest
calibrated PaySim-enriched Random Forest
```

The goal is not necessarily to improve ROC-AUC. The goal is to produce scores that are more useful and stable for business thresholding.

---

## 12. Portfolio Interpretation

This diagnostic step strengthens the project because it shows mature ML judgment.

The project does not stop at model accuracy or ROC-AUC. It investigates whether the model scores are usable for operational decisions.

This demonstrates understanding of:

```text
imbalanced classification
threshold tuning
score distribution analysis
probability calibration
fraud operations trade-offs
business decisioning
```

This is exactly the type of thinking expected in production machine learning systems.

---

## 13. Summary

The score distribution analysis found that the PaySim-enriched model produces compressed fraud scores.

Key findings:

```text
Non-fraud scores range from about 0.486 to 0.516.
Fraud scores range from about 0.492 to 0.516.
Fraud scores are generally higher than non-fraud scores, but there is overlap.
The model ranks risk well but does not produce well-calibrated probabilities.
Small threshold changes around 0.50 create large operational changes.
```

Recommended next step:

```text
Add probability calibration and compare calibrated vs uncalibrated score behavior.
```
