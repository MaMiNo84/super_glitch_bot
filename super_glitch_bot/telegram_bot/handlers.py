"""Telegram command handlers."""

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler."""
    await update.message.reply_text("Monitoring service is running.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop command handler."""
    manager = context.bot_data.get("manager")
    if manager:
        manager.stop_monitoring()
    await update.message.reply_text("Monitoring stopped.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display help information."""
    commands = [
        "/start - Start the bot",
        "/stop - Stop monitoring",
        "/start_platform <name> - Enable a platform",
        "/stop_platform <name> - Disable a platform",
        "/set_gem_filter <key> <value> - Set gem filter",
    ]
    await update.message.reply_text("Available commands:\n" + "\n".join(commands))


async def start_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enable monitoring for a platform."""
    manager = context.bot_data.get("manager")
    if manager and context.args:
        manager.start_platform(context.args[0])
        await update.message.reply_text(f"Platform {context.args[0]} started.")
    else:
        await update.message.reply_text("Usage: /start_platform <name>")


async def stop_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Disable monitoring for a platform."""
    manager = context.bot_data.get("manager")
    if manager and context.args:
        manager.stop_platform(context.args[0])
        await update.message.reply_text(f"Platform {context.args[0]} stopped.")
    else:
        await update.message.reply_text("Usage: /stop_platform <name>")


async def set_gem_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set gem filter values."""
    manager = context.bot_data.get("manager")
    if manager and len(context.args) == 2:
        manager.set_gem_filter(context.args[0], context.args[1])
        await update.message.reply_text("Gem filter updated.")
    else:
        await update.message.reply_text("Usage: /set_gem_filter <key> <value>")
