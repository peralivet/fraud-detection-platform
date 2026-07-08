# Fraud Detection Problem Framing

## Overview

This project builds a production-style machine learning platform for detecting potentially fraudulent financial transactions.

The system is designed to score transactions and estimate the likelihood that a transaction is fraudulent. The output can support downstream actions such as allowing the transaction, flagging it for review, requiring additional verification, or blocking it.

## Business Problem

Financial platforms process large volumes of transactions. Most transactions are legitimate, while a small percentage may be fraudulent.

Fraud creates direct financial losses, operational investigation costs, customer trust issues, and regulatory risk. However, incorrectly flagging legitimate customers can also harm customer experience and reduce transaction completion rates.

The business challenge is to detect fraud early while minimizing unnecessary disruption for legitimate users.

## Primary Users

The system may support the following users:

- fraud operations analysts
- risk management teams
- customer support teams
- product managers
- compliance teams
- engineering and platform teams

## Decision Supported

For each transaction, the system should help answer:

```text
Is this transaction likely to be fraudulent?
```

The system may produce:

- fraud probability score
- risk category
- recommended action
- model explanation or top contributing factors
- monitoring metadata for auditability

## Example Decision Policy

A model score alone should not be the full business decision. A production system usually combines the score with policy rules.

Example:

| Fraud Score Range | Risk Level | Possible Action |
|---|---|---|
| 0.00 - 0.30 | Low | Allow transaction |
| 0.30 - 0.70 | Medium | Step-up verification or manual review |
| 0.70 - 1.00 | High | Block or hold transaction for investigation |

The exact thresholds should be tuned based on business cost, fraud rate, customer impact, and operational capacity.

## Success Metrics

The project should be evaluated using both machine learning metrics and business metrics.

### Machine Learning Metrics

Useful ML metrics include:

- precision
- recall
- F1 score
- ROC-AUC
- PR-AUC
- confusion matrix
- false positive rate
- false negative rate

Because fraud is usually rare, PR-AUC, recall, precision, and false positive rate are especially important.

### Business Metrics

Useful business metrics include:

- fraud loss prevented
- false positive investigation cost
- customer friction rate
- manual review volume
- approval rate
- chargeback reduction
- average model scoring latency

## Key Trade-offs

Fraud detection systems involve important trade-offs.

### Recall vs Precision

Higher recall catches more fraud but may increase false positives.

Higher precision reduces false alerts but may miss more fraud.

### Fraud Prevention vs Customer Experience

Aggressive fraud blocking may reduce fraud losses but can frustrate legitimate customers.

### Automation vs Human Review

Fully automated decisions are faster, but manual review may be needed for medium-risk cases.

### Model Complexity vs Explainability

Complex models may improve performance, but simpler models are often easier to explain, debug, and govern.

### Real-Time Latency vs Feature Richness

Real-time scoring requires low latency. Some useful features may be expensive to compute in real time.

## Constraints

A practical fraud detection platform should consider:

- class imbalance
- delayed fraud labels
- data drift
- changing fraud patterns
- explainability requirements
- model monitoring
- auditability
- low-latency inference
- secure handling of transaction data

## Initial Scope

The first version of this project will focus on:

- supervised fraud classification
- clean project structure
- dataset loading
- feature validation
- baseline model training
- model evaluation
- batch scoring
- experiment tracking
- documentation of decisions and trade-offs

Later versions can add:

- FastAPI real-time scoring
- streaming transaction simulation
- Databricks workflows
- AWS deployment
- dashboard reporting
- model monitoring
- drift detection
- explainability reports

## Principle

The goal is not only to build a fraud classifier.

The goal is to design a fraud detection platform that can be tested, monitored, explained, and evolved like a real production ML system.
