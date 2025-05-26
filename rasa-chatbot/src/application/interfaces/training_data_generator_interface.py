from abc import ABC, abstractmethod
from typing import Dict, Any

class TrainingDataGeneratorInterface(ABC):
    """Interface for generating Rasa training data"""
    
    @abstractmethod
    def generate_nlu_data(self, company_data: Dict[str, Any]) -> str:
        """Generate NLU training data from company data"""
        pass
    
    @abstractmethod
    def generate_domain(self, company_data: Dict[str, Any]) -> str:
        """Generate domain.yml from company data"""
        pass
    
    @abstractmethod
    def generate_stories(self, company_data: Dict[str, Any]) -> str:
        """Generate stories.yml from company data"""
        pass