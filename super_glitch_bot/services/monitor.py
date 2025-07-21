"""Token monitoring services."""

from ..datasources.helius import HeliusSource


class TokenMonitor:
    """Monitor new token creations."""

    def __init__(self, source: HeliusSource) -> None:
        self.source = source

    def run(self) -> None:
        """Run the monitoring loop."""
        self.source.start_listening()
