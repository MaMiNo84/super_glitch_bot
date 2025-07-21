"""Base classes for data sources."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class DataSource(ABC):
    """Abstract data source interface."""

    @abstractmethod
    def fetch_token_data(self, token_address: str) -> Dict[str, Any]:
        """Fetch data for a given token."""
        raise NotImplementedError
