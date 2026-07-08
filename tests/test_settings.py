from pathlib import Path

from fraud_detection_platform.config.settings import deep_merge, load_settings


def test_deep_merge_overrides_nested_values() -> None:
    base = {
        "runtime": {
            "environment": "base",
            "log_level": "INFO",
        },
        "api": {
            "host": "0.0.0.0",
            "port": 8000,
        },
    }

    override = {
        "runtime": {
            "environment": "development",
            "log_level": "DEBUG",
        },
        "api": {
            "host": "127.0.0.1",
        },
    }

    merged = deep_merge(base, override)

    assert merged["runtime"]["environment"] == "development"
    assert merged["runtime"]["log_level"] == "DEBUG"
    assert merged["api"]["host"] == "127.0.0.1"
    assert merged["api"]["port"] == 8000


def test_load_development_settings() -> None:
    settings = load_settings("development", config_dir=Path("configs"))

    assert settings.app.name == "fraud-detection-platform"
    assert settings.runtime.environment == "development"
    assert settings.runtime.log_level == "DEBUG"
    assert settings.api.host == "127.0.0.1"
    assert settings.api.port == 8000


def test_load_production_settings() -> None:
    settings = load_settings("production", config_dir=Path("configs"))

    assert settings.app.name == "fraud-detection-platform"
    assert settings.runtime.environment == "production"
    assert settings.runtime.log_level == "WARNING"
    assert settings.api.host == "0.0.0.0"
    assert settings.api.port == 8080
