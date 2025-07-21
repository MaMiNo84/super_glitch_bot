"""BonkBOT program integration using Helius logs."""

from typing import Awaitable, Callable, Optional

from .helius_program import ProgramHeliusSource


class BonkSource(ProgramHeliusSource):
    """Detect new tokens created via bonk."""

    PROGRAM_ID = "LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj"

    def __init__(
        self, rpc_url: str, on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> None:
        super().__init__(
            rpc_url, self.PROGRAM_ID, parsed_type="initialize", on_token=on_token
        )
