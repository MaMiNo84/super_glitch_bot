"""Token monitoring services."""

import asyncio
import logging
from typing import Awaitable, Callable, Iterable

from ..datasources.helius import HeliusSource


class TokenMonitor:
    """Monitor new token creations."""

    def __init__(
        self,
        sources: Iterable[HeliusSource],
        callback: Callable[[str], Awaitable[None]],
    ) -> None:
        self.sources = list(sources)
        self.callback = callback
        self.logger = logging.getLogger(__name__)

    async def run(self) -> None:
        """Run the monitoring loop."""
        self.logger.info("Starting token monitor for %d sources", len(self.sources))
        self.logger.debug("Sources: %s", [s.__class__.__name__ for s in self.sources])
        await asyncio.gather(
            *(source.start_listening(self.callback) for source in self.sources)
        )
