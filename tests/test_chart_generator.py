import pathlib
import sys
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from datetime import datetime, timedelta

from super_glitch_bot.services.chart_generator import ChartGenerator


def test_generate_creates_image_and_cleans_up():
    gen = ChartGenerator()
    now = datetime.utcnow()
    data = [(now + timedelta(minutes=i), float(i)) for i in range(4)]
    path = gen.generate("token", data)
    assert os.path.exists(path)
    gen.cleanup()
    assert not os.path.exists(path)
