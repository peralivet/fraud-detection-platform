"""Evaluation metrics for fraud detection models."""

from dataclasses import dataclass

from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass(frozen=True)
class ClassificationMetrics:
    """Classification metrics for fraud detection."""

    precision: float
    recall: float
    f1: float
    roc_auc: float
    pr_auc: float
    true_negatives: int
    false_positives: int
    false_negatives: int
    true_positives: int


def calculate_classification_metrics(
    y_true: list[int],
    y_pred: list[int],
    y_score: list[float],
) -> ClassificationMetrics:
    """Calculate fraud-focused classification metrics.

    Args:
        y_true: True class labels.
        y_pred: Predicted class labels.
        y_score: Predicted fraud probability scores.

    Returns:
        Classification metrics including precision, recall, F1, ROC-AUC,
        PR-AUC, and confusion matrix values.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    return ClassificationMetrics(
        precision=precision_score(y_true, y_pred, zero_division=0),
        recall=recall_score(y_true, y_pred, zero_division=0),
        f1=f1_score(y_true, y_pred, zero_division=0),
        roc_auc=roc_auc_score(y_true, y_score),
        pr_auc=average_precision_score(y_true, y_score),
        true_negatives=int(tn),
        false_positives=int(fp),
        false_negatives=int(fn),
        true_positives=int(tp),
    )
