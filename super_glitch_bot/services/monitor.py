"""Token monitoring services."""

import logging
from typing import Awaitable, Callable

from ..datasources.helius import HeliusSource


class TokenMonitor:
    """Monitor new token creations."""

    def __init__(
        self, source: HeliusSource, callback: Callable[[str], Awaitable[None]]
    ) -> None:
        self.source = source
        self.callback = callback
        self.logger = logging.getLogger(__name__)

    async def run(self) -> None:
        """Run the monitoring loop."""
        self.logger.info("Starting token monitor")
        await self.source.start_listening(self.callback)
