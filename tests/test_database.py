import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from super_glitch_bot.database.connection import Database


class FakeCollection:
    def __init__(self):
        self.updates = []

    def update_one(self, flt, update):
        self.updates.append((flt, update))


class FakeDB(Database):
    def __init__(self):
        super().__init__("mongodb://localhost", "test")
        self.collection = FakeCollection()
        self.db = {"tokens": self.collection}

    def connect(self):
        pass

    def get_collection(self, name):
        return self.collection


def test_deactivate_token_reason():
    db = FakeDB()
    db.deactivate_token("abc", "rugpull")
    assert db.collection.updates[0] == (
        {"address": "abc"},
        {"$set": {"active": False, "death_reason": "rugpull"}},
    )
