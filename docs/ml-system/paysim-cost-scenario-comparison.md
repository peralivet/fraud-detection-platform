# PaySim Cost Scenario Comparison

## 1. Purpose

This document records the cost scenario comparison for the calibrated PaySim fraud detection model.

The previous cost-sensitive threshold evaluation found that threshold `0.010` minimized estimated cost under one set of assumptions.

However, fraud operations may have different business priorities.

The goal of this experiment is to answer:

```text
Does the optimal fraud threshold change when business cost assumptions change?
```

---

## 2. Why Scenario Comparison Matters

A single threshold recommendation depends on the assumed cost of:

```text
false positives
false negatives
manual review workload
customer friction
missed fraud loss
```

In real fraud systems, these costs are rarely known with perfect certainty.

Therefore, a stronger evaluation tests multiple scenarios.

This avoids pretending that one cost assumption is universally correct.

---

## 3. Scenario Definitions

The following cost scenarios were evaluated.

### Scenario 1: Balanced Operations

```text
false positive cost: $5
false negative cost: $500
manual review cost: $2
```

This represents a balanced fraud operations environment where missed fraud is costly, but false positives and reviews also matter.

---

### Scenario 2: High Fraud Loss

```text
false positive cost: $5
false negative cost: $1,000
manual review cost: $2
```

This represents a business environment where missed fraud is especially expensive.

---

### Scenario 3: High Customer Friction

```text
false positive cost: $25
false negative cost: $500
manual review cost: $2
```

This represents a business environment where incorrectly flagging legitimate customers is expensive.

---

### Scenario 4: High Review Cost

```text
false positive cost: $5
false negative cost: $500
manual review cost: $10
```

This represents a fraud operations team with expensive or limited review capacity.

---

## 4. Report Command

The scenario comparison was generated using:

```bash
python -m fraud_detection_platform.cli.evaluate_cost_scenarios \
  --scores-path reports/paysim_calibrated_test_scores.csv \
  --output-path reports/paysim_cost_scenario_report.csv \
  --best-output-path reports/paysim_cost_scenario_best_thresholds.csv \
  --thresholds 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.075 0.10 0.15 0.20
```

The generated local report files were:

```text
reports/paysim_cost_scenario_report.csv
reports/paysim_cost_scenario_best_thresholds.csv
```

Generated report files are local artifacts and should not be committed to Git.

---

## 5. Best Threshold by Scenario

| Scenario | Best Threshold | False Positive Cost | False Negative Cost | Manual Review Cost | False Positives | False Negatives | Review Volume | Total Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| balanced_operations | 0.010 | $5 | $500 | $2 | 27,273 | 932 | 28,394 | $659,153 |
| high_fraud_loss | 0.010 | $5 | $1,000 | $2 | 27,273 | 932 | 28,394 | $1,125,153 |
| high_customer_friction | 0.075 | $25 | $500 | $2 | 516 | 1,641 | 928 | $835,256 |
| high_review_cost | 0.075 | $5 | $500 | $10 | 516 | 1,641 | 928 | $832,360 |

---

## 6. Key Finding

The optimal threshold changes depending on the business scenario.

```text
Balanced operations:
    best threshold = 0.010

High fraud loss:
    best threshold = 0.010

High customer friction:
    best threshold = 0.075

High review cost:
    best threshold = 0.075
```

This means there is no universal best fraud threshold.

The best threshold depends on the operating environment.

---

## 7. Balanced Operations Interpretation

For the balanced operations scenario:

```text
false positive cost: $5
false negative cost: $500
manual review cost: $2
```

The best threshold is:

```text
0.010
```

At threshold `0.010`:

```text
False positives: 27,273
False negatives: 932
Review volume: 28,394
Total cost: $659,153
```

This threshold balances fraud capture and review volume.

It does not minimize false positives, and it does not maximize recall. It minimizes total estimated cost under the balanced assumptions.

---

## 8. High Fraud Loss Interpretation

For the high fraud loss scenario:

```text
false positive cost: $5
false negative cost: $1,000
manual review cost: $2
```

The best threshold is still:

```text
0.010
```

At threshold `0.010`:

```text
False positives: 27,273
False negatives: 932
Review volume: 28,394
Total cost: $1,125,153
```

This shows that even when missed fraud becomes more expensive, threshold `0.010` remains the best among the tested thresholds.

Lower thresholds such as `0.005` catch more fraud, but they create enough false positives and review cost that they are still more expensive overall.

---

## 9. High Customer Friction Interpretation

For the high customer friction scenario:

```text
false positive cost: $25
false negative cost: $500
manual review cost: $2
```

The best threshold becomes:

```text
0.075
```

At threshold `0.075`:

```text
False positives: 516
False negatives: 1,641
Review volume: 928
Total cost: $835,256
```

When false positives are expensive, the model should be stricter.

Threshold `0.075` greatly reduces false positives and review volume, even though it misses more fraud.

This is appropriate when customer friction, complaints, or unnecessary account holds are expensive.

---

## 10. High Review Cost Interpretation

For the high review cost scenario:

```text
false positive cost: $5
false negative cost: $500
manual review cost: $10
```

The best threshold is also:

```text
0.075
```

At threshold `0.075`:

```text
False positives: 516
False negatives: 1,641
Review volume: 928
Total cost: $832,360
```

When manual review is expensive or review capacity is limited, the model should send fewer transactions to review.

Threshold `0.075` is attractive because it creates a much smaller review queue.

---

## 11. Business Recommendation

The threshold should be selected based on business priorities.

Recommended interpretation:

```text
Use threshold 0.010 when fraud capture is the priority.

Use threshold 0.075 when customer friction or review capacity is the priority.
```

A practical risk policy could combine both thresholds:

```text
fraud_score < 0.010:
    approve

0.010 ≤ fraud_score < 0.075:
    manual_review

fraud_score ≥ 0.075:
    high_risk_review
```

This allows the system to support both broad fraud detection and higher-priority fraud review.

---

## 12. Portfolio Interpretation

This experiment demonstrates business-aware ML evaluation.

The project no longer asks only:

```text
Which threshold has the best precision or recall?
```

It now asks:

```text
Which threshold is best under different business cost assumptions?
```

This is closer to real-world fraud model deployment because model thresholds are business decisions, not purely technical decisions.

---

## 13. Current Limitations

Current limitations include:

1. Cost assumptions are illustrative.
2. Fraud amount is not yet used to estimate transaction-specific loss.
3. All false negatives are assigned the same cost.
4. All false positives are assigned the same cost.
5. Review capacity is modeled only through a per-review cost.
6. Customer friction is simplified into the false positive cost.
7. Scenario definitions are hardcoded.
8. No time-based validation has been added yet.
9. No stakeholder-specific policy configuration exists yet.
10. No automated risk-band output has been integrated into calibrated predictions yet.

---

## 14. Recommended Next Step

The next engineering step should be a configurable risk-band decision policy.

The current project already has a basic decision policy for approve, manual review, and block-style recommendations.

The next improvement should extend this idea for calibrated fraud scores.

A calibrated risk policy could support:

```text
approve
manual_review
high_risk_review
priority_investigation
```

Example:

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

This would turn the calibrated model from a scoring system into an operational decision engine.

---

## 15. Summary

The cost scenario comparison found that the optimal threshold changes by business environment.

Key findings:

```text
Balanced operations selected threshold 0.010.
High fraud loss selected threshold 0.010.
High customer friction selected threshold 0.075.
High review cost selected threshold 0.075.
```

Main conclusion:

```text
There is no universal best threshold. The best threshold depends on business cost assumptions.
```

Recommended policy direction:

```text
Use 0.010 as the main review threshold when fraud capture matters.
Use 0.075 as a higher-risk threshold when review capacity or customer friction matters.
```
