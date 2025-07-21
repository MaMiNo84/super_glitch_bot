"""Program-specific Helius data source."""

import json
from typing import Any, Awaitable, Callable, Dict, Optional

import websockets

from .helius import HeliusSource


class ProgramHeliusSource(HeliusSource):
    """Helius source for a specific program."""

    def __init__(
        self,
        rpc_url: str,
        program_id: str,
        parsed_type: Optional[str] = None,
        decoder: Optional[Callable[[str], Optional[str]]] = None,
        on_token: Optional[Callable[[str], Awaitable[None]]] = None,
    ) -> None:
        super().__init__(rpc_url, [program_id], on_token)
        self.program_id = program_id
        self.parsed_type = parsed_type
        self.decoder = decoder

    def parse_instruction(self, instruction: Dict[str, Any]) -> Optional[str]:
        if self.parsed_type:
            parsed = instruction.get("parsed")
            if parsed and parsed.get("type") == self.parsed_type:
                info = parsed.get("info", {})
                mint = info.get("mint") or info.get("tokenMint")
                self.logger.debug(
                    "Parsed %s instruction info=%s", self.parsed_type, info
                )
                return mint
            self.logger.debug("Ignored instruction %s", parsed)
            return None

        if self.decoder:
            data = instruction.get("data")
            try:
                mint = self.decoder(data)
                self.logger.debug("Decoded raw instruction to mint %s", mint)
                return mint
            except Exception as exc:  # pragma: no cover - defensive
                self.logger.exception("Decode failed: %s", exc)
                return None
        return None

    async def _listen(self) -> None:
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {"mentions": [self.program_id]},
                {"commitment": "processed"},
            ],
        }

        async with websockets.connect(self.rpc_url) as ws:
            self.logger.info("Listening to Helius WebSocket %s", self.rpc_url)
            self.logger.debug("Subscribing to program %s", self.program_id)
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
