# PaySim Cost-Sensitive Threshold Results

## 1. Purpose

This document records the cost-sensitive threshold evaluation for the calibrated PaySim fraud detection model.

Previous experiments compared thresholds using machine learning metrics such as:

```text

precision

recall

F1

false positives

false negatives

```

This experiment adds a business-cost layer.

The goal is to answer:

```text

Which fraud threshold minimizes estimated business cost under stated assumptions?

```

---

## 2. Background

The calibrated PaySim-enriched model produced more useful fraud scores than the uncalibrated model.

The calibrated model improved score behavior and allowed threshold tuning across lower rare-event probability thresholds such as:

```text

0.001

0.005

0.010

0.030

0.050

0.100

```

However, choosing a threshold only from precision and recall is incomplete.

Fraud operations must also consider the cost of:

```text

false positives

false negatives

manual review workload

```

This experiment estimates those costs for each threshold.

---

## 3. Cost Assumptions

The following cost assumptions were used:

```text

False positive cost: $5

False negative cost: $500

Manual review cost: $2

```

Definitions:

```text

False positive cost:

    Cost of incorrectly flagging a legitimate transaction.

False negative cost:

    Cost of missing a fraudulent transaction.

Manual review cost:

    Cost of reviewing one transaction predicted as fraud.

```

These values are assumptions for portfolio analysis. In a real business environment, they should be replaced with validated business estimates.

---

## 4. Cost Formula

For each threshold:

```text

predicted_positive_count = false_positives + true_positives

```

Then:

```text

false_positive_cost_total = false_positives * false_positive_cost

false_negative_cost_total = false_negatives * false_negative_cost

manual_review_cost_total = predicted_positive_count * manual_review_cost

```

Total cost:

```text

total_cost =

    false_positive_cost_total

    + false_negative_cost_total

    + manual_review_cost_total

```

---

## 5. Report Command

The cost-sensitive threshold report was generated using:

```bash

python -m fraud_detection_platform.cli.evaluate_threshold_costs \

  --scores-path reports/paysim_calibrated_test_scores.csv \

  --output-path reports/paysim_calibrated_cost_report.csv \

  --thresholds 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.075 0.10 0.15 0.20 \

  --false-positive-cost 5 \

  --false-negative-cost 500 \

  --manual-review-cost 2

```

The output report was written to:

```text

reports/paysim_calibrated_cost_report.csv

```

Generated report files are local artifacts and should not be committed to Git.

---

## 6. Ranked Cost Results

The thresholds sorted by lowest total cost were:

| Threshold | False Positives | False Negatives | Review Volume | False Positive Cost | False Negative Cost | Manual Review Cost | Total Cost |

|---:|---:|---:|---:|---:|---:|---:|---:|

| 0.010 | 27,273 | 932 | 28,394 | $136,365 | $466,000 | $56,788 | $659,153 |

| 0.020 | 18,259 | 1,230 | 19,082 | $91,295 | $615,000 | $38,164 | $744,459 |

| 0.030 | 2,095 | 1,599 | 2,549 | $10,475 | $799,500 | $5,098 | $815,073 |

| 0.075 | 516 | 1,641 | 928 | $2,580 | $820,500 | $1,856 | $824,936 |

| 0.050 | 1,594 | 1,638 | 2,009 | $7,970 | $819,000 | $4,018 | $830,988 |

| 0.040 | 1,620 | 1,638 | 2,035 | $8,100 | $819,000 | $4,070 | $831,170 |

| 0.100 | 99 | 1,791 | 361 | $495 | $895,500 | $722 | $896,717 |

| 0.150 | 41 | 1,808 | 286 | $205 | $904,000 | $572 | $904,777 |

| 0.200 | 6 | 1,992 | 67 | $30 | $996,000 | $134 | $996,164 |

| 0.005 | 112,773 | 438 | 114,388 | $563,865 | $219,000 | $228,776 | $1,011,641 |

| 0.002 | 202,514 | 135 | 204,432 | $1,012,570 | $67,500 | $408,864 | $1,488,934 |

| 0.001 | 222,805 | 72 | 224,786 | $1,114,025 | $36,000 | $449,572 | $1,599,597 |

---

## 7. Best Threshold Under Current Assumptions

The lowest-cost threshold is:

```text

0.010

```

At threshold `0.010`:

```text

False positives: 27,273

False negatives: 932

Predicted positives / review volume: 28,394

Total estimated cost: $659,153

```

This threshold balances fraud capture and review workload better than the other tested thresholds under the stated assumptions.

---

## 8. Why Threshold 0.010 Wins

Threshold `0.010` does not have the highest recall, and it does not have the highest precision.

It wins because it provides the best cost trade-off.

Compared with threshold `0.005`:

```text

Threshold 0.005:

    False positives: 112,773

    False negatives: 438

    Total cost: $1,011,641

Threshold 0.010:

    False positives: 27,273

    False negatives: 932

    Total cost: $659,153

```

Threshold `0.005` catches more fraud, but it creates a much larger false positive and manual review burden.

Compared with threshold `0.030`:

```text

Threshold 0.030:

    False positives: 2,095

    False negatives: 1,599

    Total cost: $815,073

Threshold 0.010:

    False positives: 27,273

    False negatives: 932

    Total cost: $659,153

```

Threshold `0.030` has a smaller review queue, but it misses more fraud. Under the assumption that each missed fraud costs `$500`, those false negatives make it more expensive overall.

---

## 9. Business Interpretation

The cost-sensitive result changes the threshold discussion.

Without costs, possible threshold recommendations were:

```text

0.005 for high recall

0.010 for balanced fraud capture

0.050 for operational review

0.100 for highest-risk queue

```

With the current cost assumptions, the recommended threshold is:

```text

0.010

```

This threshold is cost-optimal because it avoids excessive review workload while still catching enough fraud to reduce missed-fraud cost.

---

## 10. Risk Policy Recommendation

A practical risk policy could be:

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

The threshold `0.010` acts as the main cost-sensitive review threshold.

Thresholds `0.050` and `0.100` can still be useful for prioritizing higher-risk transactions inside the review workflow.

---

## 11. Sensitivity Warning

The threshold recommendation depends on the cost assumptions.

If missed fraud is much more expensive than `$500`, a lower threshold such as `0.005` may become better.

If manual review or customer friction is more expensive, a higher threshold such as `0.030`, `0.050`, or `0.075` may become better.

Therefore, this result should be interpreted as:

```text

Threshold 0.010 is cost-optimal under the stated assumptions.

```

not:

```text

Threshold 0.010 is universally optimal.

```

---

## 12. Portfolio Interpretation

This experiment strengthens the project because it shows business-aware model evaluation.

The project now evaluates thresholds using:

```text

classification metrics

score distribution

probability calibration

estimated business cost

```

This is much closer to production fraud modeling than simply reporting accuracy or ROC-AUC.

It demonstrates the ability to connect model behavior to operational decision-making.

---

## 13. Current Limitations

Current limitations include:

1. Cost assumptions are illustrative, not validated business values.

2. Fraud amount is not yet used to estimate transaction-specific loss.

3. All false negatives are assigned the same cost.

4. All false positives are assigned the same cost.

5. Manual review capacity limits are not explicitly modeled.

6. Customer friction cost is simplified into the false positive cost.

7. There is no time-based validation yet.

8. There is no sensitivity analysis across multiple cost scenarios yet.

---

## 14. Recommended Next Improvements

Recommended next steps:

```text

1. Add cost scenario comparison.

2. Test multiple false negative cost assumptions.

3. Use transaction amount to estimate fraud loss.

4. Add review capacity constraints.

5. Add risk-band decision policy to the pipeline.

6. Export a final business evaluation summary.

```

The most practical next step is cost scenario comparison.

That would test how the optimal threshold changes under different business assumptions.

Example scenarios:

```text

Low fraud loss scenario

Medium fraud loss scenario

High fraud loss scenario

High review cost scenario

High customer friction scenario

```

---

## 15. Summary

The cost-sensitive threshold evaluation found that threshold `0.010` minimizes estimated business cost under the following assumptions:

```text

False positive cost: $5

False negative cost: $500

Manual review cost: $2

```

At threshold `0.010`:

```text

False positives: 27,273

False negatives: 932

Review volume: 28,394

Total estimated cost: $659,153

```

This result provides a business-facing threshold recommendation for the calibrated PaySim fraud model.
