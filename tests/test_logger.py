import logging
from pathlib import Path

from fraud_detection_platform.logging import get_logger, setup_logging


def test_get_logger_returns_logger() -> None:
    logger = get_logger("fraud_detection_platform.test")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "fraud_detection_platform.test"


def test_setup_logging_with_config_file() -> None:
    setup_logging(Path("configs/logging.yaml"))

    logger = get_logger("fraud_detection_platform.test")

    assert isinstance(logger, logging.Logger)
