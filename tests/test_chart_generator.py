import pathlib
import sys
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from super_glitch_bot.services.chart_generator import ChartGenerator


def test_generate_creates_image_and_cleans_up():
    gen = ChartGenerator()
    path = gen.generate("token", [1, 2, 3, 4])
    assert os.path.exists(path)
    gen.cleanup()
    assert not os.path.exists(path)
