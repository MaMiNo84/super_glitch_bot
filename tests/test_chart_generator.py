import pathlib
import sys
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from super_glitch_bot.services.chart_generator import ChartGenerator


def test_generate_creates_image_and_cleans_up(monkeypatch):
    gen = ChartGenerator(api_key="k")

    def fake_fetch(_addr):
        return [1, 2, 3, 4]

    monkeypatch.setattr(gen, "_fetch_ohlc", fake_fetch)

    path = gen.generate("token")
    assert os.path.exists(path)
    gen.cleanup()
    assert not os.path.exists(path)
