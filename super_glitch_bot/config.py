"""Configuration loading utilities."""

from pathlib import Path
from typing import Any, Dict
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    # TODO: implement configuration loading
    raise NotImplementedError
