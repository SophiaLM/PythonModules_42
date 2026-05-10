# Ejercicio 0: Space Station Data

## 1. Objetivo del Ejercicio

Introducir los conceptos fundamentales de Pydantic mediante la creacion de un modelo `SpaceStation` que representa los datos de una estacion espacial. El ejercicio demuestra como definir modelos con validacion automatica de datos, usando restricciones en campos de texto, numericos y valores booleanos.

## 2. Modelo SpaceStation

El modelo `SpaceStation` define la estructura de datos para una estacion espacial con los siguientes campos:

```python
class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)
```

### Campos y validaciones

| Campo | Tipo | Validacion | Descripcion |
|-------|------|------------|-------------|
| `station_id` | `str` | `min_length=3`, `max_length=10` | Identificador unico de 3 a 10 caracteres |
| `name` | `str` | `min_length=1`, `max_length=50` | Nombre de la estacion |
| `crew_size` | `int` | `ge=1`, `le=20` | Tamano de tripulacion entre 1 y 20 |
| `power_level` | `float` | `ge=0.0`, `le=100.0` | Nivel de energia entre 0% y 100% |
| `oxygen_level` | `float` | `ge=0.0`, `le=100.0` | Nivel de oxigeno entre 0% y 100% |
| `last_maintenance` | `datetime` | Sin restricciones | Fecha de ultimo mantenimiento |
| `is_operational` | `bool` | Valor por defecto `True` | Estado operativo de la estacion |
| `notes` | `str \| None` | `max_length=200` | Notas opcionales, maximo 200 caracteres |

## 3. Conceptos de Pydantic

### Herencia de BaseModel

`SpaceStation` hereda de `BaseModel`, la clase base de Pydantic. Esto habilita automaticamente:

- Validacion de datos al crear instancias
- Conversión de tipos (type coercion)
- Serializacion a diccionarios y JSON
- Generacion de esquemas JSON para documentacion

### Field() para Validacion

La funcion `Field()` define validaciones individuales para cada campo:

```python
station_id: str = Field(..., min_length=3, max_length=10)
```

- `...` (Ellipsis): Indica que el campo es requerido, no puede ser `None` ni omitido
- `min_length=N`: Longitud minima del texto
- `max_length=N`: Longitud maxima del texto
- `ge=N`: Mayor o igual que N (greater than or equal)
- `le=N`: Menor o igual que N (less than or equal)
- `default=valor`: Valor por defecto si no se proporciona

### Tipos Basicos

El modelo utiliza tipos primitivos de Python:

| Tipo | Descripcion | Ejemplo |
|------|-------------|---------|
| `str` | Cadena de texto | `"ISS001"` |
| `int` | Numero entero | `6` |
| `float` | Numero decimal | `85.5` |
| `bool` | Valor booleano | `True` |
| `datetime` | Fecha y hora | `datetime(2024, 1, 15, 10, 30)` |

### Campos Opcionales

Los campos opcionales se declaran con `| None` o `Optional[T]`:

```python
notes: str | None = Field(default=None, max_length=200)
```

- `str | None`: Indica que puede ser una cadena o `None`
- `default=None`: Si se omite el campo, toma el valor `None`

## 4. Codigo Completo

```python
from datetime import datetime

from pydantic import BaseModel, Field


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 10, 30),
        is_operational=True,
    )

    print("Valid station created:")
    print(f"  ID: {valid_station.station_id}")
    print(f"  Name: {valid_station.name}")
    print(f"  Crew: {valid_station.crew_size} people")
    print(f"  Power: {valid_station.power_level}%")
    print(f"  Oxygen: {valid_station.oxygen_level}%")
    is_op = valid_station.is_operational
    status = "Operational" if is_op else "Non-operational"
    print(f"  Status: {status}")

    print("========================================")
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="ISS002",
            name="Test Station",
            crew_size=25,  # Excede le=20, genera error
            power_level=80.0,
            oxygen_level=90.0,
            last_maintenance=datetime.now(),
        )
    except Exception as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
```

### Salida Esperada

```
Space Station Data Validation
========================================
Valid station created:
  ID: ISS001
  Name: International Space Station
  Crew: 6 people
  Power: 85.5%
  Oxygen: 92.3%
  Status: Operational
========================================
Expected validation error:
  1 validation error for SpaceStation
  crew_size
    Field required greater than or equal to 20 ...
```

## 5. Conceptos Clave Aprendidos

1. **BaseModel**: Clase fundamental de Pydantic que proporciona validacion automatica
2. **Field()**: Funcion para definir restricciones de validacion personalizadas
3. **Validaciones numericas**: `ge` y `le` para establecer limites en valores numericos
4. **Validaciones de texto**: `min_length` y `max_length` para longitudes de cadenas
5. **Campos opcionales**: Se declaran con `| None` y `default=None`
6. **Valores por defecto**: Se asignan con `default=valor` en `Field()`
7. **Conversion de tipos**: Pydantic convierte automaticamente tipos compatibles
8. **Errores de validacion**: Se lanzan excepciones `ValidationError` cuando los datos no cumplen las restricciones

Este ejercicio establece las bases para trabajar con Pydantic en ejercicios posteriores que modelsaran entidades mas complejas como astronautas y contactos alienigenas.
