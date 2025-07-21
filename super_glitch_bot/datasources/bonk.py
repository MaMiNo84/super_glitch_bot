"""BonkBOT program integration using Helius logs.

This source listens for the BonkBot program and detects new token mints.
"""

from __future__ import annotations

import base64
from typing import Any, Awaitable, Callable, Dict, Optional

from .helius import HeliusSource


class BonkSource(HeliusSource):
    """Detect new tokens created via BonkBot."""

    PROGRAM_ID = "LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj"
    INIT_VARIANT = 0

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

        if instruction.get("programId") != self.PROGRAM_ID:
            return None

        data_b64 = instruction.get("data")
        if not data_b64:
            self.logger.debug("Bonk instruction missing data")
            return None

        try:
            raw = base64.b64decode(data_b64)
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.debug("Bonk failed to decode data: %s", exc)
            return None

        if not raw or raw[0] != self.INIT_VARIANT:
            self.logger.debug("Bonk unknown instruction variant")
            return None

        accounts = instruction.get("accounts", [])
        mint = accounts[1] if len(accounts) > 1 else None
        self.logger.debug("Bonk initialize via raw data accounts=%s", accounts)
        return mint
