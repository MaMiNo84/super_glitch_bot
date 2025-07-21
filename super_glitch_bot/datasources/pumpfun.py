"""Pump.fun program integration using Helius logs."""

from typing import Any, Dict, Optional, Awaitable, Callable

from .helius import HeliusSource


class PumpFunSource(HeliusSource):
    """Detect new tokens created via pump.fun."""

    PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

    def __init__(
        self, rpc_url: str, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        super().__init__(rpc_url, [self.PROGRAM_ID], on_token)

    def parse_instruction(self, instruction: Dict[str, Any]) -> Optional[str]:
        parsed = instruction.get("parsed")
        if parsed and parsed.get("type") == "Create":
            info = parsed.get("info", {})
            mint = info.get("mint") or info.get("tokenMint")
            self.logger.debug("Pump.fun Create instruction info=%s", info)
            return mint
        self.logger.debug("Pump.fun ignored instruction %s", parsed)
        return None
