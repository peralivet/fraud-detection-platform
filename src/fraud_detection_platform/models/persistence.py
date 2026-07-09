"""Model persistence utilities for fraud detection models."""

from pathlib import Path
from typing import Any

import joblib


def save_model(model: Any, output_path: str | Path) -> Path:
    """Save a trained model artifact to disk.

    Args:
        model: Trained model object to save.
        output_path: Destination path for the model artifact.

    Returns:
        Path to the saved model artifact.
    """
    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, resolved_output_path)

    return resolved_output_path


def load_model(model_path: str | Path) -> Any:
    """Load a trained model artifact from disk.

    Args:
        model_path: Path to the saved model artifact.

    Returns:
        Loaded model object.

    Raises:
        FileNotFoundError: If the model artifact does not exist.
    """
    resolved_model_path = Path(model_path)

    if not resolved_model_path.exists():
        msg = f"Model artifact not found: {resolved_model_path}"
        raise FileNotFoundError(msg)

    return joblib.load(resolved_model_path)
