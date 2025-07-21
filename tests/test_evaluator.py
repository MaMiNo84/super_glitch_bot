import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import asyncio
from super_glitch_bot.services.evaluator import TokenEvaluator
from super_glitch_bot.services.assessor import TokenAssessor
from super_glitch_bot.services.performance_tracker import PerformanceTracker


class FakeDex:
    def __init__(self, response):
        self.response = response

    def fetch_token_data(self, address):
        return self.response

    def get_raydium_pair(self, data):
        return data.get("raydium_pair")


class FakeRug:
    def __init__(self, response):
        self.response = response

    def fetch_token_data(self, address):
        return self.response


class FakeBot:
    async def send_message(self, chat_id, text):
        pass


class FakeCollection:
    def __init__(self, docs):
        self.docs = docs
        self.updates = []

    def find(self, query):
        return [d for d in self.docs if all(d.get(k) == v for k, v in query.items())]

    def update_one(self, flt, update):
        for doc in self.docs:
            if doc["address"] == flt["address"]:
                if "$set" in update:
                    doc.update(update["$set"])
                if "$push" in update:
                    if "status_history" in update["$push"]:
                        doc.setdefault("status_history", []).append(
                            update["$push"]["status_history"]
                        )
                    if "assessment_history" in update["$push"]:
                        doc.setdefault("assessment_history", []).append(
                            update["$push"]["assessment_history"]
                        )
        self.updates.append((flt, update))


class FakeDB:
    def __init__(self, docs):
        self.collection = FakeCollection(docs)

    def get_collection(self, name):
        assert name == "tokens"
        return self.collection

    def update_token(self, address, updates):
        self.collection.update_one({"address": address}, {"$set": updates})


def test_evaluator_updates_token():
    docs = [
        {
            "address": "t1",
            "active": True,
            "passed_filter": False,
            "rugcheck_report": {"score": 50},
            "dexscreener_data": {"liquidity": {"usd": 500}},
        }
    ]
    db = FakeDB(docs)
    rug = FakeRug({"score": 70})
    dex = FakeDex({"liquidity": {"usd": 2000}, "price": {"usd": 1.0}})
    bot = FakeBot()
    assessor = TokenAssessor()
    tracker = PerformanceTracker(dex, bot, chat_id=1, database=db)
    evaluator = TokenEvaluator(
        db, rug, dex, assessor, tracker, bot, chat_id=1, interval=0
    )
    asyncio.run(evaluator.evaluate_once())
    assert docs[0]["passed_filter"] is True
    assert "passed_filter" in docs[0].get("status_history", [])
    hist = docs[0].get("assessment_history", [])
    assert hist and hist[-1]["passed"] is True
    assert docs[0].get("last_assessed") is not None
    assert docs[0]["rugcheck_report"] == {"score": 70}
    assert docs[0]["dexscreener_data"]["liquidity"]["usd"] == 2000
