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

    def decoder(data: str):
        calls.append(data)
        return "mint2"

    source = ProgramHeliusSource("ws://", "pid", decoder=decoder)
    instruction = {"data": "abc"}
    assert source.parse_instruction(instruction) == "mint2"
    assert calls == ["abc"]
