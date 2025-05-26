from dataclasses import dataclass
from typing import List, Dict, Any
from .product import Product
from .service import Service

@dataclass
class Company:
    """Company entity"""
    name: str
    website: str
    products: List[Product]
    services: List[Service]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert company data to dictionary"""
        return {
            'name': self.name,
            'website': self.website,
            'products': [vars(p) for p in self.products],
            'services': [vars(s) for s in self.services]
        }