"""Tests for fraud risk decision policy."""

import pytest

from fraud_detection_platform.risk.decision_policy import (
    RiskDecisionPolicy,
    recommend_action,
)


def test_recommend_action_approves_low_risk_score() -> None:
    action = recommend_action(0.20)

    assert action == "approve"


def test_recommend_action_recommends_manual_review_for_medium_risk_score() -> None:
    action = recommend_action(0.65)

    assert action == "manual_review"


def test_recommend_action_blocks_high_risk_score() -> None:
    action = recommend_action(0.90)

    assert action == "block"


def test_recommend_action_uses_custom_policy() -> None:
    policy = RiskDecisionPolicy(review_threshold=0.30, block_threshold=0.60)

    assert recommend_action(0.25, policy) == "approve"
    assert recommend_action(0.40, policy) == "manual_review"
    assert recommend_action(0.75, policy) == "block"


def test_recommend_action_validates_score_range() -> None:
    with pytest.raises(ValueError, match="fraud_score must be between 0.0 and 1.0"):
        recommend_action(1.20)


def test_policy_validates_threshold_ranges() -> None:
    with pytest.raises(ValueError, match="review_threshold must be between 0.0 and 1.0"):
        RiskDecisionPolicy(review_threshold=-0.1)


def test_policy_requires_review_threshold_below_block_threshold() -> None:
    with pytest.raises(ValueError, match="review_threshold must be less than block_threshold"):
        RiskDecisionPolicy(review_threshold=0.8, block_threshold=0.5)
