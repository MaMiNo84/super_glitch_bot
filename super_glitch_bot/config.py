"""Configuration loading utilities."""

from pathlib import Path
from typing import Any, Dict
import os
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    with path.open("r", encoding="utf-8") as f:
        raw_cfg = yaml.safe_load(f)

    def _resolve(value: Any) -> Any:
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            return os.getenv(value[2:-1], "")
        if isinstance(value, dict):
            return {k: _resolve(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_resolve(v) for v in value]
        return value

    return _resolve(raw_cfg)
