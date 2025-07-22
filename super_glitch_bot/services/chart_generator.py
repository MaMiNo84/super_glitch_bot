"""Generate charts for tokens."""

from __future__ import annotations

import os
from tempfile import NamedTemporaryFile
from typing import List, Optional, Sequence

import io
import requests
from PIL import Image, ImageDraw
from ..config import load_config

import matplotlib.pyplot as plt


class ChartGenerator:
    """Create charts to include in messages."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self._temp_files: List[str] = []
        cfg = load_config()
        self.api_key = api_key or cfg.get("moralis_api_key", "")

    def _fetch_ohlc(self, token_address: str) -> Sequence[float]:
        url = (
            "https://solana-gateway.moralis.io/token/mainnet/pairs/"
            f"{token_address}/ohlcv"
        )
        params = {"timeframe": "1min", "limit": 20, "currency": "usd"}
        headers = {"accept": "application/json", "X-API-Key": self.api_key}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        result = data.get("result", [])
        closes = [item.get("close", 0.0) for item in result]
        return closes

    def _circular_logo(self, url: str, size: int = 48) -> Image.Image:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return img

    def generate(self, token_address: str, logo_url: Optional[str] = None) -> str:
        """Return path to generated chart image."""
        closes = self._fetch_ohlc(token_address)
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            fig, ax = plt.subplots()
            ax.plot(closes, color="tab:blue")
            ax.set_title(f"{token_address} Market Cap")
            ax.set_xlabel("index")
            ax.set_ylabel("USD")
            fig.tight_layout()
            if logo_url:
                try:
                    img = self._circular_logo(logo_url)
                    fig.figimage(img, 10, fig.bbox.ymax - img.size[1] - 10)
                except (requests.RequestException, PIL.UnidentifiedImageError):
                    pass
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
