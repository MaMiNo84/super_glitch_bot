"""MongoDB connection utilities."""

from pymongo import MongoClient
from typing import Any


class Database:
    """Database connection handler."""

    def __init__(self, uri: str, name: str) -> None:
        self.uri = uri
        self.name = name
        self.client: MongoClient | None = None
        self.db = None

    def connect(self) -> None:
        """Establish the database connection."""
        self.client = MongoClient(self.uri)
        self.db = self.client[self.name]

    def get_collection(self, name: str) -> Any:
        """Return a collection by name."""
        if self.db is None:
            raise RuntimeError("Database not connected")
        return self.db[name]
