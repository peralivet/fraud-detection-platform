"""Tests for calibrated fraud risk-band decision policy."""

import pytest

from fraud_detection_platform.risk.calibrated_decision_policy import (
    CalibratedRiskDecisionPolicy,
    recommend_calibrated_action,
)


def test_calibrated_policy_recommends_approve_below_review_threshold() -> None:
    assert recommend_calibrated_action(0.005) == "approve"


def test_calibrated_policy_recommends_manual_review_at_review_threshold() -> None:
    assert recommend_calibrated_action(0.010) == "manual_review"


def test_calibrated_policy_recommends_manual_review_between_review_and_high_risk() -> None:
    assert recommend_calibrated_action(0.050) == "manual_review"


def test_calibrated_policy_recommends_high_risk_review_at_high_risk_threshold() -> None:
    assert recommend_calibrated_action(0.075) == "high_risk_review"


def test_calibrated_policy_recommends_high_risk_review_between_high_risk_and_priority() -> None:
    assert recommend_calibrated_action(0.090) == "high_risk_review"


def test_calibrated_policy_recommends_priority_investigation_at_priority_threshold() -> None:
    assert recommend_calibrated_action(0.100) == "priority_investigation"


def test_calibrated_policy_recommends_priority_investigation_above_priority_threshold() -> None:
    assert recommend_calibrated_action(0.200) == "priority_investigation"


def test_calibrated_policy_accepts_custom_thresholds() -> None:
    policy = CalibratedRiskDecisionPolicy(
        review_threshold=0.020,
        high_risk_threshold=0.050,
        priority_threshold=0.080,
    )

    assert recommend_calibrated_action(0.010, policy) == "approve"
    assert recommend_calibrated_action(0.020, policy) == "manual_review"
    assert recommend_calibrated_action(0.050, policy) == "high_risk_review"
    assert recommend_calibrated_action(0.080, policy) == "priority_investigation"


def test_calibrated_policy_rejects_invalid_review_threshold() -> None:
    with pytest.raises(ValueError, match="review_threshold must be between 0.0 and 1.0"):
        CalibratedRiskDecisionPolicy(review_threshold=-0.1)


def test_calibrated_policy_rejects_invalid_high_risk_threshold() -> None:
    with pytest.raises(ValueError, match="high_risk_threshold must be between 0.0 and 1.0"):
        CalibratedRiskDecisionPolicy(high_risk_threshold=1.1)


def test_calibrated_policy_rejects_invalid_priority_threshold() -> None:
    with pytest.raises(ValueError, match="priority_threshold must be between 0.0 and 1.0"):
        CalibratedRiskDecisionPolicy(priority_threshold=1.1)


def test_calibrated_policy_rejects_review_threshold_greater_than_high_risk_threshold() -> None:
    with pytest.raises(
        ValueError,
        match="review_threshold must be less than high_risk_threshold",
    ):
        CalibratedRiskDecisionPolicy(
            review_threshold=0.080,
            high_risk_threshold=0.075,
            priority_threshold=0.100,
        )


def test_calibrated_policy_rejects_review_threshold_equal_to_high_risk_threshold() -> None:
    with pytest.raises(
        ValueError,
        match="review_threshold must be less than high_risk_threshold",
    ):
        CalibratedRiskDecisionPolicy(
            review_threshold=0.075,
            high_risk_threshold=0.075,
            priority_threshold=0.100,
        )


def test_calibrated_policy_rejects_high_risk_threshold_greater_than_priority_threshold() -> None:
    with pytest.raises(
        ValueError,
        match="high_risk_threshold must be less than priority_threshold",
    ):
        CalibratedRiskDecisionPolicy(
            review_threshold=0.010,
            high_risk_threshold=0.120,
            priority_threshold=0.100,
        )


def test_calibrated_policy_rejects_high_risk_threshold_equal_to_priority_threshold() -> None:
    with pytest.raises(
        ValueError,
        match="high_risk_threshold must be less than priority_threshold",
    ):
        CalibratedRiskDecisionPolicy(
            review_threshold=0.010,
            high_risk_threshold=0.100,
            priority_threshold=0.100,
        )


def test_recommend_calibrated_action_rejects_negative_score() -> None:
    with pytest.raises(ValueError, match="fraud_score must be between 0.0 and 1.0"):
        recommend_calibrated_action(-0.1)


def test_recommend_calibrated_action_rejects_score_above_one() -> None:
    with pytest.raises(ValueError, match="fraud_score must be between 0.0 and 1.0"):
        recommend_calibrated_action(1.1)
