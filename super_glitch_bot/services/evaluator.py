"""Periodic token re-evaluation service."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from ..database.connection import Database
from ..datasources.dexscreener import DexScreenerSource
from ..datasources.rugcheck import RugCheckSource
from .assessor import TokenAssessor
from .performance_tracker import PerformanceTracker
from .message_templates import MessageTemplates
from ..telegram_bot.bot import TelegramBot


class TokenEvaluator:
    """Reassess stored tokens and announce new gems."""

    def __init__(
        self,
        db: Database,
        rugcheck: RugCheckSource,
        dexscreener: DexScreenerSource,
        assessor: TokenAssessor,
        tracker: PerformanceTracker,
        bot: TelegramBot,
        chat_id: int,
        interval: int = 120,
    ) -> None:
        self.db = db
        self.rugcheck = rugcheck
        self.dexscreener = dexscreener
        self.assessor = assessor
        self.tracker = tracker
        self.bot = bot
        self.chat_id = chat_id
        self.interval = interval
        self.logger = logging.getLogger(__name__)

    async def run(self) -> None:
        """Continuously reassess inactive tokens."""
        while True:
            await self.evaluate_once()
            await asyncio.sleep(self.interval)

    async def evaluate_once(self) -> None:
        """Process tokens one time."""
        coll = self.db.get_collection("tokens")
        tokens = list(coll.find({"active": True, "passed_filter": False}))
        self.logger.debug("Evaluating %d tokens", len(tokens))
        for doc in tokens:
            address = doc.get("address")
            if not address:
                continue
            self.logger.debug("Refreshing data for %s", address)
            rug_data = self.rugcheck.fetch_token_data(address)
            dex_data = self.dexscreener.fetch_token_data(address)
            updates = {
                "rugcheck_report": rug_data,
                "dexscreener_data": dex_data,
                "updated_at": datetime.utcnow(),
            }
            self.db.update_token(address, updates)
            doc.update(updates)

            score = rug_data.get("score", 0)
            liquidity = dex_data.get("liquidity", {}).get("usd", 0.0)
            passed = self.assessor.assess(doc)
            coll.update_one(
                {"address": address},
                {
                    "$push": {
                        "assessment_history": {
                            "timestamp": datetime.utcnow(),
                            "score": score,
                            "liquidity": liquidity,
                            "passed": passed,
                        }
                    },
                    "$set": {"last_assessed": datetime.utcnow()},
                },
            )
            if passed:
                self.db.update_token(address, {"passed_filter": True})
                coll.update_one(
                    {"address": address},
                    {"$push": {"status_history": "passed_filter"}},
                )
                await self.bot.send_message(
                    self.chat_id,
                    MessageTemplates.NEW_GEM.format(
                        token_name=doc.get("name") or address
                    ),
                )
                self.tracker.track(doc)
