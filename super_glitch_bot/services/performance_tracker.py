"""Track token performance after signaling."""

from typing import Any, Dict


class PerformanceTracker:
    """Track and report performance of tokens."""

    def __init__(self) -> None:
        # TODO: initialize tracking state
        pass

    def track(self, token: Dict[str, Any]) -> None:
        """Start tracking a token's performance."""
        # TODO: implement tracking
        raise NotImplementedError

    def update(self) -> None:
        """Send performance updates."""
        # TODO: implement update sending
        raise NotImplementedError
