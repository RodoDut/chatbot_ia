from typing import Dict, Any
import yaml

def generate_domain_yaml(company_data: Dict[str, Any]) -> str:
    """Generate domain.yml content"""
    domain = {
        'version': '3.1',
        'intents': [
            'greet',
            'goodbye',
            'ask_product_info',
            'ask_service_info'
        ],
        'entities': [
            'product',
            'service'
        ],
        'slots': {
            'product': {'type': 'text'},
            'service': {'type': 'text'}
        },
        'responses': {
            'utter_greet': [
                {'text': f"Welcome to {company_data['name']}! How can I help you today?"}
            ],
            'utter_goodbye': [
                {'text': "Goodbye! Have a great day!"}
            ],
            'utter_product_info': [
                {'text': "Let me tell you about our products..."}
            ],
            'utter_service_info': [
                {'text': "Here's information about our services..."}
            ]
        },
        'actions': [
            'action_product_info',
            'action_service_info'
        ]
    }
    
    return yaml.dump(domain, allow_unicode=True)