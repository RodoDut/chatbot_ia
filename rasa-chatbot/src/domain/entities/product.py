from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    """Product entity"""
    id: str
    name: str
    description: str
    price: float
    category: str
    stock: Optional[int] = None