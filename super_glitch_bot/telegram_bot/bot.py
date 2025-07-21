"""Telegram bot implementation."""

import logging
from typing import Any, Optional

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
        self.app: Optional[Application] = None
        self.logger = logging.getLogger(__name__)

    async def run(self) -> None:
        """Start the Telegram bot and run until stopped."""
        self.app = ApplicationBuilder().token(self.token).build()
        self.logger.debug("Telegram bot application built")
        self.app.add_handler(CommandHandler("start", handlers.start))
        self.app.add_handler(CommandHandler("stop", handlers.stop))
        self.app.add_handler(CommandHandler("help", handlers.help_command))
        self.app.add_handler(CommandHandler("start_platform", handlers.start_platform))
        self.app.add_handler(CommandHandler("stop_platform", handlers.stop_platform))
        self.app.add_handler(CommandHandler("set_gem_filter", handlers.set_gem_filter))

        self.app.bot_data["manager"] = self.manager

        await self.app.initialize()
        self.logger.debug("Telegram bot initialized")
        self.logger.info("Telegram bot starting")
        await self.app.start()
        self.logger.debug("Telegram bot started")
        await self.app.updater.start_polling()
        await self.app.updater.idle()

    async def send_message(self, chat_id: int, text: str) -> None:
        """Send a plain text message."""
        if not self.app:
            raise RuntimeError("Bot not started")
        self.logger.info("Sending message to %s: %s", chat_id, text)
        self.logger.debug("Message length %d", len(text))
        await self.app.bot.send_message(chat_id=chat_id, text=text)
