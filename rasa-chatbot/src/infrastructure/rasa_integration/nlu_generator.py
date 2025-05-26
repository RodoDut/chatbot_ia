from typing import Dict, Any
import yaml

def generate_product_intents(products: list) -> dict:
    """Generate intents for products"""
    examples = []
    for product in products:
        examples.extend([
            f"What is the price of {product['name']}?",
            f"Tell me about {product['name']}",
            f"Do you have {product['name']}?",
            f"I want to know more about {product['name']}"
        ])
    
    return {
        'intent': 'ask_product_info',
        'examples': '\n'.join(f"- {example}" for example in examples)
    }

def generate_service_intents(services: list) -> dict:
    """Generate intents for services"""
    examples = []
    for service in services:
        examples.extend([
            f"What is the cost of {service['name']}?",
            f"Tell me about {service['name']} service",
            f"Do you offer {service['name']}?",
            f"I need information about {service['name']}"
        ])
    
    return {
        'intent': 'ask_service_info',
        'examples': '\n'.join(f"- {example}" for example in examples)
    }

def generate_nlu_yaml(company_data: Dict[str, Any]) -> str:
    """Generate NLU training data in YAML format"""
    nlu_data = {
        'version': '3.1',
        'nlu': [
            generate_product_intents(company_data['products']),
            generate_service_intents(company_data['services']),
            {
                'intent': 'greet',
                'examples': '- hey\n- hello\n- hi\n- good morning\n- good evening'
            },
            {
                'intent': 'goodbye',
                'examples': '- bye\n- goodbye\n- see you around\n- see you later'
            }
        ]
    }
    
    return yaml.dump(nlu_data, allow_unicode=True)