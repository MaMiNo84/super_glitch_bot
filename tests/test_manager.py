import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import asyncio

from super_glitch_bot.services.manager import ServiceManager


class FakeCollection:
    def __init__(self):
        self.calls = []

    def update_one(self, flt, update, upsert=False):
        self.calls.append((flt, update, upsert))


class FakeDB:
    def __init__(self):
        self.closed = False
        self.collections = {"gem_filter": FakeCollection()}

    def connect(self):
        pass

    def close(self):
        self.closed = True

    def get_collection(self, name):
        return self.collections.setdefault(name, FakeCollection())


class FakeBot:
    def __init__(self):
        self.stopped = False

    async def stop(self):
        self.stopped = True


CONFIG = {
    "mongodb": {"uri": "mongodb://localhost", "name": "test"},
    "telegram": {"token": "t", "admins": [1]},
    "helius": {"ws_url": "ws://"},
}


def create_manager():
    manager = ServiceManager(CONFIG)
    manager.db = FakeDB()
    manager.bot = FakeBot()
    return manager


def test_start_stop_platform():
    manager = create_manager()
    assert len(manager.monitor.sources) == 3

    manager.stop_platform("pumpfun")
    assert all(
        src is not manager.platforms["pumpfun"] for src in manager.monitor.sources
    )

    manager.start_platform("pumpfun")
    assert manager.platforms["pumpfun"] in manager.monitor.sources


def test_set_gem_filter_updates_db_and_assessor():
    manager = create_manager()
    manager.set_gem_filter("min_score", "80")
    assert manager.assessor.min_score == 80
    coll = manager.db.get_collection("gem_filter")
    assert coll.calls[0] == ({"_id": "config"}, {"$set": {"min_score": "80"}}, True)


def test_stop_monitoring_cancels_tasks_and_closes_db():
    async def run():
        manager = create_manager()
        manager.monitor_task = asyncio.create_task(asyncio.sleep(1))
        manager.evaluator_task = asyncio.create_task(asyncio.sleep(1))
        manager.performance_task = asyncio.create_task(asyncio.sleep(1))
        await manager.stop_monitoring()
        assert manager.monitor_task.cancelled()
        assert manager.evaluator_task.cancelled()
        assert manager.performance_task.cancelled()
        assert manager.db.closed is True

    asyncio.run(run())
