"""Helius WebSocket RPC source for new token events."""

import asyncio
import json
import logging
from typing import Any, Awaitable, Callable, List, Optional

import websockets


class HeliusSource:
    """Monitor new tokens via Helius WebSocket RPC."""

    def __init__(
        self,
        rpc_url: str,
        program_ids: Optional[List[str]] = None,
        on_token: Optional[Callable[[str], Awaitable[None]]] = None,
    ) -> None:
        self.rpc_url = rpc_url
        self.program_ids = program_ids or []
        self.on_token = on_token
        self.logger = logging.getLogger(__name__)

    async def _listen(self) -> None:
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {"mentions": self.program_ids},
                {"commitment": "finalized", "encoding": "jsonParsed"},
            ],
        }

        async with websockets.connect(self.rpc_url) as ws:
            self.logger.info("Listening to Helius WebSocket %s", self.rpc_url)
            await ws.send(json.dumps(request))
            while True:
                message = await ws.recv()
                data = json.loads(message)
                if data.get("method") != "logsNotification":
                    continue

                instructions = data["params"]["result"]["value"].get("instructions", [])
                for ix in instructions:
                    parsed = ix.get("parsed")
                    if parsed and parsed.get("type") == "initializeMint":
                        mint = parsed.get("info", {}).get("mint")
                        if mint and self.on_token:
                            await self.on_token(mint)

    async def start_listening(
        self, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        """Begin listening for token creation events."""
        if on_token is not None:
            self.on_token = on_token
        await self._listen()
