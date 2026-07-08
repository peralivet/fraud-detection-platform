"""Application configuration loading and validation."""

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field

Environment = Literal["development", "production"]


class AppConfig(BaseModel):
    """Application metadata."""

    name: str
    version: str


class RuntimeConfig(BaseModel):
    """Runtime configuration."""

    environment: str
    log_level: str = Field(default="INFO")


class PathConfig(BaseModel):
    """Project path configuration."""

    data_dir: str
    model_dir: str
    reports_dir: str


class APIConfig(BaseModel):
    """API configuration."""

    host: str
    port: int


class Settings(BaseModel):
    """Validated application settings."""

    app: AppConfig
    runtime: RuntimeConfig
    paths: PathConfig
    api: APIConfig


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge override values into base values.

    Values in override take precedence over values in base.
    """
    merged = base.copy()

    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value

    return merged


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file into a dictionary."""
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        msg = f"Configuration file must contain a YAML mapping: {path}"
        raise ValueError(msg)

    return data


def load_settings(
    environment: Environment = "development",
    config_dir: Path | None = None,
) -> Settings:
    """Load and validate application settings for a given environment."""
    resolved_config_dir = config_dir or Path.cwd() / "configs"

    base_config = load_yaml(resolved_config_dir / "base.yaml")
    environment_config = load_yaml(resolved_config_dir / f"{environment}.yaml")

    merged_config = deep_merge(base_config, environment_config)

    return Settings.model_validate(merged_config)
