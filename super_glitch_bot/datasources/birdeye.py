"""Birdeye API integration."""

from typing import Any, Dict


class BirdEyeSource:
    """Fetch market data from Birdeye."""

    def fetch_token_data(self, token_address: str) -> Dict[str, Any]:
        """Retrieve token details from the API."""
        # TODO: implement API call
        raise NotImplementedError
