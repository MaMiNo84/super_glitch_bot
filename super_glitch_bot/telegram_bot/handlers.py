"""Telegram command handlers."""

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler."""
    # TODO: implement start command
    raise NotImplementedError


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop command handler."""
    # TODO: implement stop command
    raise NotImplementedError
