"""Helius WebSocket RPC source for new token events."""

from typing import Any


class HeliusSource:
    """Monitor new tokens via Helius WebSocket RPC."""

    def __init__(self, rpc_url: str) -> None:
        self.rpc_url = rpc_url

    def start_listening(self) -> None:
        """Begin listening for token creation events."""
        # TODO: implement WebSocket connection and monitoring
        raise NotImplementedError
