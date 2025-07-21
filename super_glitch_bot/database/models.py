"""Database models using dataclasses."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class Token:
    """Internal representation of a token."""

    address: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    market_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


# Additional models can be added here
