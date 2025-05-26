import os
from typing import Dict, Any
from src.infrastructure.rasa_integration.nlu_generator import generate_nlu_yaml
from src.infrastructure.rasa_integration.domain_generator import generate_domain_yaml
from src.infrastructure.rasa_integration.stories_generator import generate_stories_yaml
from src.application.interfaces.data_source_interface import DataSourceInterface

class ChatbotOrchestrator:
    """Orchestrator for chatbot training data generation"""
    
    def __init__(self, data_source: DataSourceInterface):
        self.data_source = data_source
    
    def generate_training_files(self, output_dir: str) -> None:
        """Generate all necessary training files for Rasa"""
        company_data = self.data_source.load_data()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate and save NLU data
        nlu_content = generate_nlu_yaml(company_data)
        with open(os.path.join(output_dir, 'nlu.yml'), 'w', encoding='utf-8') as f:
            f.write(nlu_content)
        
        # Generate and save domain
        domain_content = generate_domain_yaml(company_data)
        with open(os.path.join(output_dir, 'domain.yml'), 'w', encoding='utf-8') as f:
            f.write(domain_content)
        
        # Generate and save stories
        stories_content = generate_stories_yaml(company_data)
        with open(os.path.join(output_dir, 'stories.yml'), 'w', encoding='utf-8') as f:
            f.write(stories_content)
        
        print(f"Training files generated in {output_dir}")