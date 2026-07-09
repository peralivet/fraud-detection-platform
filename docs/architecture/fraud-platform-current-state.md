# Fraud Detection Platform: Current System State

## 1. Purpose

The fraud detection platform is a production-style machine learning system for identifying potentially fraudulent transactions.

At the current stage, the platform supports a full local machine learning workflow:

```text
generate sample transaction data
        ↓
train a baseline fraud model
        ↓
evaluate classification performance
        ↓
save the trained model artifact
        ↓
load the model for batch inference
        ↓
score transactions
        ↓
recommend business actions
```

The goal is not only to build a model, but to build the foundation of an ML product that can eventually support APIs, monitoring, cloud deployment, and real-time scoring.

---

## 2. Main Components

### 2.1 Data Layer

Location:

```text
src/fraud_detection_platform/data/
```

Responsibilities:

- Define the expected transaction schema.
- Load transaction CSV files.
- Validate required columns.
- Split input data into model features and target labels.
- Generate synthetic sample transaction data for local development.

Important files:

```text
schema.py
loader.py
sample_generator.py
```

The current required transaction columns are:

```text
transaction_id
customer_id
transaction_amount
transaction_time
merchant_category
payment_channel
is_fraud
```

---

### 2.2 Feature Engineering Layer

Location:

```text
src/fraud_detection_platform/features/
```

Responsibilities:

- Convert raw transaction data into model-ready features.
- Extract time-based features from `transaction_time`.
- Create amount-based features from `transaction_amount`.

Current engineered features include:

```text
transaction_hour
transaction_day_of_week
transaction_amount_log
```

This layer is important because the same feature transformations must be used during both training and inference.

---

### 2.3 Model Layer

Location:

```text
src/fraud_detection_platform/models/
```

Responsibilities:

- Build the baseline fraud detection model.
- Train the model.
- Save and load model artifacts.

The current baseline model uses a scikit-learn pipeline with:

```text
ColumnTransformer
OneHotEncoder
RandomForestClassifier
```

The model handles both categorical and numeric features.

Categorical features:

```text
customer_id
merchant_category
payment_channel
```

Numeric features:

```text
transaction_amount
transaction_hour
transaction_day_of_week
transaction_amount_log
```

The trained model is saved as a `.joblib` artifact.

---

### 2.4 Evaluation Layer

Location:

```text
src/fraud_detection_platform/evaluation/
```

Responsibilities:

- Calculate fraud-focused model metrics.
- Return structured classification results.

Current metrics include:

```text
precision
recall
f1
roc_auc
pr_auc
true_negatives
false_positives
false_negatives
true_positives
```

Accuracy is intentionally not the main metric because fraud detection is usually an imbalanced classification problem.

---

### 2.5 Training Pipeline

Location:

```text
src/fraud_detection_platform/pipelines/training.py
```

Responsibilities:

- Load transaction data.
- Build feature table.
- Split data into train and test sets.
- Train the baseline model.
- Generate fraud scores.
- Convert scores into fraud predictions.
- Calculate evaluation metrics.
- Optionally save the trained model artifact.

The training pipeline is available from the command line:

```bash
python -m fraud_detection_platform.cli.train \
  --data-path data/raw/sample_transactions.csv \
  --model-output-path models/baseline_fraud_model.joblib
```

---

### 2.6 Batch Inference Pipeline

Location:

```text
src/fraud_detection_platform/pipelines/batch_inference.py
```

Responsibilities:

- Load new transaction data.
- Apply the same feature engineering used during training.
- Load the saved model artifact.
- Generate fraud scores.
- Convert fraud scores into binary predictions.
- Apply the business risk decision policy.
- Write prediction results to CSV.

The batch inference pipeline is available from the command line:

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/sample_transactions.csv \
  --model-path models/baseline_fraud_model.joblib \
  --output-path data/processed/fraud_predictions.csv
```

The output prediction file contains:

```text
transaction_id
fraud_score
fraud_prediction
recommended_action
is_fraud
```

---

### 2.7 Risk Decision Policy Layer

Location:

```text
src/fraud_detection_platform/risk/decision_policy.py
```

Responsibilities:

- Convert fraud scores into business-facing actions.
- Keep operational decision logic separate from the model.

Current policy:

```text
fraud_score < review_threshold       → approve
fraud_score >= review_threshold      → manual_review
fraud_score >= block_threshold       → block
```

Default thresholds:

```text
review_threshold = 0.5
block_threshold = 0.8
```

The batch inference CLI allows these thresholds to be configured:

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/sample_transactions.csv \
  --model-path models/baseline_fraud_model.joblib \
  --output-path data/processed/fraud_predictions.csv \
  --threshold 0.5 \
  --review-threshold 0.4 \
  --block-threshold 0.85
```

---

## 3. Data Flow

The current end-to-end data flow is:

```text
Synthetic transaction data
        ↓
CSV file in data/raw/
        ↓
Data loader
        ↓
Feature engineering
        ↓
Training pipeline
        ↓
Baseline model
        ↓
Evaluation metrics
        ↓
Saved model artifact
        ↓
Batch inference pipeline
        ↓
Fraud scores and recommended actions
        ↓
Prediction CSV in data/processed/
```

---

## 4. Fraud Score vs Fraud Prediction vs Recommended Action

The platform separates three related but different concepts.

### 4.1 fraud_score

`fraud_score` is the model's probability-like estimate of fraud risk.

Example:

```text
fraud_score = 0.82
```

This means the model believes the transaction is high risk.

---

### 4.2 fraud_prediction

`fraud_prediction` is the binary model classification.

Example:

```text
fraud_prediction = 1
```

This is created by applying a classification threshold to the fraud score.

Example:

```text
fraud_score >= 0.5 → fraud_prediction = 1
fraud_score < 0.5  → fraud_prediction = 0
```

---

### 4.3 recommended_action

`recommended_action` is the business decision generated by the risk policy.

Possible values:

```text
approve
manual_review
block
```

This is the most business-facing output because it tells a fraud analyst or transaction system what to do next.

This separation is important because the model can stay the same while business risk thresholds change.

---

## 5. Why the Decision Policy Matters

A fraud model should not directly control business operations.

The model answers:

```text
How risky is this transaction?
```

The decision policy answers:

```text
What should the business do about it?
```

This distinction is important because different organizations may have different risk appetites.

For example:

```text
Conservative fraud team:
  review at 0.30
  block at 0.70

Customer-friendly business:
  review at 0.60
  block at 0.90

High-value transaction workflow:
  review at 0.20
  block at 0.60
```

The same model can support different operational policies by changing thresholds rather than retraining the model.

This moves the project from a simple machine learning model toward a machine learning product.

---

## 6. Current Limitations

The current platform is still an early production-style skeleton. Important limitations include:

1. The data is synthetic and intentionally simple.
2. The model currently produces perfect scores on sample data because the fraud patterns are obvious.
3. The training split is random rather than time-based.
4. The batch inference pipeline currently expects `is_fraud` to exist in the input data.
5. There is no model registry yet.
6. There is no API endpoint yet.
7. There is no monitoring or drift detection yet.
8. There is no cloud deployment yet.
9. There is no real transaction dataset yet.
10. There is no explainability layer yet.

These limitations are acceptable at this stage because the current focus is building the platform foundation.

---

## 7. Next Planned Improvements

The next improvements should move the project closer to a production ML platform.

Recommended next steps:

1. Support unlabeled inference data where `is_fraud` is not required.
2. Add a FastAPI prediction service for real-time scoring.
3. Add request and response schemas for API validation.
4. Add model metadata such as model version, training date, and metrics.
5. Add MLflow experiment tracking.
6. Add model explainability using feature importance or SHAP.
7. Replace synthetic data with a more realistic fraud dataset.
8. Add monitoring for prediction distributions and data drift.
9. Containerize the API and batch inference workflows.
10. Prepare cloud deployment using AWS and Databricks.

---

## 8. Engineering Summary

The platform has moved beyond a notebook-style model into a modular ML system.

Current strengths:

- Clear package structure.
- Separate data, feature, model, evaluation, pipeline, CLI, and risk layers.
- Automated tests.
- Type checking with MyPy.
- Linting and formatting with Ruff.
- Pre-commit quality gates.
- Reusable training pipeline.
- Reusable batch inference pipeline.
- Saved model artifacts.
- Business-facing decision policy.

This structure makes the project easier to test, extend, deploy, and explain in interviews.

---

## 9. Current Local Commands

Generate sample data:

```bash
python -m fraud_detection_platform.cli.generate_sample_data \
  --output-path data/raw/sample_transactions.csv \
  --row-count 100
```

Train and save the model:

```bash
python -m fraud_detection_platform.cli.train \
  --data-path data/raw/sample_transactions.csv \
  --model-output-path models/baseline_fraud_model.joblib
```

Run batch inference:

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/sample_transactions.csv \
  --model-path models/baseline_fraud_model.joblib \
  --output-path data/processed/fraud_predictions.csv
```

Run batch inference with custom business thresholds:

```bash
python -m fraud_detection_platform.cli.batch_inference \
  --data-path data/raw/sample_transactions.csv \
  --model-path models/baseline_fraud_model.joblib \
  --output-path data/processed/fraud_predictions.csv \
  --threshold 0.5 \
  --review-threshold 0.4 \
  --block-threshold 0.85
```

Run quality checks:

```bash
make quality
pre-commit run --all-files
```

---

## 10. Portfolio Talking Point

This project demonstrates more than model training.

It shows the design of an end-to-end ML system with:

- data validation
- feature engineering
- model training
- evaluation
- model persistence
- batch inference
- business decision policy
- command-line workflows
- testing and quality gates

The most important architectural decision so far is the separation between:

```text
model score
model prediction
business action
```

This is a production-oriented design because it allows the model and business policy to evolve independently.
