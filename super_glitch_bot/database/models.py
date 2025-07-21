"""Database models using dataclasses."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Token:
    """Internal representation of a token."""

    address: str
    name: Optional[str] = None
    symbol: Optional[str] = None
    decimals: Optional[int] = None
    rugcheck_report: Dict[str, Any] = field(default_factory=dict)
    dexscreener_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    raydium_pair: Optional[str] = None
    active: bool = True
    status_history: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    passed_filter: bool = False
    assessment_history: List[Dict[str, Any]] = field(default_factory=list)
    last_assessed: Optional[datetime] = None
    death_reason: Optional[str] = None


# Additional models can be added here
