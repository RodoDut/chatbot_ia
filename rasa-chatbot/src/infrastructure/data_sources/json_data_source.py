# rasa-chatbot/src/infrastructure/data_sources/json_data_source.py
#             print("¡Listo para interactuar con los clientes!")
#         else:
#             print("\n❌ Error configurando el chatbot.")
#     except Exception as e:
import json
import os
from pathlib import Path
from typing import Dict, Any
from src.application.interfaces.data_source_interface import DataSourceInterface

class JsonDataSource(DataSourceInterface):
    """Implementación de almacenamiento en archivos JSON"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Asegura que el archivo JSON exista"""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self.save_data({})
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Guarda datos en archivo JSON"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def load_data(self) -> Dict[str, Any]:
        """Carga datos desde archivo JSON"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_data(self, data: Dict[str, Any]) -> None:
        """Actualiza datos existentes en el archivo JSON"""
        current_data = self.load_data()
        current_data.update(data)
        self.save_data(current_data)


# rasa-chatbot/src/infrastructure/rasa_integration/rasa_training_generator.py
import yaml
from typing import Dict, Any, List
from pathlib import Path
from src.domain.entities.company import CompanyData
from src.application.interfaces.training_data_generator_interface import ITrainingDataGenerator

class RasaTrainingGenerator(ITrainingDataGenerator):
    """Generador completo de archivos de entrenamiento para Rasa"""
    
    def generate_nlu_data(self, company_data: CompanyData) -> Dict[str, Any]:
        """Genera datos NLU completos"""
        
        nlu_data = {
            'version': '3.1',
            'nlu': [
                {
                    'intent': 'greet',
                    'examples': self._get_greet_examples()
                },
                {
                    'intent': 'goodbye',
                    'examples': self._get_goodbye_examples()
                },
                {
                    'intent': 'ask_products',
                    'examples': self._generate_product_examples(company_data.products)
                },
                {
                    'intent': 'ask_services',
                    'examples': self._generate_service_examples(company_data.services)
                },
                {
                    'intent': 'ask_price',
                    'examples': self._generate_price_examples(company_data)
                },
                {
                    'intent': 'ask_company_info',
                    'examples': self._generate_company_info_examples(company_data.company_info)
                },
                {
                    'intent': 'affirm',
                    'examples': '- sí\n- si\n- está bien\n- perfecto\n- de acuerdo\n- correcto\n- exacto'
                },
                {
                    'intent': 'deny',
                    'examples': '- no\n- no gracias\n- no es correcto\n- no está bien\n- negativo'
                }
            ]
        }
        
        return nlu_data
    
    def generate_domain_data(self, company_data: CompanyData) -> Dict[str, Any]:
        """Genera domain.yml completo"""
        
        # Extraer nombres para entidades
        product_names = [p.name.lower() for p in company_data.products]
        service_names = [s.name.lower() for s in company_data.services]
        categories = company_data.get_all_categories()
        
        domain_data = {
            'version': '3.1',
            'intents': [
                'greet',
                'goodbye', 
                'ask_products',
                'ask_services',
                'ask_price',
                'ask_company_info',
                'affirm',
                'deny'
            ],
            'entities': [
                'product',
                'service', 
                'category'
            ],
            'slots': {
                'product': {
                    'type': 'text',
                    'influence_conversation': True,
                    'mappings': [
                        {
                            'type': 'from_entity',
                            'entity': 'product'
                        }
                    ]
                },
                'service': {
                    'type': 'text',
                    'influence_conversation': True,
                    'mappings': [
                        {
                            'type': 'from_entity',
                            'entity': 'service'
                        }
                    ]
                },
                'category': {
                    'type': 'text',
                    'influence_conversation': True,
                    'mappings': [
                        {
                            'type': 'from_entity',
                            'entity': 'category'
                        }
                    ]
                }
            },
            'responses': {
                'utter_greet': [
                    {'text': f'¡Hola! Soy el asistente virtual de {company_data.company_info.name}. ¿En qué puedo ayudarte?'},
                    {'text': f'¡Bienvenido a {company_data.company_info.name}! ¿Qué información necesitas?'},
                    {'text': '¡Hola! ¿Te puedo ayudar con información sobre nuestros productos o servicios?'}
                ],
                'utter_goodbye': [
                    {'text': '¡Hasta luego! Que tengas un excelente día.'},
                    {'text': 'Adiós, fue un placer ayudarte.'},
                    {'text': 'Nos vemos pronto. ¡Cuídate!'}
                ],
                'utter_ask_rephrase': [
                    {'text': 'No entendí bien. ¿Podrías reformular tu pregunta?'},
                    {'text': 'Disculpa, no comprendí. ¿Puedes preguntarlo de otra manera?'}
                ],
                'utter_default': [
                    {'text': 'No estoy seguro de cómo ayudarte con eso. ¿Puedes preguntarme sobre productos, servicios o precios?'}
                ]
            },
            'actions': [
                'action_show_products',
                'action_show_services', 
                'action_show_price',
                'utter_greet',
                'utter_goodbye',
                'utter_ask_rephrase',
                'utter_default'
            ],
            'session_config': {
                'session_expiration_time': 60,
                'carry_over_slots_to_new_session': True
            }
        }
        
        return domain_data
    
    def generate_stories_data(self, company_data: CompanyData) -> Dict[str, Any]:
        """Genera stories.yml completo"""
        
        stories_data = {
            'version': '3.1',
            'stories': [
                {
                    'story': 'saludo básico',
                    'steps': [
                        {'intent': 'greet'},
                        {'action': 'utter_greet'}
                    ]
                },
                {
                    'story': 'consulta productos',
                    'steps': [
                        {'intent': 'greet'},
                        {'action': 'utter_greet'},
                        {'intent': 'ask_products'},
                        {'action': 'action_show_products'}
                    ]
                },
                {
                    'story': 'consulta servicios',
                    'steps': [
                        {'intent': 'ask_services'},
                        {'action': 'action_show_services'}
                    ]
                },
                {
                    'story': 'consulta precios con producto',
                    'steps': [
                        {'intent': 'ask_price', 'entities': [{'entity': 'product', 'value': 'ejemplo'}]},
                        {'action': 'action_show_price'}
                    ]
                },
                {
                    'story': 'despedida',
                    'steps': [
                        {'intent': 'goodbye'},
                        {'action': 'utter_goodbye'}
                    ]
                },
                {
                    'story': 'flujo completo productos',
                    'steps': [
                        {'intent': 'greet'},
                        {'action': 'utter_greet'},
                        {'intent': 'ask_products'},
                        {'action': 'action_show_products'},
                        {'intent': 'ask_price'},
                        {'action': 'action_show_price'},
                        {'intent': 'goodbye'},
                        {'action': 'utter_goodbye'}
                    ]
                }
            ]
        }
        
        return stories_data
    
    def _get_greet_examples(self) -> str:
        return '''- hola
- buenos días
- buenas tardes
- buenas noches
- hey
- saludos
- hola qué tal
- buenas
- hello
- hi'''
    
    def _get_goodbye_examples(self) -> str:
        return '''- adiós
- hasta luego
- nos vemos
- bye
- chau
- hasta pronto
- me voy
- gracias, adiós
- eso es todo
- hasta la vista'''
    
    def _generate_product_examples(self, products) -> str:
        examples = [
            '- qué productos tienen',
            '- cuáles son sus productos',
            '- mostrar productos',
            '- productos disponibles',
            '- catálogo de productos',
            '- lista de productos',
            '- ver productos',
            '- productos que venden'
        ]
        
        for product in products[:3]:
            examples.extend([
                f'- información sobre {product.name.lower()}',
                f'- detalles de {product.name.lower()}',
                f'- cuéntame de {product.name.lower()}'
            ])
        
        return '\n'.join([f'- {ex}' if not ex.startswith('- ') else ex for ex in examples])
    
    def _generate_service_examples(self, services) -> str:
        examples = [
            '- qué servicios ofrecen',
            '- cuáles son sus servicios',
            '- mostrar servicios',
            '- servicios disponibles',
            '- lista de servicios',
            '- ver servicios',
            '- servicios que brindan'
        ]
        
        for service in services[:3]:
            examples.extend([
                f'- información sobre {service.name.lower()}',
                f'- detalles de {service.name.lower()}'
            ])
        
        return '\n'.join([f'- {ex}' if not ex.startswith('- ') else ex for ex in examples])
    
    def _generate_price_examples(self, company_data) -> str:
        examples = [
            '- cuánto cuesta',
            '- precio de',
            '- qué precio tiene',
            '- cuál es el precio',
            '- costos',
            '- precios',
            '- cuánto vale',
            '- información de precios'
        ]
        
        # Agregar ejemplos específicos
        for product in company_data.products[:2]:
            examples.extend([
                f'- cuánto cuesta {product.name.lower()}',
                f'- precio de {product.name.lower()}'
            ])
        
        for service in company_data.services[:2]:
            examples.extend([
                f'- cuánto cuesta {service.name.lower()}',
                f'- precio de {service.name.lower()}'
            ])
        
        return '\n'.join([f'- {ex}' if not ex.startswith('- ') else ex for ex in examples])
    
    def _generate_company_info_examples(self, company_info) -> str:
        examples = [
            '- información de la empresa',
            '- datos de la empresa',
            '- detalles de la empresa',
            '- historia de la empresa',
            '- misión y visión'
        ]
        
        # Agregar ejemplos específicos
        examples.extend([
            f'- cuéntame sobre {company_info.name.lower()}',
            f'- información sobre {company_info.name.lower()}'
        ])
        
        return '\n'.join([f'- {ex}' if not ex.startswith('- ') else ex for ex in examples])