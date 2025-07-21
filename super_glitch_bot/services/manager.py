"""Central service manager."""

from typing import Any, Dict

from ..database.connection import Database
from ..datasources.helius import HeliusSource
from ..telegram_bot.bot import TelegramBot
from ..utils.threading_utils import run_in_thread
from .monitor import TokenMonitor


class ServiceManager:
    """Control flow for the monitoring service."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.db = Database(config["mongodb"]["uri"], config["mongodb"]["name"])
        helius = HeliusSource(config["helius"]["ws_url"])
        self.monitor = TokenMonitor(helius)
        self.bot = TelegramBot(config["telegram"]["token"], self)
        self.monitor_thread = None

    def start(self) -> None:
        """Start monitoring and bot services."""
        self.db.connect()
        self.monitor_thread = run_in_thread(self.monitor.run)
        self.bot.start()

    def stop_monitoring(self) -> None:
        """Placeholder to stop monitoring loop."""
        # Monitor stopping logic would go here
        pass

    def start_platform(self, name: str) -> None:
        """Enable a monitoring platform."""
        # Implementation depends on platform specifics
        pass

    def stop_platform(self, name: str) -> None:
        """Disable a monitoring platform."""
        # Implementation depends on platform specifics
        pass

    def set_gem_filter(self, key: str, value: Any) -> None:
        """Set a gem filter option."""
        # Persist filter to DB or config in a real implementation
        pass
