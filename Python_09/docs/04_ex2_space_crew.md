# Ejercicio 2: Space Crew Management

## Objetivo del Ejercicio

Este ejercicio introduce el concepto de **modelos anidados** en Pydantic. El objetivo es aprender a:

- Definir modelos que contienen otros modelos como atributos
- Utilizar enumeraciones (`Enum`) para representar valores predefinidos
- Aplicar validaciones avanzadas con `@model_validator` que involucran relaciones entre objetos anidados

En este caso, modelamos una misión espacial donde la misión contiene una lista de miembros de la tripulación (`CrewMember`). Las validaciones deben considerar el estado y composición de toda la tripulación.

---

## 1. Enum Rank

El enum `Rank` define los cinco rangos posibles para los miembros de la tripulación:

```python
class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"
```

Los rangos están ordenados jerárquicamente desde `cadet` (más bajo) hasta `commander` (más alto).

---

## 2. Modelo CrewMember

Representa a un miembro individual de la tripulación:

```python
class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `member_id` | str | Identificador único (3-10 caracteres) |
| `name` | str | Nombre del miembro (2-50 caracteres) |
| `rank` | Rank | Rango del miembro |
| `age` | int | Edad (entre 18 y 80 años) |
| `specialization` | str | Especialización (3-30 caracteres) |
| `years_experience` | int | Años de experiencia (0-50) |
| `is_active` | bool | Si está activo (por defecto True) |

---

## 3. Modelo SpaceMission

Contiene la lista de miembros de la tripulación como atributo anidado:

```python
class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `mission_id` | str | Identificador de la misión (5-15 caracteres) |
| `mission_name` | str | Nombre de la misión |
| `destination` | str | Destino de la misión |
| `launch_date` | datetime | Fecha de lanzamiento |
| `duration_days` | int | Duración en días (1-3650) |
| `crew` | list[CrewMember] | Lista de miembros de la tripulación (1-12) |
| `mission_status` | str | Estado de la misión (por defecto "planned") |
| `budget_millions` | float | Presupuesto en millones |

---

## 4. Validaciones con @model_validator

El decorator `@model_validator(mode="after")` permite validar reglas que dependen de múltiples atributos del modelo después de que se hayan procesado todos los campos.

### Validación 1: Mission ID debe empezar con "M"

```python
if not self.mission_id.startswith("M"):
    raise ValueError("Mission ID must start with 'M'")
```

### Validación 2: Debe haber al menos un Commander o Captain

```python
has_commander = any(
    c.rank in (Rank.commander, Rank.captain) for c in self.crew
)
if not has_commander:
    raise ValueError(
        "Mission must have at least one Commander or Captain"
    )
```

### Validación 3: Misiones largas necesitan 50% con experiencia

```python
if self.duration_days > 365:
    experienced = sum(1 for c in self.crew if c.years_experience >= 5)
    required = len(self.crew) * 0.5
    if experienced < required:
        raise ValueError(
            "Long missions (>365 days) need "
            "50% experienced crew (5+ years)"
        )
```

### Validación 4: Todos los miembros deben estar activos

```python
if not all(c.is_active for c in self.crew):
    raise ValueError("All crew members must be active")
```

---

## 5. Explicación de Validación de Modelos Anidados

La validación de modelos anidados en Pydantic presenta consideraciones especiales:

### Acceso a modelos hijos

En el `@model_validator`, podemos acceder a todos los miembros de la tripulación a través de `self.crew`. Cada elemento es una instancia de `CrewMember` con todos sus atributos validados.

### Validación entre objetos

Las validaciones pueden establecer relaciones entre objetos. Por ejemplo, verificar que existe un comandante implica iterar sobre la lista y evaluar el atributo `rank` de cada miembro.

### Cascada de validación

Los modelos hijos (`CrewMember`) se validan primero individualmente según sus propias reglas. Luego, el `@model_validator` del padre (`SpaceMission`) puede realizar validaciones que involucren la colección completa.

### Orden de ejecución

1. Se validan los campos simples de `SpaceMission`
2. Se valida cada `CrewMember` individualmente
3. Se ejecuta el `@model_validator` de `SpaceMission`
4. Si todo es válido, se retorna la instancia

---

## 6. Código Completo

```python
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_commander = any(
            c.rank in (Rank.commander, Rank.captain) for c in self.crew
        )
        if not has_commander:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(1 for c in self.crew if c.years_experience >= 5)
            required = len(self.crew) * 0.5
            if experienced < required:
                raise ValueError(
                    "Long missions (>365 days) need "
                    "50% experienced crew (5+ years)"
                )

        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2025, 6, 1, 12, 0),
        duration_days=900,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=42,
                specialization="Mission Command",
                years_experience=15,
                is_active=True,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=35,
                specialization="Navigation",
                years_experience=10,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=28,
                specialization="Engineering",
                years_experience=6,
                is_active=True,
            ),
        ],
        mission_status="planned",
        budget_millions=2500.0,
    )

    print("Valid mission created:")
    print(f"  Mission: {valid_mission.mission_name}")
    print(f"  ID: {valid_mission.mission_id}")
    print(f"  Destination: {valid_mission.destination}")
    print(f"  Duration: {valid_mission.duration_days} days")
    print(f"  Budget: ${valid_mission.budget_millions}M")
    print(f"  Crew size: {len(valid_mission.crew)}")
    print("  Crew members:")
    for member in valid_mission.crew:
        rank = member.rank.value
        spec = member.specialization
        print(f"    - {member.name} ({rank}) - {spec}")

    print("========================================")
    print("Expected validation error:")

    try:
        SpaceMission(
            mission_id="FAIL001",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime(2025, 1, 1),
            duration_days=30,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Test User",
                    rank=Rank.officer,
                    age=25,
                    specialization="Test",
                    years_experience=2,
                    is_active=True,
                ),
            ],
            budget_millions=100.0,
        )
    except Exception as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
```

### Ejecución

```
$ python ex2/space_crew.py
Space Mission Crew Validation
========================================
Valid mission created:
  Mission: Mars Colony Establishment
  ID: M2024_MARS
  Destination: Mars
  Duration: 900 days
  Budget: $2500.0M
  Crew size: 3
  Crew members:
    - Sarah Connor (commander) - Mission Command
    - John Smith (lieutenant) - Navigation
    - Alice Johnson (officer) - Engineering
========================================
Expected validation error:
  Mission must have at least one Commander or Captain
```