import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from super_glitch_bot.datasources.helius_program import ProgramHeliusSource


def test_parse_with_parsed_type():
    source = ProgramHeliusSource("ws://", "pid", parsed_type="Create")
    instruction = {"parsed": {"type": "Create", "info": {"mint": "mint1"}}}
    assert source.parse_instruction(instruction) == "mint1"


def test_parse_with_decoder():
    calls = []

    def decoder(ix: dict):
        calls.append(ix)
        return "mint2"

    source = ProgramHeliusSource("ws://", "pid", decoder=decoder)
    instruction = {"data": "abc"}
    assert source.parse_instruction(instruction) == "mint2"
    assert calls == [instruction]


def test_parse_with_fallback_to_decoder():
    calls = []

    def decoder(ix: dict):
        calls.append(ix)
        return "mint3"

    source = ProgramHeliusSource(
        "ws://",
        "pid",
        parsed_type="Create",
        decoder=decoder,
    )
    instruction = {"data": "def"}
    assert source.parse_instruction(instruction) == "mint3"
    assert calls == [instruction]
