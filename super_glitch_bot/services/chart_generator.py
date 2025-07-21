"""Generate charts for tokens."""

from __future__ import annotations

import os
from datetime import datetime
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Iterable, List, Optional, Sequence, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image, ImageDraw


class ChartGenerator:
    """Create charts to include in messages."""

    def __init__(self, api_key: str | None = None) -> None:
        self._temp_files: List[str] = []
        self.api_key = api_key

    def generate(
        self,
        token_address: str,
        data: Optional[Sequence[Tuple[datetime, float]]] = None,
        *,
        title: str | None = None,
        logo_url: str | None = None,
    ) -> str:
        """Return path to generated chart image.

        If ``data`` is ``None`` it will be fetched from the Moralis API
        using the configured ``api_key``.
        """

        if data is None:
            data = self._fetch_close_prices(token_address)

        if not data:
            raise ValueError("No data available to generate chart")

        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            fig, ax = plt.subplots(figsize=(8, 4))
            dates, prices = zip(*data)
            ax.plot(dates, prices, color="tab:blue")
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            fig.autofmt_xdate()

            ax.set_title(title or token_address)
            ax.set_xlabel("Time")
            ax.set_ylabel("Price")

            if logo_url:
                try:
                    logo = self._load_circular_logo(logo_url, size=64)
                    fig.figimage(
                        logo,
                        10,
                        fig.bbox.ymax - logo.shape[0] - 10,
                        zorder=10,
                    )
                except Exception:
                    pass

            fig.tight_layout()
            fig.savefig(tmp.name, dpi=150)
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

    def _fetch_close_prices(
        self, token_address: str, limit: int = 50
    ) -> List[Tuple[datetime, float]]:
        """Fetch OHLC data from Moralis and return timestamps and close prices."""
        if not self.api_key:
            return []

        url = f"https://solana-gateway.moralis.io/token/mainnet/pairs/{token_address}/ohlcv"
        params = {
            "timeframe": "5min",
            "currency": "usd",
            "limit": limit,
        }
        headers = {"accept": "application/json", "X-API-Key": self.api_key}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("result", [])
        except Exception:
            return []

        result: List[Tuple[datetime, float]] = []
        for item in data:
            ts = item.get("timestamp")
            close = item.get("close")
            if ts is None or close is None:
                continue
            try:
                dt = datetime.fromisoformat(ts)
            except ValueError:
                continue
            result.append((dt, float(close)))
        result.sort(key=lambda x: x[0])
        return result

    @staticmethod
    def _load_circular_logo(url: str, size: int = 64) -> np.ndarray:
        """Return a circular version of the image at ``url``."""
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)

        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return np.asarray(img)
