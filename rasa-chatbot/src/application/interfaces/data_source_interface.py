from abc import ABC, abstractmethod
from typing import Dict, List, Any

class DataSourceInterface(ABC):
    """Interface for data sources"""
    
    @abstractmethod
    def save_data(self, data: Dict[str, Any]) -> None:
        """Save data to the data source"""
        pass
    
    @abstractmethod
    def load_data(self) -> Dict[str, Any]:
        """Load data from the data source"""
        pass
    
    @abstractmethod
    def update_data(self, data: Dict[str, Any]) -> None:
        """Update existing data in the data source"""
        pass