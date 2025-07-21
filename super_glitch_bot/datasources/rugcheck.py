"""Rugcheck.xyz API integration."""

import logging
from typing import Any, Dict

import requests


class RugCheckSource:
    """Fetch token data from rugcheck.xyz."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def fetch_token_data(self, token_address: str) -> Dict[str, Any]:
        """Retrieve token details from the API."""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        url = f"https://api.rugcheck.xyz/tokens/solana/{token_address}/report"
        self.logger.debug("Fetching rugcheck data from %s", url)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
