"""Track token performance after signaling."""

from typing import Any, Dict, List

from .message_templates import MessageTemplates

from ..datasources.dexscreener import DexScreenerSource
from ..telegram_bot.bot import TelegramBot


class PerformanceTracker:
    """Track and report performance of tokens."""

    def __init__(
        self, dexscreener: DexScreenerSource, bot: TelegramBot, chat_id: int
    ) -> None:
        self.dexscreener = dexscreener
        self.bot = bot
        self.chat_id = chat_id
        self.tokens: Dict[str, Dict[str, Any]] = {}
        self.calls = 0
        self.calls_2x = 0

    def track(self, token: Dict[str, Any]) -> None:
        """Start tracking a token's performance."""
        price = token.get("dexscreener_data", {}).get("price", {}).get("usd", 0.0)
        self.tokens[token["address"]] = {
            "token": token,
            "initial_price": price,
            "highest_price": price,
            "hit_2x": False,
        }
        self.calls += 1

    async def update(self) -> None:
        """Send performance updates."""
        for addr, info in self.tokens.items():
            data = self.dexscreener.fetch_token_data(addr)
            price = data.get("price", {}).get("usd", 0.0)
            info["highest_price"] = max(info["highest_price"], price)
            token_name = info["token"].get("name") or addr
            if not info["hit_2x"] and price >= 2 * info["initial_price"]:
                info["hit_2x"] = True
                self.calls_2x += 1
                await self.bot.send_message(
                    self.chat_id,
                    MessageTemplates.PERFORMANCE_UPDATE.format(
                        token_name=token_name,
                        details=f"Hit 2x at ${price}",
                    ),
                )

    def get_stats(self) -> Dict[str, Any]:
        """Return aggregated performance statistics."""
        if self.calls == 0:
            return {"calls": 0, "reached_2x": 0, "average_x": 0.0}
        avg_x = (
            sum(
                info["highest_price"] / info["initial_price"]
                for info in self.tokens.values()
            )
            / self.calls
        )
        return {"calls": self.calls, "reached_2x": self.calls_2x, "average_x": avg_x}
