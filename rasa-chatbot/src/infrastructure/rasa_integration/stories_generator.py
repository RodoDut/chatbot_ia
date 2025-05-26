from typing import Dict, Any
import yaml

def generate_stories_yaml(company_data: Dict[str, Any]) -> str:
    """Generate stories.yml content"""
    stories = {
        'version': '3.1',
        'stories': [
            {
                'story': 'greet and goodbye',
                'steps': [
                    {'intent': 'greet'},
                    {'action': 'utter_greet'},
                    {'intent': 'goodbye'},
                    {'action': 'utter_goodbye'}
                ]
            },
            {
                'story': 'ask about product',
                'steps': [
                    {'intent': 'ask_product_info'},
                    {'action': 'action_product_info'}
                ]
            },
            {
                'story': 'ask about service',
                'steps': [
                    {'intent': 'ask_service_info'},
                    {'action': 'action_service_info'}
                ]
            }
        ]
    }
    
    return yaml.dump(stories, allow_unicode=True)