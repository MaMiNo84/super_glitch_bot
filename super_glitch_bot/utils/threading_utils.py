"""Threading utilities."""

from threading import Thread
from typing import Callable


def run_in_thread(target: Callable, *args, **kwargs) -> Thread:
    """Run a target function in a daemon thread."""
    # TODO: implement thread helper
    raise NotImplementedError
