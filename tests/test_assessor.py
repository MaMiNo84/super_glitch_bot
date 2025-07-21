import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from super_glitch_bot.services.assessor import TokenAssessor


def test_assessor_passes():
    assessor = TokenAssessor()
    token = {
        "address": "abc",
        "rugcheck_report": {"score": 70},
        "dexscreener_data": {"liquidity": {"usd": 2000}},
    }
    assert assessor.assess(token) is True


def test_assessor_fails_low_score():
    assessor = TokenAssessor()
    token = {
        "address": "abc",
        "rugcheck_report": {"score": 50},
        "dexscreener_data": {"liquidity": {"usd": 2000}},
    }
    assert assessor.assess(token) is False
