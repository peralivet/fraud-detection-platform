# PaySim Calibrated Batch Inference Results

## 1. Purpose

This document records the calibrated PaySim batch inference workflow and risk action summary.

The goal of this stage is to move beyond model evaluation and produce a business-facing fraud scoring output.

The pipeline converts raw PaySim transactions into:

```text
fraud scores
binary fraud predictions
risk-band recommended actions
analyst-friendly scored transaction records
action-level management summaries
```

This demonstrates how the fraud model can support operational decision-making.

---

## 2. Model Used

The batch inference workflow used the calibrated PaySim-enriched fraud model.

Model artifact:

```text
models/paysim_calibrated_fraud_model.joblib
```

The calibrated model was trained using PaySim-enriched features and probability calibration.

The model produces calibrated fraud scores that are more useful for thresholding and risk-band assignment than the uncalibrated Random Forest scores.

---

## 3. Risk-Band Policy

The calibrated risk policy used the following thresholds:

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

The binary fraud prediction threshold was:

```text
0.010
```

This means transactions with a fraud score greater than or equal to `0.010` were assigned `fraud_prediction = 1`.

---

## 4. Batch Inference Command

The calibrated batch inference pipeline was run using:

```bash
python -m fraud_detection_platform.cli.paysim_batch_inference \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-path models/paysim_calibrated_fraud_model.joblib \
  --output-path reports/paysim_calibrated_scored_transactions.csv \
  --threshold 0.010 \
  --review-threshold 0.010 \
  --high-risk-threshold 0.075 \
  --priority-threshold 0.100
```

The scored output was written to:

```text
reports/paysim_calibrated_scored_transactions.csv
```

Generated model and report files are local artifacts and should not be committed to Git.

---

## 5. Scored Transaction Output

The batch inference pipeline scored:

```text
6,362,620 transactions
```

The scored CSV contains analyst-friendly columns:

```text
transaction_id
customer_id
transaction_time
transaction_amount
merchant_category
payment_channel
fraud_score
fraud_prediction
recommended_action
is_fraud
```

The `recommended_action` column is the main business decision column.

It assigns each transaction to one of the following categories:

```text
approve
manual_review
high_risk_review
priority_investigation
```

---

## 6. Action Distribution

The action distribution was:

| Recommended Action | Transaction Count |
|---|---:|
| approve | 6,248,594 |
| manual_review | 110,088 |
| high_risk_review | 2,252 |
| priority_investigation | 1,686 |

As percentages:

| Recommended Action | Percentage of Total |
|---|---:|
| approve | 98.21% |
| manual_review | 1.73% |
| high_risk_review | 0.035% |
| priority_investigation | 0.027% |

This creates a practical fraud operations funnel:

```text
approve:
    low-risk normal processing

manual_review:
    broad fraud review queue

high_risk_review:
    smaller elevated-risk queue

priority_investigation:
    highest-risk queue
```

---

## 7. Highest-Risk Sample

The top-ranked transactions were assigned to:

```text
priority_investigation
```

The highest-risk sample contained large `transfer` and `cash_out` transactions with high calibrated fraud scores.

In the inspected top 20 highest-risk transactions, all displayed records were actual fraud cases.

This suggests that the priority investigation queue is highly concentrated with fraudulent behavior.

---

## 8. Action Summary Report

An action-level summary report was generated using:

```bash
python -m fraud_detection_platform.cli.summarize_actions \
  --scored-path reports/paysim_calibrated_scored_transactions.csv \
  --output-path reports/paysim_action_summary.csv
```

The report was written to:

```text
reports/paysim_action_summary.csv
```

The summary includes:

```text
recommended_action
transaction_count
percentage_of_total
fraud_count
non_fraud_count
fraud_rate
average_fraud_score
average_transaction_amount
```

---

## 9. Action Summary Results

| Recommended Action | Transaction Count | Percentage of Total | Fraud Count | Non-Fraud Count | Fraud Rate | Average Fraud Score | Average Transaction Amount |
|---|---:|---:|---:|---:|---:|---:|---:|
| approve | 6,248,594 | 0.982079 | 3,404 | 6,245,190 | 0.000545 | 0.000846 | 160,445.90 |
| manual_review | 110,088 | 0.017302 | 3,048 | 107,040 | 0.027687 | 0.022530 | 1,231,613.00 |
| high_risk_review | 2,252 | 0.000354 | 489 | 1,763 | 0.217140 | 0.088316 | 1,194,280.00 |
| priority_investigation | 1,686 | 0.000265 | 1,272 | 414 | 0.754448 | 0.172211 | 2,109,186.00 |

---

## 10. Business Interpretation

The action summary shows that fraud concentration increases sharply as action severity increases.

Fraud rate by action:

```text
approve:                  0.0545%
manual_review:            2.77%
high_risk_review:         21.71%
priority_investigation:   75.44%
```

This is strong evidence that the risk bands are working as intended.

The `approve` group contains the overwhelming majority of transactions and has a very low fraud rate.

The `manual_review` group is broader and captures more suspicious activity, but it still contains many legitimate transactions.

The `high_risk_review` group is much smaller and has a substantially higher fraud rate.

The `priority_investigation` group is the most concentrated queue, with a fraud rate above `75%`.

---

## 11. Operational Value

The transaction-level scored file helps analysts investigate individual transactions.

The action summary helps managers understand workload and fraud concentration.

Together, these outputs support both:

```text
case-level investigation
management-level monitoring
```

A risk manager could use the action summary to answer:

```text
How many transactions are being approved?
How large is the manual review queue?
How concentrated is fraud in the high-risk queue?
How many transactions require priority investigation?
What is the fraud rate in each action band?
```

---

## 12. Portfolio Interpretation

This is a strong portfolio milestone because it shows a complete operational ML workflow.

The project now supports:

```text
raw transaction ingestion
feature engineering
model training
probability calibration
threshold tuning
cost-sensitive threshold evaluation
cost scenario comparison
risk-band decision policy
batch scoring
analyst-facing transaction output
management-level action summary
```

This demonstrates the difference between a model and a deployable ML decision system.

---

## 13. Current Limitations

Current limitations include:

1. The workflow still uses PaySim simulated data.
2. The train/test split is still random rather than time-based.
3. The risk-band thresholds are based on illustrative cost assumptions.
4. The action summary uses labels available in PaySim, but real production scoring would not include known labels at scoring time.
5. The model has not been deployed behind an API.
6. No dashboard has been built yet.
7. No drift monitoring has been implemented yet.
8. No human review feedback loop has been added yet.
9. No alerting or SLA tracking exists yet.
10. No time-window monitoring has been added yet.

---

## 14. Recommended Next Improvements

Recommended next improvements:

```text
1. Add a production-style scoring mode without is_fraud labels.
2. Add a dashboard or report for risk action monitoring.
3. Add time-based validation.
4. Add model explainability for high-risk transactions.
5. Add monitoring for score drift and action distribution drift.
6. Add an API endpoint for real-time scoring.
7. Add a feedback loop for analyst review outcomes.
```

The most practical next step is to add a production-style scoring mode that excludes `is_fraud` from the output when labels are not available.

---

## 15. Summary

The calibrated PaySim batch inference workflow scored `6,362,620` transactions and assigned each transaction to a risk action.

Key outcomes:

```text
98.21% of transactions were approved.
1.73% were sent to manual review.
0.035% were sent to high-risk review.
0.027% were sent to priority investigation.
```

The priority investigation queue contained:

```text
1,686 transactions
1,272 fraud cases
75.44% fraud rate
```

This demonstrates an end-to-end fraud scoring workflow that converts calibrated model probabilities into business-ready risk actions.
