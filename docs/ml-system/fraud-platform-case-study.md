# Fraud Detection Platform Case Study

## 1. Problem

Fraud detection is a high-impact machine learning problem where the goal is not only to identify suspicious transactions, but to support operational decisions.

A fraud detection system must help the business answer questions such as:

```text
Which transactions should be approved automatically?
Which transactions should be sent to manual review?
Which transactions require urgent investigation?
How many false positives can the business tolerate?
How costly is it to miss fraud?
How should model scores be converted into business actions?
```

This project was built to demonstrate a production-oriented fraud detection workflow that goes beyond model training.

The system turns transaction data into calibrated fraud scores, cost-aware thresholds, risk-band actions, analyst-facing scored outputs, and management-level summaries.

---

## 2. Why This Problem Is Hard

Fraud detection is challenging because fraud is a rare event.

Most transactions are legitimate, so a model can appear accurate while still failing to catch meaningful fraud.

For example, if fraud represents less than 1% of all transactions, a model that predicts every transaction as legitimate could have very high accuracy but no business value.

This makes metrics such as accuracy misleading.

More useful questions include:

```text
How many fraud cases are caught?
How many legitimate customers are incorrectly flagged?
How concentrated is fraud in the highest-risk queue?
What is the trade-off between false positives and false negatives?
What threshold minimizes business cost?
```

A practical fraud detection system must balance technical model performance with business constraints such as review capacity, customer friction, fraud loss, and investigation cost.

---

## 3. Dataset Strategy

The project supports two data paths.

### Synthetic Data

Synthetic transaction data is used for fast development and lightweight automated tests.

This keeps the test suite reproducible and avoids requiring large external datasets during CI runs.

### PaySim Data

The main realistic workflow uses the PaySim mobile money simulation dataset.

PaySim provides transaction-level fraud labels and balance movement fields that can be used to simulate fraud detection workflows.

The raw PaySim dataset is stored locally and is not committed to Git.

Expected local path:

```text
data/external/PS_20174392719_1491204439457_log.csv
```

The project ingests and transforms more than:

```text
6.36 million transactions
```

---

## 4. Approach

The project was designed as a modular Python machine learning system rather than a notebook-only experiment.

The workflow includes:

```text
data validation
PaySim data adaptation
feature engineering
baseline modeling
PaySim-enriched modeling
probability calibration
threshold tuning
score distribution analysis
cost-sensitive threshold evaluation
cost scenario comparison
risk-band decisioning
batch inference
production-style scoring
action summary reporting
```

The goal was to show how model outputs can become practical business decisions.

---

## 5. System Design

The platform is organized as a Python package:

```text
src/fraud_detection_platform/
├── cli/
├── data/
├── evaluation/
├── features/
├── models/
├── pipelines/
└── risk/
```

Each area has a specific responsibility.

```text
data:
    Loading, validation, schema definitions, and PaySim transformation.

features:
    Generic transaction features and PaySim-specific balance movement features.

models:
    Baseline Random Forest, PaySim-enriched Random Forest, and calibrated model.

evaluation:
    Classification metrics, threshold analysis, score distribution,
    cost-sensitive evaluation, scenario comparison, and action summaries.

risk:
    Business decision policies that convert fraud scores into recommended actions.

pipelines:
    End-to-end training and batch inference workflows.

cli:
    Command-line interfaces for running workflows.
```

This structure separates model logic, feature logic, evaluation logic, and business decisioning logic.

That separation makes the project easier to test, maintain, and extend.

---

## 6. Feature Engineering

The project starts with generic transaction features such as:

```text
transaction hour
transaction day of week
log transaction amount
merchant category
payment channel
customer identifier
```

The PaySim-enriched workflow adds fraud-specific balance movement features:

```text
origin_balance_delta
destination_balance_delta
amount_to_origin_balance_ratio
amount_to_destination_balance_ratio
```

These features capture how money moves between accounts and whether the transaction amount is unusual relative to account balances.

This was a major improvement over the generic baseline.

---

## 7. Baseline Model

The first PaySim baseline used generic platform features only.

Result:

```text
Precision: 0.0030
Recall: 1.0000
F1: 0.0059
ROC-AUC: 0.7154
PR-AUC: 0.0024
False positives: 690,372
False negatives: 0
True positives: 2,053
```

The model caught all fraud cases, but it produced too many false positives.

This is a common fraud detection problem: maximizing recall can overwhelm the business with too many legitimate transactions sent to review.

---

## 8. PaySim-Enriched Model

The enriched model used PaySim balance movement features.

Result:

```text
Precision: 0.0109
Recall: 0.9157
F1: 0.0216
ROC-AUC: 0.9473
PR-AUC: 0.1955
False positives: 169,967
False negatives: 173
True positives: 1,880
```

Compared with the generic baseline, the enriched model reduced false positives from:

```text
690,372 to 169,967
```

This is a reduction of about:

```text
75%
```

The enriched features substantially improved the model's ability to separate suspicious transactions from legitimate ones.

---

## 9. Probability Calibration

The uncalibrated enriched model ranked fraud risk well, but its scores were compressed around 0.50.

This made threshold selection unstable.

A calibrated model was trained to make the fraud scores more useful for decisioning.

Comparison:

| Metric | Uncalibrated Enriched Model | Calibrated Enriched Model |
|---|---:|---:|
| ROC-AUC | 0.9473 | 0.9642 |
| PR-AUC | 0.1955 | 0.2093 |

Calibrated score distribution:

```text
Non-fraud mean score: 0.001240
Fraud mean score:     0.038846
```

Calibration produced more realistic rare-event probabilities and made thresholding more practical.

---

## 10. Threshold Tuning

Threshold tuning was used to compare model behavior across different decision thresholds.

The calibrated model allowed more meaningful threshold choices than the uncalibrated model.

Useful calibrated thresholds included:

```text
0.005
0.010
0.030
0.050
0.075
0.100
0.150
```

Different thresholds created different trade-offs between fraud recall, false positives, and review volume.

---

## 11. Cost-Sensitive Evaluation

Fraud thresholds should be business decisions, not purely technical choices.

The project added cost-sensitive threshold evaluation using configurable assumptions:

```text
False positive cost: $5
False negative cost: $500
Manual review cost: $2
```

Under these assumptions, the best threshold was:

```text
0.010
```

At threshold `0.010`:

```text
False positives: 27,273
False negatives: 932
Predicted positive / review volume: 28,394
Total estimated cost: $659,153
```

This showed how cost assumptions can guide threshold selection.

---

## 12. Cost Scenario Comparison

The project also compared thresholds across different business scenarios.

| Scenario | Best Threshold |
|---|---:|
| balanced_operations | 0.010 |
| high_fraud_loss | 0.010 |
| high_customer_friction | 0.075 |
| high_review_cost | 0.075 |

This demonstrated an important business insight:

```text
There is no universal best fraud threshold.
```

The right threshold depends on whether the business prioritizes fraud capture, customer experience, review cost, or operational capacity.

---

## 13. Risk-Band Decisioning

Instead of producing only a binary fraud prediction, the project converts calibrated fraud scores into risk actions.

Default risk policy:

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

This creates a more practical fraud operations workflow.

The model score remains technical, while the risk-band policy translates the score into business action.

---

## 14. Batch Inference

The calibrated batch inference pipeline scores raw PaySim transactions and outputs analyst-friendly records.

Production-style output columns:

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
```

The output tells analysts:

```text
which transaction was scored
who/customer was involved
when the transaction happened
how much the transaction was worth
what type of transaction it was
what fraud score the model assigned
whether it crossed the fraud threshold
what action is recommended
```

---

## 15. Production Scoring Mode

The project supports production scoring mode.

In production, true fraud labels are not available at scoring time.

For that reason, production mode omits:

```text
is_fraud
```

Production scoring command:

```bash
python -m fraud_detection_platform.cli.paysim_batch_inference \
  --raw-paysim-data-path data/external/PS_20174392719_1491204439457_log.csv \
  --model-path models/paysim_calibrated_fraud_model.joblib \
  --output-path reports/paysim_calibrated_scored_transactions_production.csv \
  --threshold 0.010 \
  --review-threshold 0.010 \
  --high-risk-threshold 0.075 \
  --priority-threshold 0.100 \
  --production-mode
```

This makes the scored output more realistic for a fraud analyst or risk manager.

---

## 16. Risk Action Summary

The project also produces a management-level action summary.

Observed action distribution:

| Recommended Action | Transaction Count | Percentage of Total | Fraud Rate |
|---|---:|---:|---:|
| approve | 6,248,594 | 98.21% | 0.0545% |
| manual_review | 110,088 | 1.73% | 2.77% |
| high_risk_review | 2,252 | 0.035% | 21.71% |
| priority_investigation | 1,686 | 0.027% | 75.44% |

Fraud concentration increases sharply as action severity increases.

The priority investigation queue is especially strong:

```text
1,686 transactions
1,272 fraud cases
75.44% fraud rate
```

This queue represents only:

```text
0.027% of all transactions
```

but contains a highly concentrated set of fraud cases.

That is a strong operational result.

---

## 17. Business Impact

This project demonstrates how an ML model can support business decisioning.

The system helps the business:

```text
reduce review overload
prioritize high-risk cases
understand cost trade-offs
compare threshold strategies
separate scoring from policy
produce analyst-friendly outputs
generate management-level summaries
```

The most important business result is that the platform creates small, high-value fraud investigation queues instead of only producing abstract model metrics.

---

## 18. Production Thinking

This project includes several production-oriented design choices:

```text
modular package structure
command-line workflows
unit tests
CI quality checks
type checking
data validation
model persistence
batch scoring
production mode without labels
risk-band decisioning
cost-sensitive thresholding
documentation
```

The system separates:

```text
model training
model scoring
threshold selection
business risk policy
analyst output
management reporting
```

This is important because real ML systems require more than a trained model.

They require workflows, controls, outputs, and clear business decision logic.

---

## 19. Current Limitations

Current limitations include:

```text
PaySim is simulated data.
The current train/test split is random rather than time-based.
The model has not yet been deployed behind an API.
No dashboard has been built yet.
No drift monitoring has been implemented yet.
No model explainability layer has been added yet.
No analyst feedback loop exists yet.
No production database integration exists yet.
```

These limitations are documented intentionally to show awareness of what would still be needed in a real production system.

---

## 20. Next Steps

Recommended next improvements:

```text
Add time-based validation.
Add feature importance and explainability.
Add a FastAPI real-time scoring endpoint.
Add dashboard reporting for action distributions.
Add monitoring for score drift and action distribution drift.
Add analyst feedback loop simulation.
Compare Random Forest with gradient boosting models.
Add transaction-amount-based loss modeling.
Add review capacity constraints.
```

The most practical next technical step is time-based validation because fraud patterns and financial behavior change over time.

---

## 21. Summary

This project demonstrates an end-to-end fraud detection ML platform that moves beyond simple classification.

It includes:

```text
PaySim ingestion
feature engineering
calibrated modeling
threshold tuning
cost-sensitive evaluation
scenario comparison
risk-band decisioning
batch scoring
production-style outputs
action summary reporting
documentation
CI quality checks
```

The strongest result is the creation of operational fraud queues.

The priority investigation queue represented only `0.027%` of transactions but had a `75.44%` fraud rate.

This shows how calibrated ML scores can be converted into useful, business-ready fraud actions.
