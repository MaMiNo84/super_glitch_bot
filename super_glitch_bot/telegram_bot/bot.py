"""Telegram bot implementation."""

from typing import Any

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
)

from . import handlers


class TelegramBot:
    """Telegram bot wrapper."""

    def __init__(self, token: str, manager: Any) -> None:
        self.token = token
        self.manager = manager
        self.app: Application | None = None

    def start(self) -> None:
        """Start the Telegram bot."""
        self.app = ApplicationBuilder().token(self.token).build()
        self.app.add_handler(CommandHandler("start", handlers.start))
        self.app.add_handler(CommandHandler("stop", handlers.stop))
        self.app.add_handler(CommandHandler("help", handlers.help_command))
        self.app.add_handler(CommandHandler("start_platform", handlers.start_platform))
        self.app.add_handler(CommandHandler("stop_platform", handlers.stop_platform))
        self.app.add_handler(CommandHandler("set_gem_filter", handlers.set_gem_filter))

        self.app.bot_data["manager"] = self.manager
        self.app.run_polling()

    def send_message(self, chat_id: int, text: str) -> None:
        """Send a plain text message."""
        if not self.app:
            raise RuntimeError("Bot not started")
        self.app.bot.send_message(chat_id=chat_id, text=text)
