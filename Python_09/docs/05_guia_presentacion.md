# Guía de Presentación: Cosmic Data - Pydantic Models & Validation

## 1. Estructura Recomendada de la Presentación

**Tiempo total sugerido: 20-25 minutos**

| Sección | Tiempo | Objetivo |
|---------|--------|----------|
| Introducción a Pydantic | 4 min | Contextualizar, despertar interés |
| Ejercicio 0: Conceptos Básicos | 5 min | Mostrar Field y validación automática |
| Ejercicio 1: Validación Custom | 6 min | Profundizar en model_validator |
| Ejercicio 2: Modelos Anidados | 6 min | Demostrar complejidad real |
| Demostración Práctica | 4 min | Impacto con live coding |
| Preguntas y Tips | 3 min | Cerrar con confianza |

---

## 2. Qué Explicar en Cada Sección

### 2.1 Introducción a Pydantic (4 min)

**Conceptos clave a transmitir:**

- Pydantic es una biblioteca de validación de datos que usa **type hints** de Python
- Define modelos heredando de `BaseModel`
- Validación automática + conversión de tipos
- Errores claros y accionables

**Ejemplo rápido que pueden entender inmediatamente:**

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Pydantic convierte automáticamente
user = User(name="Ana", age="25")  # str "25" → int 25 ✅
user = User(name="Ana", age="veinticinco")  # Error claro ❌
```

**Pregunta que quizás surja:** _¿Por qué no usar simplemente `if/else` o Try/Except?_

**Respuesta:** Pydantic centraliza la validación en un solo lugar, hace el código reutilizable, y proporciona mensajes de error estándar. Con `if/else` tendrías que escribir validación en cada lugar donde usas los datos.

---

### 2.2 Ejercicio 0: Conceptos Básicos (5 min)

**Archivo:** `ex0/space_station.py`

**Qué destacar:**

1. **`Field(...)` con constraints:**
   ```python
   crew_size: int = Field(..., ge=1, le=20)
   # ge = greater than or equal
   # le = less than or equal
   ```

2. **Valores por defecto:**
   ```python
   is_operational: bool = True  #默认值
   notes: str | None = Field(default=None, max_length=200)  #可选
   ```

3. **Conversión automática de tipos:**
   ```python
   last_maintenance=datetime(2024, 1, 15)  # datetime object funciona
   last_maintenance="2024-01-15T10:30:00"  # string también se convierte
   ```

4. **Error cuando falla la validación:**
   ```
   Input should be less than or equal to 20
   ```

**Ejecutar en vivo:**
```bash
cd /home/soluna/PythonModules_42/Python_09/ex0 && python space_station.py
```

---

### 2.3 Ejercicio 1: Custom Validation (6 min)

**Archivo:** `ex1/alien_contact.py`

**Qué destacar:**

1. **Enum para tipos definidos:**
   ```python
   class ContactType(Enum):
       radio = "radio"
       visual = "visual"
       telepathic = "telepathic"
   ```

2. **`@model_validator(mode='after')`:**
   - Se ejecuta DESPUÉS de que Pydantic valida todos los campos individuales
   - Recibe `self` con todos los campos ya validados
   - Debe retornar `self` al final

3. **Reglas de negocio implementadas:**
   ```python
   @model_validator(mode="after")
   def validate_contact(self) -> "AlienContact":
       if self.contact_type == ContactType.physical and not self.is_verified:
           raise ValueError("Physical contact reports must be verified")
       # ... más reglas
       return self
   ```

4. **Validación cross-field:**
   - Una regla que involucra múltiples campos (contact_type + is_verified)
   - No se puede hacer solo con `Field`

**Error esperado cuando falla:**
```
Telepathic contact requires at least 3 witnesses
```

**Ejecutar en vivo:**
```bash
cd /home/soluna/PythonModules_42/Python_09/ex1 && python alien_contact.py
```

---

### 2.4 Ejercicio 2: Modelos Anidados (6 min)

**Archivo:** `ex2/space_crew.py`

**Qué destacar:**

1. **Dos modelos relacionados:**
   - `CrewMember` - datos individuales de un tripulante
   - `SpaceMission` - contiene lista de `CrewMember`

2. **Lista de modelos anidados:**
   ```python
   crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
   ```

3. **Validación que recorre la lista:**
   ```python
   if not all(c.is_active for c in self.crew):
       raise ValueError("All crew members must be active")
   ```

4. **Validación compleja (50% requirement):**
   ```python
   if self.duration_days > 365:
       experienced = sum(1 for c in self.crew if c.years_experience >= 5)
       required = len(self.crew) * 0.5
       if experienced < required:
           raise ValueError("Long missions need 50% experienced crew")
   ```

5. **Pydantic valida automáticamente los modelos anidados:**
   - Si `CrewMember` tiene datos inválidos, `SpaceMission` falla

**Error esperado:**
```
Mission must have at least one Commander or Captain
```

**Ejecutar en vivo:**
```bash
cd /home/soluna/PythonModules_42/Python_09/ex2 && python space_crew.py
```

---

## 3. Preguntas Típicas y Respuestas

### 3.1 Diferencia entre `Field` y `model_validator`

| Aspecto | `Field` | `model_validator` |
|---------|---------|-------------------|
| **Qué valida** | Un solo campo | Múltiples campos o lógica de negocio |
| **Cuándo** | Durante validación del campo | Después de que todos los campos están validados |
| **Limitaciones** | No puede ver otros campos | Ve todos los campos pero no puede modificar tipos |
| **Uso típico** | Constraints simples (rango, longitud, regex) | Reglas de negocio, validaciones cross-field |

**Ejemplo de cuándo usar cada uno:**

```python
# Field: validaciones simples
name: str = Field(..., min_length=1)
age: int = Field(..., ge=0, le=150)

# model_validator: lógica de negocio
@model_validator(mode="after")
def validate(self):
    if self.is_admin and not self.email_verified:
        raise ValueError("Admin must have verified email")
    return self
```

---

### 3.2 Cuándo usar `mode='before'` vs `mode='after'`

**`mode='after'` (el más común):**
- Todos los campos ya están validados y convertidos
- Trabajas con datos "limpios" y tipados correctamente
- Recibes la instancia del modelo

```python
@model_validator(mode="after")
def validate(self) -> "AlienContact":
    # self tiene todos los campos con sus tipos correctos
    # puedes acceder a self.contact_type, self.witness_count, etc.
    return self
```

**`mode='before'` (avanzado):**
- Recibes los datos "crudos" antes de cualquier conversión
- Útil para transformar datos de entrada
- Trabajas con dict o datos sin procesar

```python
@model_validator(mode="before")
def clean_data(cls, data):
    if isinstance(data, dict):
        data['name'] = data.get('name', '').strip()
    return data
```

**Regla práctica:** Empieza con `mode='after'`. Solo usa `mode='before'` cuando necesitas transformar datos antes de que Pydantic los procese.

---

### 3.3 Cómo maneja Pydantic la validación de modelos anidados

**El flujo es recursivo y ordenado:**

1. Pydantic recibe `SpaceMission` con `crew: [CrewMember, CrewMember, ...]`
2. Valida campos simples de `SpaceMission` (mission_id, duration_days, etc.)
3. Para cada `CrewMember` en la lista `crew`:
   - Valida `member_id`, `name`, `rank`, etc.
   - Si algún `CrewMember` falla, todo falla
4. Después de validar todos los campos, ejecuta `model_validator` de `SpaceMission`

**Demostración visual:**

```
SpaceMission (validando...)
├── mission_id: "M2024_MARS" ✅
├── duration_days: 900 ✅
├── crew: [CrewMember, CrewMember, ...] 
│   ├── CrewMember[0]
│   │   ├── member_id: "CM001" ✅
│   │   ├── rank: Rank.commander ✅
│   │   └── ... ✅
│   ├── CrewMember[1]
│   │   └── ... ✅
│   └── CrewMember[2]
│       └── ... ✅
└── model_validator de SpaceMission ✅ (se ejecuta al final)
```

**Si un CrewMember tiene crew_size=50, el error indica exactamente dónde está el problema.**

---

### 3.4 Errores Comunes y Cómo Evitarlos

**Error 1: Olvidar `return self` en el validator**

```python
# ❌ INCORRECTO - causa confusión
@model_validator(mode="after")
def validate_contact(self) -> "AlienContact":
    if self.signal_strength > 7:
        raise ValueError("Too strong")
    # olvidaste return self

# ✅ CORRECTO
@model_validator(mode="after")
def validate_contact(self) -> "AlienContact":
    if self.signal_strength > 7:
        raise ValueError("Too strong")
    return self
```

**Error 2: Usar `mode='before'` cuando no es necesario**

```python
# ❌ INCORRECTO - complica innecesariamente
@model_validator(mode="before")
def clean_fields(cls, data):
    if isinstance(data, dict):
        data['name'] = str(data.get('name', '')).strip()
    return data

# ✅ CORRECTO - Pydantic ya hace conversión de tipos
name: str = Field(default="")
# Solo usa mode='before' si necesitas lógica de pre-transformación
```

**Error 3: Validar campos en el orden incorrecto**

```python
# En mode='after', los campos ya están validados individualmente
@model_validator(mode="after")
def validate(self) -> "MyModel":
    # Aquí puedes asumir que:
    # - self.age existe y es int
    # - self.name existe y es str
    # - NO necesitas verificar si son None (ya lo hizo Pydantic)
    pass
```

**Error 4: Confundir `model_validator` con `field_validator`**

```python
# Si solo necesitas validar UN campo, usa field_validator
from pydantic import field_validator

class User(BaseModel):
    age: int
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

---

## 4. Demostración Práctica - Qué Mostrar en Vivo

### 4.1 Configuración Previa (antes de la presentación)

Preparar terminal con:
- Carpeta del proyecto abierta
- Editor listo (VS Code o similar)
- Tres terminales pequeñas abiertas, una por ejercicio

### 4.2 Demo 1: Conversión Automática (1 min)

**Archivo:** Crear archivo temporal `demo_conversion.py`

```python
from pydantic import BaseModel
from datetime import datetime

class Demo(BaseModel):
    timestamp: datetime
    count: int

# Mostrar que Pydantic convierte tipos automáticamente
demo = Demo(timestamp="2024-01-15T10:30:00", count="42")
print(f"timestamp: {demo.timestamp} (type: {type(demo.timestamp)})")
print(f"count: {demo.count} (type: {type(demo.count)})")
```

**Salida esperada:**
```
timestamp: 2024-01-15 10:30:00 (type: <class 'datetime.datetime'>)
count: 42 (type: <class 'int'>)
```

---

### 4.3 Demo 2: Modificar Datos en Vivo (2 min)

En el archivo `ex0/space_station.py`, mostrar qué pasa con diferentes valores:

1. Crear estación válida → funciona
2. Cambiar `crew_size=25` → error "less than or equal to 20"
3. Cambiar `power_level="invalid"` → error de tipo
4. Quitar `last_maintenance` → error "field required"

Esto demuestra que Pydantic valida:
- Rangos numéricos
- Tipos de datos
- Campos obligatorios vs opcionales

---

### 4.4 Demo 3: Modelos Anidados en Acción (1 min)

En `ex2/space_crew.py`, modificar el mission_id para que no empiece con "M":

```python
# Cambiar mission_id de "M2024_MARS" a "FAIL_001"
mission_id="FAIL_001"  # debería fallar con modelo_validator
```

También probar cambiar crew_size a 15 sin commanders:

```python
crew=[
    CrewMember(member_id="C001", name="Test", rank=Rank.officer, ...),  # solo officer
    CrewMember(member_id="C002", name="Test2", rank=Rank.officer, ...), # solo officer
    # Sin commander ni captain
]
```

---

## 5. Consejos de Experto

### 5.1 Antes de la Presentación

1. **Ejecuta cada ejercicio 3 veces** - asegúrate de que la salida es exactamente la esperada
2. **Prepara respuestas para estas 3 preguntas** que siempre salen:
   - "¿Por qué usar Pydantic y no dataclasses?"
   - "¿Qué pasa si tengo datos que vienen de una API externa?"
   - "¿Cómo manejas errores de validación en producción?"

3. **Ten el código de instrucciones visible** - a veces te piden que muestres los requisitos exactos

### 5.2 Durante la Presentación

1. **Nombra las cosas correctamente:**
   - Di "decorador model_validator" no solo "validador"
   - Di "constraint ge" no solo "ge"

2. **Muestra siempre el error completo** - no solo digas "falla", muestra el mensaje real
   ```
   "less than or equal to 20" - esto comunica mejor que "el número está malo"
   ```

3. **Compara con código equivalente sin Pydantic:**
   ```python
   # Sin Pydantic - tedioso y repetitivo
   if not isinstance(data.get('crew_size'), int):
       raise TypeError("crew_size must be int")
   if not (1 <= data['crew_size'] <= 20):
       raise ValueError("crew_size must be 1-20")
   
   # Con Pydantic - limpio
   crew_size: int = Field(..., ge=1, le=20)
   ```

4. **Resalta el mensaje de error** - Pydantic da errores muy descriptivos

### 5.3 Frases Clave para Demostrar Dominio

- "Pydantic usa type hints de Python para definir esquemas de validación"
- "Field(...) permite definir constraints individuales por campo"
- "@model_validator(mode='after') ejecuta lógica de negocio después de la validación de campos"
- "La validación de modelos anidados es recursiva - Pydantic valida cada objeto interno"
- "Los mensajes de error de Pydantic indican exactamente qué campo falló y por qué"

### 5.4 Si No Sabes la Respuesta

Si te preguntan algo fuera del alcance:
1. Di "Esa es una pregunta interesante que toca un tema más avanzado"
2. Explica lo que SÍ sabes del tema
3. Menciona que te gustaría investigarlo más a fondo

**Nunca inventes respuestas.** Es mejor decir "no estoy seguro" que dar información incorrecta.

---

## Resumen Rápido - Checklist Antes de Presentar

- [ ] Puedo explicar la diferencia entre `Field` y `model_validator`
- [ ] Sé cuándo usar `mode='before'` vs `mode='after'`
- [ ] Puedo mostrar cómo Pydantic valida modelos anidados
- [ ] He ejecutado los 3 ejercicios sin errores
- [ ] Tengo respuestas para las 4 preguntas típicas
- [ ] Sé preparar una demo en vivo cambiando valores
- [ ] Conozco los errores comunes y cómo evitarlos