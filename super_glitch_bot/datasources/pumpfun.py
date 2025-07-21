"""Pump.fun program integration using Helius logs."""

from typing import Awaitable, Callable, Optional

from .helius_program import ProgramHeliusSource


class PumpFunSource(ProgramHeliusSource):
    """Detect new tokens created via pump.fun."""

    PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

    def __init__(
        self, rpc_url: str, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        super().__init__(
            rpc_url,
            self.PROGRAM_ID,
            parsed_type="Create",
            on_token=on_token,
        )
