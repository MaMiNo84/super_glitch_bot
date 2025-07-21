"""Queue utilities."""

from queue import Queue


def create_queue() -> Queue:
    """Create a queue for cross-thread communication."""
    return Queue()
