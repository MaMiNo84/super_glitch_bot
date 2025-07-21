"""Dexscreener API integration."""

from typing import Any, Dict, Optional

import logging
import requests


class DexScreenerSource:
    """Fetch market data from dexscreener."""

    def __init__(self, chain_id: str) -> None:
        self.chain_id = chain_id
        self.logger = logging.getLogger(__name__)

    def fetch_token_data(self, token_address: str) -> Dict[str, Any]:
        """Retrieve token details from the API."""
        url = f"https://api.dexscreener.com/tokens/v1/{self.chain_id}/{token_address}"
        self.logger.debug("Fetching dexscreener data from %s", url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_raydium_pair(self, data: Dict[str, Any]) -> Optional[str]:
        """Return the Raydium pair address if present."""
        pairs = data.get("pairs", [])
        for pair in pairs:
            if pair.get("dex") == "Raydium" and pair.get("pairAddress"):
                self.logger.debug("Found Raydium pair %s", pair["pairAddress"])
                return pair["pairAddress"]
        return None
