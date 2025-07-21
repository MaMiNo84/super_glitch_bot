"""BonkBOT program integration using Helius logs.

This source listens for the BonkBot program and detects new token mints.
"""

from __future__ import annotations

import base64
from typing import Any, Awaitable, Callable, Dict, Optional

from .helius_program import ProgramHeliusSource


class BonkSource(ProgramHeliusSource):
    """Detect new tokens created via BonkBot."""

    PROGRAM_ID = "LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj"
    INIT_VARIANT = 0

    def __init__(
        self, rpc_url: str, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        def decoder(ix: Dict[str, Any]) -> Optional[str]:
            data_b64 = ix.get("data")
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

            accounts = ix.get("accounts", [])
            mint = accounts[1] if len(accounts) > 1 else None
            self.logger.debug("Bonk initialize via raw data accounts=%s", accounts)
            return mint

        super().__init__(
            rpc_url,
            self.PROGRAM_ID,
            parsed_type="initialize",
            decoder=decoder,
            on_token=on_token,
        )
