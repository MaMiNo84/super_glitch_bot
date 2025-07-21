"""MongoDB connection utilities."""

from pymongo import MongoClient
from typing import Any


class Database:
    """Database connection handler."""

    def __init__(self, uri: str, name: str) -> None:
        self.uri = uri
        self.name = name
        self.client: MongoClient | None = None

    def connect(self) -> None:
        """Establish the database connection."""
        # TODO: implement connection logic
        raise NotImplementedError

    def get_collection(self, name: str) -> Any:
        """Return a collection by name."""
        # TODO: implement retrieval
        raise NotImplementedError
