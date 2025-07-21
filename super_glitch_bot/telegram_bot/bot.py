"""Telegram bot implementation."""

from typing import Any
from telegram.ext import Application, CommandHandler


class TelegramBot:
    """Telegram bot wrapper."""

    def __init__(self, token: str) -> None:
        self.token = token
        self.app: Application | None = None

    def start(self) -> None:
        """Start the Telegram bot."""
        # TODO: setup handlers and start polling
        raise NotImplementedError
