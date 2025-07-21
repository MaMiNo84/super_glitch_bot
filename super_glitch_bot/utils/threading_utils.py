"""Threading utilities."""

from threading import Thread
from typing import Callable


def run_in_thread(target: Callable, *args, **kwargs) -> Thread:
    """Run a target function in a daemon thread."""
    thread = Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread
