"""Token monitoring services."""

from typing import Callable

from ..datasources.helius import HeliusSource


class TokenMonitor:
    """Monitor new token creations."""

    def __init__(self, source: HeliusSource, callback: Callable[[str], None]) -> None:
        self.source = source
        self.callback = callback

    def run(self) -> None:
        """Run the monitoring loop."""
        self.source.start_listening(self.callback)
