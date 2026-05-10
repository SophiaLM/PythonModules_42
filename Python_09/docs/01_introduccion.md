# Cosmic Data: Pydantic Models & Validation

## Introducción

Pydantic es una biblioteca de Python para la validación de datos utilizando modelos basados en anotaciones de tipo. Permite definir estructuras de datos con validaciones automáticas, conversión de tipos y generación de mensajes de error detallados.

**¿Por qué es importante?**
- Valida datos de forma automática sin escribir código adicional
- Convierte tipos automáticamente (ej: strings a datetime)
- Genera esquemas JSON para APIs
- Reduce errores en sistemas de datos y APIs

Este proyecto teachnology Pydantic 2.x a través de tres ejercicios con temática espacial, progressing desde modelos básicos hasta validaciones complejas.

## Conceptos Clave de Pydantic

### BaseModel

La clase base para todos los modelos Pydantic. Hereda de `BaseModel` para crear clases de datos validadas automáticamente.

```python
from pydantic import BaseModel

class SpaceStation(BaseModel):
    station_id: str
    name: str
    crew_size: int
```

### Field

Define validación y metadata para campos individuales. Permite especificar restricciones y valores por defecto.

```python
from pydantic import BaseModel, Field

class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    crew_size: int = Field(ge=1, le=20)
```

### model_validator

Decorador para validación personalizada que se ejecuta después de la validación de campos individuales. Reemplaza el deprecated `@validator` de Pydantic v1.

```python
from pydantic import model_validator

class AlienContact(BaseModel):
    contact_type: str
    witness_count: int

    @model_validator(mode='after')
    def validate_contact(self):
        if self.contact_type == 'telepathic' and self.witness_count < 3:
            raise ValueError('Telepathic contact requires at least 3 witnesses')
        return self
```

## Requisitos del Proyecto

| Requisito | Descripción |
|-----------|-------------|
| **Python** | 3.10 o superior |
| **Pydantic** | Versión 2.x |
| **flake8** | Verificación de estilo de código |
| **mypy** | Validación de tipos estáticos |
| **venv** | Entorno virtual recomendado |

## Estructura del Proyecto

```
Python_09/
├── ex0/                 # Ejercicio 0: Space Station Data
│   └── space_station.py # Modelo básico con BaseModel y Field
│
├── ex1/                 # Ejercicio 1: Alien Contact Logs
│   └── alien_contact.py # Validación personalizada con model_validator
│
├── ex2/                 # Ejercicio 2: Space Crew Management
│   └── space_crew.py    # Modelos anidados y reglas complejas
│
└── docs/
    └── 01_introduccion.md
```

### Progresión de los Ejercicios

| Ejercicio | Concepto Principal | Descripción |
|-----------|---------------------|-------------|
| **ex0** | BaseModel, Field | Validación básica de campos de estación espacial |
| **ex1** | model_validator | Reglas de negocio para registros de contacto alienígena |
| **ex2** | Modelos anidados | Gestión de misiones espaciales con tripulación |