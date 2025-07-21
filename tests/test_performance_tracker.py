import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from unittest.mock import AsyncMock
from super_glitch_bot.services.performance_tracker import PerformanceTracker


class FakeDex:
    def __init__(self, response):
        self.response = response
        self.calls = 0

    def fetch_token_data(self, address):
        self.calls += 1
        return self.response

    def get_raydium_pair(self, data):
        return data.get("raydium_pair")


class FakeBot:
    async def send_message(self, chat_id, text):
        pass


class FakeDB:
    def __init__(self):
        self.updates = []

    def update_token(self, address, updates):
        self.updates.append((address, updates))

    def get_collection(self, name):
        class Coll:
            def update_one(self, *args, **kwargs):
                pass

        return Coll()


def test_pair_update_and_tracking():
    dex_data = {"price": {"usd": 1.0}, "raydium_pair": "pair123"}
    dex = FakeDex(dex_data)
    bot = FakeBot()
    db = FakeDB()
    tracker = PerformanceTracker(dex, bot, chat_id=1, database=db)
    token = {"address": "token1", "dexscreener_data": dex_data}
    tracker.track(token)
    assert "token1" in tracker.tokens

    import asyncio

    asyncio.run(tracker.update())
    assert db.updates[0] == ("token1", {"raydium_pair": "pair123"})
