from dataclasses import dataclass
from typing import Optional

@dataclass
class Service:
    """Service entity"""
    id: str
    name: str
    description: str
    price: float
    duration: Optional[str] = None