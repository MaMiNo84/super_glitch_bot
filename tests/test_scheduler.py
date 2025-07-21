import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import asyncio
from unittest.mock import AsyncMock
from super_glitch_bot.services.performance_tracker import PerformanceTracker


class FakeDex:
    def fetch_token_data(self, address):
        return {"price": {"usd": 1.0}}

    def get_raydium_pair(self, data):
        return None


class FakeBot:
    async def send_message(self, chat_id, text):
        pass


def test_performance_scheduler_triggers_update():
    dex = FakeDex()
    bot = FakeBot()
    tracker = PerformanceTracker(dex, bot, chat_id=1)
    tracker.update = AsyncMock()

    async def run_loop():
        task = asyncio.create_task(tracker.run_scheduler(0.1))
        await asyncio.sleep(0.15)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(run_loop())
    assert tracker.update.await_count >= 1
