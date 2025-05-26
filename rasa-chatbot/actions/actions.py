from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import json
from src.infrastructure.data_sources.json_data_source import JsonDataSource

class ActionProductInfo(Action):
    def name(self) -> Text:
        return "action_product_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener el producto mencionado
        product_name = next(tracker.get_latest_entity_values("product"), None)
        
        if not product_name:
            dispatcher.utter_message(text="I'm not sure which product you're asking about. Could you please specify?")
            return []
            
        # Cargar datos de la compañía
        data_source = JsonDataSource('data/company_a_data.json')  # Ajustar según la compañía actual
        company_data = data_source.load_data()
        
        # Buscar el producto
        product = next((p for p in company_data.get('products', []) if p['name'].lower() == product_name.lower()), None)
        
        if product:
            response = f"Here's what I know about {product['name']}:\n"
            response += f"Description: {product['description']}\n"
            response += f"Price: ${product['price']:.2f}"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I'm sorry, I couldn't find information about {product_name}")
        
        return []

class ActionServiceInfo(Action):
    def name(self) -> Text:
        return "action_service_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener el servicio mencionado
        service_name = next(tracker.get_latest_entity_values("service"), None)
        
        if not service_name:
            dispatcher.utter_message(text="I'm not sure which service you're asking about. Could you please specify?")
            return []
            
        # Cargar datos de la compañía
        data_source = JsonDataSource('data/company_a_data.json')  # Ajustar según la compañía actual
        company_data = data_source.load_data()
        
        # Buscar el servicio
        service = next((s for s in company_data.get('services', []) if s['name'].lower() == service_name.lower()), None)
        
        if service:
            response = f"Here's what I know about our {service['name']} service:\n"
            response += f"Description: {service['description']}\n"
            response += f"Price: ${service['price']:.2f}"
            if service.get('duration'):
                response += f"\nDuration: {service['duration']}"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I'm sorry, I couldn't find information about {service_name}")
        
        return []