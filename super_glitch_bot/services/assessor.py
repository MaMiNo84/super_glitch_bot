"""Token assessment logic."""

import logging
from typing import Any, Dict


class TokenAssessor:
    """Assess tokens and identify gems."""

    def __init__(self) -> None:
        self.min_score = 60
        self.min_liquidity = 1000.0
        self.logger = logging.getLogger(__name__)

    def assess(self, token: Dict[str, Any]) -> bool:
        """Return True if the token qualifies as a gem."""
        score = token.get("rugcheck_report", {}).get("score", 0)
        liquidity = (
            token.get("dexscreener_data", {}).get("liquidity", {}).get("usd", 0.0)
        )
        result = score >= self.min_score and liquidity >= self.min_liquidity
        self.logger.info(
            "Assessment for %s: score=%s liquidity=%s result=%s",
            token.get("address"),
            score,
            liquidity,
            result,
        )
        return result
