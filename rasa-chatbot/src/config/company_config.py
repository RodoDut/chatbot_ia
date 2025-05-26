# rasa-chatbot/src/config/company_config.py
#Configuración y las acciones de Rasa integradas con la arquitectura CLEAN. 
import os                       # Para manejar variables de entorno
from typing import Dict, Any    # Para anotaciones de tipos
from dataclasses import dataclass
from typing import Dict, Type
from src.infrastructure.scrapers.company_a_scraper import CompanyAScraper
from src.application.interfaces.scraper_interface import ScraperInterface

@dataclass
class CompanyConfig:
    """Configuration for a company"""
    name: str
    website: str
    scraper_class: Type[ScraperInterface]

class CompanyRegistry:
    """Registry of supported companies"""
    
    COMPANIES: Dict[str, CompanyConfig] = {
        'company_a': CompanyConfig(
            name='Company A',
            website='https://www.company-a.com',
            scraper_class=CompanyAScraper
        ),
        # Agregar más compañías aquí
    }
    
    @classmethod
    def get_company_config(cls, company_id: str) -> CompanyConfig:
        """Get configuration for a specific company"""
        if company_id not in cls.COMPANIES:
            raise ValueError(f"Company {company_id} not supported")
        return cls.COMPANIES[company_id]


# rasa-chatbot/src/config/settings.py
import os
from pathlib import Path

class Settings:
    """Configuraciones globales del sistema"""
    
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    
    # Configuración de scraping
    SCRAPING_DELAY = float(os.getenv('SCRAPING_DELAY', '1.0'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    # Configuración de datos
    DATA_EXPIRY_HOURS = int(os.getenv('DATA_EXPIRY_HOURS', '24'))


# rasa-chatbot/actions/actions.py
"""
Acciones personalizadas de Rasa integradas con nuestra arquitectura Clean
"""

import sys
from pathlib import Path
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.infrastructure.data_sources.json_data_source import JSONDataSource
from src.domain.entities.company import CompanyData, CompanyInfo
from src.domain.entities.product import Product
from src.domain.entities.service import Service


class ActionShowProducts(Action):
    """Acción para mostrar productos disponibles"""
    
    def name(self) -> Text:
        return "action_show_products"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Cargar datos de la compañía
            data_source = JSONDataSource(Path(__file__).parent.parent / "data" / "scraped_data")
            company_data_dict = data_source.load_data("company_company_a")  # Usar configuración dinámica
            
            if not company_data_dict:
                dispatcher.utter_message(text="Lo siento, no pude cargar la información de productos.")
                return []
            
            # Reconstruir entidades
            products = [Product(**p) for p in company_data_dict['products']]
            
            if not products:
                dispatcher.utter_message(text="No tenemos productos disponibles en este momento.")
                return []
            
            # Formatear respuesta
            if len(products) <= 3:
                # Mostrar todos si son pocos
                message = "Estos son nuestros productos disponibles:\n\n"
                for product in products:
                    message += f"🔹 **{product.name}**\n"
                    message += f"   {product.description}\n"
                    message += f"   💰 Precio: {product.get_display_price()}\n"
                    message += f"   📦 {'Disponible' if product.is_available() else 'No disponible'}\n\n"
            else:
                # Mostrar resumen si son muchos
                categories = list(set(p.category for p in products))
                message = f"Tenemos {len(products)} productos en {len(categories)} categorías:\n\n"
                
                for category in categories[:5]:  # Mostrar hasta 5 categorías
                    category_products = [p for p in products if p.category == category]
                    message += f"🏷️ **{category}**: {len(category_products)} productos\n"
                
                message += f"\n¿Te interesa alguna categoría en particular?"
            
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            dispatcher.utter_message(text="Disculpa, ocurrió un error al cargar los productos.")
            print(f"Error en ActionShowProducts: {e}")
        
        return []


class ActionShowServices(Action):
    """Acción para mostrar servicios disponibles"""
    
    def name(self) -> Text:
        return "action_show_services"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            data_source = JSONDataSource(Path(__file__).parent.parent / "data" / "scraped_data")
            company_data_dict = data_source.load_data("company_company_a")
            
            if not company_data_dict:
                dispatcher.utter_message(text="Lo siento, no pude cargar la información de servicios.")
                return []
            
            services = [Service(**s) for s in company_data_dict['services']]
            
            if not services:
                dispatcher.utter_message(text="No tenemos servicios disponibles en este momento.")
                return []
            
            message = "Estos son nuestros servicios:\n\n"
            for service in services[:5]:  # Mostrar hasta 5 servicios
                message += f"🔸 **{service.name}**\n"
                message += f"   {service.description}\n"
                message += f"   💰 Precio: {service.get_display_price()}\n"
                if service.duration:
                    message += f"   ⏱️ Duración: {service.duration}\n"
                message += "\n"
            
            if len(services) > 5:
                message += f"Y {len(services) - 5} servicios más disponibles."
            
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            dispatcher.utter_message(text="Disculpa, ocurrió un error al cargar los servicios.")
            print(f"Error en ActionShowServices: {e}")
        
        return []


class ActionShowPrice(Action):
    """Acción para mostrar precio de producto/servicio específico"""
    
    def name(self) -> Text:
        return "action_show_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtener entidades mencionadas
        product_name = tracker.get_slot("product")
        service_name = tracker.get_slot("service")
        
        try:
            data_source = JSONDataSource(Path(__file__).parent.parent / "data" / "scraped_data")
            company_data_dict = data_source.load_data("company_company_a")
            
            if not company_data_dict:
                dispatcher.utter_message(text="Lo siento, no pude cargar la información de precios.")
                return []
            
            products = [Product(**p) for p in company_data_dict['products']]
            services = [Service(**s) for s in company_data_dict['services']]
            
            found_items = []
            
            # Buscar en productos
            if product_name:
                for product in products:
                    if product_name.lower() in product.name.lower():
                        found_items.append(f"🔹 {product.name}: {product.get_display_price()}")
            
            # Buscar en servicios
            if service_name:
                for service in services:
                    if service_name.lower() in service.name.lower():
                        found_items.append(f"🔸 {service.name}: {service.get_display_price()}")
            
            if found_items:
                message = "Aquí tienes los precios:\n\n" + "\n".join(found_items)
            else:
                message = "No encontré información de precio para ese producto o servicio. ¿Podrías ser más específico?"
            
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            dispatcher.utter_message(text="Disculpa, ocurrió un error al buscar el precio.")
            print(f"Error en ActionShowPrice: {e}")
        
        return []