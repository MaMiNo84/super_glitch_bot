"""Dexscreener API integration."""

from typing import Any, Dict, Optional

import requests


class DexScreenerSource:
    """Fetch market data from dexscreener."""

    def __init__(self, chain_id: str) -> None:
        self.chain_id = chain_id

    def fetch_token_data(self, token_address: str) -> Dict[str, Any]:
        """Retrieve token details from the API."""
        url = f"https://api.dexscreener.com/tokens/v1/{self.chain_id}/{token_address}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_raydium_pair(self, data: Dict[str, Any]) -> Optional[str]:
        """Return the Raydium pair address if present."""
        pairs = data.get("pairs", [])
        for pair in pairs:
            if pair.get("dex") == "Raydium" and pair.get("pairAddress"):
                return pair["pairAddress"]
        return None
