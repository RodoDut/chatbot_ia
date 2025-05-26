# Rasa Chatbot with Clean Architecture

Este proyecto implementa un chatbot inteligente utilizando Rasa y siguiendo los principios de Clean Architecture y SOLID. El chatbot está diseñado para ser fácilmente adaptable a diferentes compañías, permitiendo obtener información de productos y servicios de manera automatizada.

## Características

- Arquitectura limpia (Clean Architecture)
- Principios SOLID
- Web scraping automatizado
- Generación automática de datos de entrenamiento
- Fácilmente adaptable a diferentes compañías

## Estructura del Proyecto

```
rasa-chatbot/
├── src/                        # Código fuente principal
│   ├── domain/                 # Lógica de negocio
│   │   ├── entities/          # Entidades del dominio
│   │   └── services/          # Servicios del dominio
│   ├── infrastructure/         # Implementaciones concretas
│   │   ├── scrapers/          # Web scrapers
│   │   ├── data_sources/      # Fuentes de datos
│   │   └── rasa_integration/  # Integración con Rasa
│   ├── application/           # Casos de uso
│   │   ├── interfaces/        # Interfaces
│   │   └── use_cases/        # Casos de uso
│   └── config/                # Configuraciones
├── actions/                   # Acciones personalizadas de Rasa
└── data/                     # Datos de entrenamiento
```

## Requisitos

- Python 3.9+
- Rasa 3.0+
- BeautifulSoup4
- Requests

## Instalación

1. Crear entorno virtual:
```bash
python -m venv chatbotvenv
```

2. Activar entorno virtual:
```bash
# Windows
.\chatbotvenv\Scripts\activate
# Linux/Mac
source chatbotvenv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Configurar una nueva compañía:
   - Crear un nuevo scraper en `src/infrastructure/scrapers/`
   - Registrar la compañía en `src/config/company_config.py`

2. Ejecutar el programa principal:
```bash
python main.py
```

3. Entrenar el modelo:
```bash
rasa train
```

4. Iniciar el chatbot:
```bash
rasa run actions  # En una terminal
rasa shell       # En otra terminal
```

## Agregar una Nueva Compañía

1. Crear un nuevo scraper heredando de `BaseScraper`
2. Implementar los métodos `scrape_products()` y `scrape_services()`
3. Registrar la nueva compañía en `CompanyRegistry`

## Licencia

MIT

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.
