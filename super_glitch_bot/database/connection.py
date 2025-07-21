"""MongoDB connection utilities."""

import logging
from typing import Any, Dict, Optional

from pymongo import MongoClient


class Database:
    """Database connection handler."""

    def __init__(self, uri: str, name: str) -> None:
        self.uri = uri
        self.name = name
        self.client: Optional[MongoClient] = None
        self.db = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> None:
        """Establish the database connection."""
        self.logger.info("Connecting to MongoDB at %s", self.uri)
        self.client = MongoClient(self.uri)
        self.db = self.client[self.name]

    def get_collection(self, name: str) -> Any:
        """Return a collection by name."""
        if self.db is None:
            raise RuntimeError("Database not connected")
        return self.db[name]

    def update_token(self, address: str, updates: Dict[str, Any]) -> None:
        """Update a token document."""
        coll = self.get_collection("tokens")
        self.logger.info("Updating token %s with %s", address, updates)
        coll.update_one({"address": address}, {"$set": updates})

    def deactivate_token(self, address: str) -> None:
        """Mark a token as inactive."""
        self.update_token(address, {"active": False})
