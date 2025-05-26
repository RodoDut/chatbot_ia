# rasa-chatbot/main.py
"""
Punto de entrada principal del sistema de chatbot
Integra la arquitectura Clean con Rasa existente
"""

import os                   # Asegúrate de que el entorno virtual esté activado
import sys                  # Para modificar el path de importación
from pathlib import Path    # Para manejar rutas de archivos

# Agregar src al path para imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.config.company_config import CompanyRegistry
from src.infrastructure.data_sources.json_data_source import JsonDataSource


class ChatbotManager:
    """Manager class for chatbot setup and training"""
    
    def __init__(self, company_id: str):
        self.company_config = CompanyRegistry.get_company_config(company_id)
        self.data_source = JsonDataSource(
            os.path.join('data', f'{company_id}_data.json')
        )
    
    def update_company_data(self) -> None:
        """Update company data from website"""
        scraper = self.company_config.scraper_class(self.company_config.website)
        
        company_data = {
            'products': scraper.scrape_products(),
            'services': scraper.scrape_services(),
            'name': self.company_config.name,
            'website': self.company_config.website
        }
        
        self.data_source.save_data(company_data)
        print(f"Updated data for {self.company_config.name}")


def main():
    """Main entry point"""
    # Ejemplo de uso
    company_id = 'company_a'  # Este ID debe coincidir con los registrados en CompanyRegistry
    
    try:
        # Inicializar el manager
        manager = ChatbotManager(company_id)
        
        # Actualizar datos de la compañía
        manager.update_company_data()
        print("Data update completed successfully")
        
        # Generar archivos de entrenamiento
        from src.domain.services.chatbot_orchestrator import ChatbotOrchestrator
        orchestrator = ChatbotOrchestrator(manager.data_source)
        orchestrator.generate_training_files('data')
        print("Training files generated successfully")
        
        # Aquí podrías agregar el comando para entrenar el modelo
        print("To train the model, run: rasa train")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()