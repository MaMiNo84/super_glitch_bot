"""Logging configuration for the application."""

import logging
from logging import Logger


def configure_logging() -> Logger:
    """Configure and return root logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("super_glitch_bot")
