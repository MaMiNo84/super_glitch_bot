import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from super_glitch_bot.datasources.bonk import BonkSource


def test_parse_bonk_parsed_instruction():
    source = BonkSource("ws")
    instruction = {
        "parsed": {"type": "initialize", "info": {"mint": "mint123"}},
    }
    assert source.parse_instruction(instruction) == "mint123"


def test_parse_bonk_raw_instruction():
    source = BonkSource("ws")
    raw = bytes([BonkSource.INIT_VARIANT]) + b"\0" * 32
    instruction = {
        "programId": BonkSource.PROGRAM_ID,
        "data": base64.b64encode(raw).decode(),
        "accounts": ["creator", "mintABC"],
    }
    assert source.parse_instruction(instruction) == "mintABC"


def test_bonk_ignores_other_program():
    source = BonkSource("ws")
    instruction = {
        "programId": "other",
        "parsed": {"type": "initialize", "info": {"mint": "mint123"}},
    }
    assert source.parse_instruction(instruction) is None
