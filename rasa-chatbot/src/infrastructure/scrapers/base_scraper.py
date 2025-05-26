# Clase base para los scrapers
from abc import ABC
from src.application.interfaces.scraper_interface import ScraperInterface
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any

class BaseScraper(ScraperInterface, ABC):
    """Base scraper implementation"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _get_soup(self, url: str) -> BeautifulSoup:
        """Get BeautifulSoup object from URL"""
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    
    def _clean_price(self, price_str: str) -> float:
        """Clean price string and convert to float"""
        return float(''.join(filter(str.isdigit, price_str))) / 100