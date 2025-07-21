"""Central service manager."""

import asyncio
import logging
from typing import Any, Dict

from ..database.connection import Database
from ..datasources.dexscreener import DexScreenerSource
from ..datasources.helius import HeliusSource
from ..datasources.pumpfun import PumpFunSource
from ..datasources.bonk import BonkSource
from ..datasources.rugcheck import RugCheckSource
from ..telegram_bot.bot import TelegramBot
from .monitor import TokenMonitor
from .assessor import TokenAssessor
from .performance_tracker import PerformanceTracker
from .evaluator import TokenEvaluator
from ..database.models import Token
from .message_templates import MessageTemplates


class ServiceManager:
    """Control flow for the monitoring service."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.db = Database(config["mongodb"]["uri"], config["mongodb"]["name"])
        self.dexscreener = DexScreenerSource("solana")
        self.rugcheck = RugCheckSource(config.get("rugcheck_api_key", ""))
        self.assessor = TokenAssessor()
        self.bot = TelegramBot(config["telegram"]["token"], self)
        chat_id = config["telegram"]["admins"][0]
        self.tracker = PerformanceTracker(self.dexscreener, self.bot, chat_id, self.db)
        self.evaluator = TokenEvaluator(
            self.db,
            self.rugcheck,
            self.dexscreener,
            self.assessor,
            self.tracker,
            self.bot,
            chat_id,
            config.get("assessment_interval", 120),
        )
        ws_url = config["helius"]["ws_url"]
        helius = HeliusSource(
            ws_url,
            ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"],
            self.handle_new_token,
        )
        pump = PumpFunSource(ws_url, self.handle_new_token)
        bonk = BonkSource(ws_url, self.handle_new_token)
        self.monitor = TokenMonitor([helius, pump, bonk], self.handle_new_token)
        self.monitor_task = None
        self.evaluator_task = None
        self.performance_task = None

    async def start(self) -> None:
        """Start monitoring and bot services."""

        self.db.connect()
        self.logger.info("Service started")
        self.logger.debug(
            "Monitoring platforms: %s",
            [s.__class__.__name__ for s in self.monitor.sources],
        )
        self.monitor_task = asyncio.create_task(self.monitor.run())
        self.evaluator_task = asyncio.create_task(self.evaluator.run())
        self.performance_task = asyncio.create_task(
            self.tracker.run_scheduler(self.config.get("performance_interval", 120))
        )
        await self.bot.run()

    async def handle_new_token(self, address: str) -> None:
        """Process a newly created token."""
        self.logger.info("Processing new token %s", address)
        self.logger.debug("Fetching rugcheck data")
        rug_data = self.rugcheck.fetch_token_data(address)
        self.logger.debug("Fetching dexscreener data")
        dex_data = self.dexscreener.fetch_token_data(address)
        pair = self.dexscreener.get_raydium_pair(dex_data)
        token = Token(
            address=address,
            name=rug_data.get("name") or dex_data.get("name"),
            symbol=rug_data.get("symbol") or dex_data.get("symbol"),
            decimals=rug_data.get("decimals") or dex_data.get("decimals"),
            rugcheck_report=rug_data,
            dexscreener_data=dex_data,
            raydium_pair=pair,
        )
        coll = self.db.get_collection("tokens")
        self.logger.debug("Inserting token document into DB")
        passed = self.assessor.assess(token.__dict__)
        assessment_entry = {
            "timestamp": token.created_at,
            "score": rug_data.get("score", 0),
            "liquidity": dex_data.get("liquidity", {}).get("usd", 0.0),
            "passed": passed,
        }
        if passed:
            token.passed_filter = True
        token.assessment_history.append(assessment_entry)
        token.last_assessed = token.created_at
        coll.insert_one(token.__dict__)

        if passed:
            chat_id = self.config["telegram"]["admins"][0]
            await self.bot.send_message(
                chat_id,
                MessageTemplates.NEW_GEM.format(token_name=token.name or token.address),
            )
            self.logger.debug("Starting performance tracking for %s", address)
            self.tracker.track(token.__dict__)
        else:
            self.logger.info("Token %s did not pass assessment", address)

    async def stop_monitoring(self) -> None:
        """Stop all running tasks and close resources."""
        tasks = [self.monitor_task, self.evaluator_task, self.performance_task]
        self.logger.info("Stopping service tasks")
        for task in tasks:
            if task:
                task.cancel()
        await asyncio.gather(*(t for t in tasks if t), return_exceptions=True)

        await self.bot.stop()
        self.db.close()
        self.logger.info("Service stopped")

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
