"""BonkBOT program integration using Helius logs."""

from typing import Any, Dict, Optional, Awaitable, Callable

from .helius import HeliusSource


class BonkSource(HeliusSource):
    """Detect new tokens created via bonk."""

    PROGRAM_ID = "LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj"

    def __init__(
        self, rpc_url: str, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        super().__init__(rpc_url, [self.PROGRAM_ID], on_token)

    def parse_instruction(self, instruction: Dict[str, Any]) -> Optional[str]:
        parsed = instruction.get("parsed")
        if parsed and parsed.get("type") == "initialize":
            info = parsed.get("info", {})
            mint = info.get("mint") or info.get("tokenMint")
            self.logger.debug("Bonk initialize instruction info=%s", info)
            return mint
        self.logger.debug("Bonk ignored instruction %s", parsed)
        return None
