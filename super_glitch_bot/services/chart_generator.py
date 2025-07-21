"""Generate charts for tokens."""

from __future__ import annotations

import os
from tempfile import NamedTemporaryFile
from typing import List

import matplotlib.pyplot as plt


class ChartGenerator:
    """Create charts to include in messages."""

    def __init__(self) -> None:
        self._temp_files: List[str] = []

    def generate(self, token_address: str, data: List[float]) -> str:
        """Return path to generated chart image."""
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            fig, ax = plt.subplots()
            ax.plot(data)
            ax.set_title(token_address)
            ax.set_xlabel("index")
            ax.set_ylabel("value")
            fig.tight_layout()
            fig.savefig(tmp.name)
            plt.close(fig)
            self._temp_files.append(tmp.name)
            return tmp.name

    def cleanup(self) -> None:
        """Remove generated temporary files."""
        for path in self._temp_files:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
        self._temp_files = []

    def __del__(self) -> None:  # pragma: no cover - cleanup on GC
        self.cleanup()
