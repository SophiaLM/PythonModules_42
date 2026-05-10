# Ejercicio 1: Alien Contact Logs

## 1. Objetivo del Ejercicio

Validar datos de contactos extraterrestres con Pydantic, aplicando reglas de negocio personalizadas mediante `@model_validator`. El ejercicio demuestra cómo garantizar la integridad de datos complejos que requieren validaciones inter-campos.

---

## 2. Enum ContactType

```python
class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"
```

Define los cuatro tipos posibles de contacto extraterrestre documentados por Cosmic Data.

---

## 3. Modelo AlienContact

```python
class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False
```

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `contact_id` | `str` | Identificador unico (5-15 caracteres) |
| `timestamp` | `datetime` | Fecha y hora del contacto |
| `location` | `str` | Ubicacion geografica (3-100 caracteres) |
| `contact_type` | `ContactType` | Tipo de contacto (enum) |
| `signal_strength` | `float` | Intensidad de la seal (0.0 a 10.0) |
| `duration_minutes` | `int` | Duracion en minutos (1 a 1440) |
| `witness_count` | `int` | Numero de testigos (1 a 100) |
| `message_received` | `str | None` | Mensaje recibido (opcional, max 500 chars) |
| `is_verified` | `bool` | Si el contacto fue verificado |

---

## 4. Validacion Personalizada con @model_validator

```python
@model_validator(mode="after")
def validate_contact(self) -> "AlienContact":
    # Regla 1: Contact ID debe empezar con "AC"
    if not self.contact_id.startswith("AC"):
        raise ValueError("Contact ID must start with 'AC'")

    # Regla 2: Contactos fisicos deben estar verificados
    if self.contact_type == ContactType.physical and not self.is_verified:
        raise ValueError("Physical contact reports must be verified")

    # Regla 3: Contactos telepaticos requieren 3+ testigos
    if (self.contact_type == ContactType.telepathic
            and self.witness_count < 3):
        raise ValueError("Telepathic contact requires at least 3 witnesses")

    # Regla 4: Senales fuertes (>7.0) deben incluir mensaje
    if self.signal_strength > 7.0 and not self.message_received:
        raise ValueError(
            "Strong signals (>7.0) should include received messages"
        )

    return self
```

### Reglas de Validacion

| Regla | Descripcion |
|-------|------------|
| **Regla 1** | El ID de contacto debe iniciar con el prefijo "AC" para mantener consistencia en la nomenclatura de Cosmic Data. |
| **Regla 2** | Solo contactos fisicos verificados son aceptados; previene reportes no confirmados de encuentros directos. |
| **Regla 3** | Contactos telepaticos requieren minimo 3 testigos independientes para confirmar experiencias subjetivas. |
| **Regla 4** | Senales con intensidad mayor a 7.0 deben incluir el mensaje recibido; asegura datos completos para eventos significativos. |

---

## 5. Explicacion de model_validator(mode='after')

### Modo 'before' vs 'after'

| Modo | Cuando se ejecuta | Uso comun |
|------|-------------------|-----------|
| `'before'` | Antes de la coercion de tipos | Normalizar datos crudos, limpiar inputs |
| `'after'` | Despues de validar campos individuales | Validar reglas de negocio inter-campos |

### Por que 'after' en este ejercicio?

El validador `mode="after"` se ejecuta **despues** de que Pydantic ha:
1. Convertido los datos de entrada a los tipos correctos
2. Aplicado las restricciones de `Field()` (min_length, ge, etc.)
3. Creado la instancia del modelo

Esto permite acceder a los valores ya tipados correctamente:

```python
# self.contact_type es un enum (no un string)
# self.signal_strength es un float (no un string)
# Se puede comparar directamente sin conversiones
if self.signal_strength > 7.0 and not self.message_received:
    ...
```

Sin `mode='after'`, deberiamos hacer conversiones manuales o verificar tipos dentro del validador.

---

## 6. Codigo Completo

```python
from datetime import datetime

from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (self.contact_type == ContactType.telepathic
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (>7.0) should include received messages"
            )

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")

    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 3, 15, 14, 30),
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True,
    )

    print("Valid contact report:")
    print(f"  ID: {valid_contact.contact_id}")
    print(f"  Type: {valid_contact.contact_type.value}")
    print(f"  Location: {valid_contact.location}")
    print(f"  Signal: {valid_contact.signal_strength}/10")
    print(f"  Duration: {valid_contact.duration_minutes} minutes")
    print(f"  Witnesses: {valid_contact.witness_count}")
    print(f"  Message: {valid_contact.message_received!r}")

    print("======================================")
    print("Expected validation error:")

    try:
        AlienContact(
            contact_id="TEST_001",
            timestamp=datetime.now(),
            location="Unknown Location",
            contact_type=ContactType.telepathic,
            signal_strength=5.0,
            duration_minutes=30,
            witness_count=2,
            is_verified=False,
        )
    except Exception as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
```

---

## Ejecucion

```bash
python ex1/alien_contact.py
```

**Salida esperada:**
```
Alien Contact Log Validation
======================================
Valid contact report:
  ID: AC_2024_001
  Type: radio
  Location: Area 51, Nevada
  Signal: 8.5/10
  Duration: 45 minutes
  Witnesses: 5
  Message: 'Greetings from Zeta Reticuli'
======================================
Expected validation error:
  2 validation errors for AlienContact
  contact_id
    Contact ID must start with 'AC' [type=value_error, input_value='TEST_001', ...
  witness_count
    Telepathic contact requires at least 3 witnesses [type=value_error, ...
```