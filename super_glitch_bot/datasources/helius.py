"""Helius WebSocket RPC source for new token events."""

import asyncio
import json
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional

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

    def parse_instruction(self, instruction: Dict[str, Any]) -> Optional[str]:
        """Return mint address if the instruction represents a new token."""
        parsed = instruction.get("parsed")
        if parsed and parsed.get("type") == "initializeMint":
            mint = parsed.get("info", {}).get("mint")
            self.logger.debug("Parsed initializeMint with mint %s", mint)
            return mint
        self.logger.debug("Ignored instruction %s", parsed)
        return None

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
            self.logger.debug("Subscribing with programs: %s", self.program_ids)
            await ws.send(json.dumps(request))
            while True:
                message = await ws.recv()
                data = json.loads(message)
                if data.get("method") != "logsNotification":
                    continue

                instructions = data["params"]["result"]["value"].get("instructions", [])
                for ix in instructions:
                    mint = self.parse_instruction(ix)
                    if mint and self.on_token:
                        self.logger.debug("Detected new token %s", mint)
                        await self.on_token(mint)

    async def start_listening(
        self, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        """Begin listening for token creation events."""
        if on_token is not None:
            self.on_token = on_token
        self.logger.debug("Starting listen loop")
        await self._listen()
