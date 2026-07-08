"""Logging utilities for ML platform projects."""

import logging
import logging.config
from pathlib import Path
from typing import Any

import yaml


def setup_logging(config_path: Path | None = None) -> None:
    """Configure application logging from a YAML config file.

    If no config path is provided, the function loads configs/logging.yaml
    from the current working directory.
    """
    resolved_config_path = config_path or Path.cwd() / "configs" / "logging.yaml"

    if not resolved_config_path.exists():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
        return

    with resolved_config_path.open("r", encoding="utf-8") as file:
        config: dict[str, Any] = yaml.safe_load(file) or {}

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the given name."""
    return logging.getLogger(name)
