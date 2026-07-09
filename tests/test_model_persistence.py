"""Tests for fraud model persistence utilities."""

from pathlib import Path

import pytest
from sklearn.dummy import DummyClassifier

from fraud_detection_platform.models.persistence import load_model, save_model


def test_save_model_writes_model_artifact(tmp_path: Path) -> None:
    model = DummyClassifier(strategy="most_frequent")
    output_path = tmp_path / "model.joblib"

    saved_path = save_model(model, output_path)

    assert saved_path == output_path
    assert output_path.exists()


def test_load_model_returns_saved_model(tmp_path: Path) -> None:
    model = DummyClassifier(strategy="most_frequent")
    output_path = tmp_path / "model.joblib"

    save_model(model, output_path)
    loaded_model = load_model(output_path)

    assert isinstance(loaded_model, DummyClassifier)
    assert loaded_model.strategy == "most_frequent"


def test_load_model_raises_for_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_model.joblib"

    with pytest.raises(FileNotFoundError, match="Model artifact not found"):
        load_model(missing_path)
