from abc import ABC, abstractmethod
from typing import Dict, List, Any

class ScraperInterface(ABC):
    """Interface for web scrapers"""
    
    @abstractmethod
    def scrape_products(self) -> List[Dict[str, Any]]:
        """Scrape products data from the website"""
        pass
    
    @abstractmethod
    def scrape_services(self) -> List[Dict[str, Any]]:
        """Scrape services data from the website"""
        pass