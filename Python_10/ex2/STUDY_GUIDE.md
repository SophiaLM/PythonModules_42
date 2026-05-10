# Guía de Estudio: Closures y Lexical Scoping

**Nivel:** Intermedio/Avanzado  
**Tema Principal:** Closures y lexical scoping en Python

---

## 1. Resumen de Conceptos

### ¿Qué es un Closure?

Un **closure** es una función anidada que captura y recuerda el entorno donde fue definida. Este entorno incluye las variables locales del ámbito externo, incluso después de que la función externa haya terminado su ejecución.

### ¿Qué es Lexical Scoping?

El **lexical scoping** (scope léxico) determina cómo se resuelven los nombres de variables según la estructura estática del código, no la llamada dinámica. Python utiliza lexical scoping, lo que significa que una función anidada puede acceder a variables de su función padre porque el ámbito se define por la ubicación física del código, no por el orden de ejecución.

### ¿Cómo mantienen estado sin variables globales?

Las closures permiten **encapsular estado privado** sin necesidad de:
- Variables globales
- clases
- atributos de instancia

La clave es que las variables se almacenan en el **alcance envolvente** de la función interna. Cada llamada a la función externa crea un nuevo entorno léxico, dando como resultado instancias independientes.

### Mecanismo de captura (Free Variables)

Cuando una función interna referencia una variable de la función externa, esa variable se convierte en una **free variable**. El closure captura una referencia al ámbito externo, no una copia del valor. Por eso, modificaciones en variables mutables (como listas) persisten entre llamadas.

---

## 2. Código de Referencia

```python
from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count = [0]

    def counter() -> int:
        count[0] += 1
        return count[0]
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total = [initial_power]

    def accumulator(amount: int) -> int:
        total[0] += amount
        return total[0]
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchantment


StoreFunc = Callable[[str, str], None]
RecallFunc = Callable[[str], str]


def memory_vault() -> dict[str, Callable[..., Any]]:
    storage: dict[str, str] = {}

    def store(key: str, value: str) -> None:
        storage[key] = value

    def recall(key: str) -> str:
        return storage.get(key, "Memory not found")
    return {'store': store, 'recall': recall}
```

---

## 3. Explicación de Cada Función

### mage_counter()

**Propósito:** Crear un contador que mantiene estado entre llamadas.

**Mecanismo:**
- `count = [0]` crea una lista mutable para almacenar el estado
- La función interna `counter` cierra sobre `count`
- Cada invocación incrementa el valor y lo retorna

**Salida esperada:**
```
counter_a call 1: 1
counter_a call 2: 2
counter_b call 1: 1
```

**Punto clave:** `counter_a` y `counter_b` son independientes porque `mage_counter()` se llamó dos veces, creando dos entornos léxicos distintos.

---

### spell_accumulator(initial_power: int)

**Propósito:** Crear un acumulador que suma valores a partir de una potencia inicial.

**Mecanismo:**
- `total = [initial_power]` inicializa el estado con el valor proporcionado
- La función interna acumula sobre `total[0]`

**Salida esperada:**
```
Base 100, add 20: 120
Base 100, add 30: 150
```

**Punto clave:** El parámetro `initial_power` se captura en el closure, permitiendo configuración inicial por instancia.

---

### enchantment_factory(enchantment_type: str)

**Propósito:** Generar funciones de encantamiento especializadas según el tipo.

**Mecanismo:**
- `enchantment_type` se captura por valor en el closure
- Cada función retornada mantiene el tipo específico

**Salida esperada:**
```
Flaming Sword
Frozen Shield
```

**Punto clave:** El parámetro se "fija" en cada instancia, permitiendo crear múltiples variantes especializadas.

---

### memory_vault()

**Propósito:** Crear un mini-sistema de almacenamiento clave-valor con operaciones store y recall.

**Mecanismo:**
- `storage` es un diccionario privado compartido entre `store` y `recall`
- Retorna un diccionario con las funciones closures
- `recall` usa `.get()` para manejar claves inexistentes

**Salida esperada:**
```
Store 'secret' = 42
Recall 'secret': 42
Recall 'unknown': Memory not found
```

**Punto clave:** El closure permite múltiples funciones que comparten estado privado, imitando el patrón de módulos con encapsulación.

---

## 4. Guía de Evaluación

El estudiante debe demostrar comprensión de los siguientes puntos:

| Concepto | Peso | Indicador de dominio |
|----------|------|---------------------|
| Definición de closure | 15% | Explica que es una función que recuerda su entorno |
| Lexical scoping | 20% | Describe cómo el scope se determina por la ubicación física del código |
| Estado persistente | 20% | Explica cómo las closures mantienen estado entre llamadas |
| Independencia de instancias | 15% | Demuestra que cada llamada crea un nuevo closure |
| Uso de variables mutables | 15% | Explica por qué se usan listas/diccionarios en lugar de enteros/dict simples |
| Captura de parámetros | 10% | Reconoce que los parámetros de la función externa se incluyen en el closure |
| Aplicaciones prácticas | 5% | Menciona casos de uso como factories, contadores, encapsulación |

---

## 5. Preguntas de Evaluación

### Pregunta 1: Concepto Fundamental

**¿Qué es un closure y cómo se diferencia de una función normal?**

Un closure es una función anidada que conserva acceso a las variables de su ámbito envolvente incluso después de que la función externa haya terminado. A diferencia de una función normal que solo tiene acceso a sus parámetros y variables globales, un closure captura variables no locales en el momento de su definición, permitiendo estado persistente sin variables globales ni clases.

---

### Pregunta 2: Lexical Scoping

**Explica qué significa lexical scoping y cómo afecta la resolución de variables en closures.**

Lexical scoping significa que el alcance de una variable se determina por su ubicación física en el código fuente, no por el orden de ejecución. En closures, esto implica que una función interna puede acceder a variables de la función padre porque el intérprete busca en el ámbito donde la función fue definida, no donde se ejecuta. Cuando Python busca una variable libre, la encuentra en el ámbito léxico envolvente que existía cuando se creó el closure.

---

### Pregunta 3: Estado Mutable

**¿Por qué se usa `count = [0]` en lugar de `count = 0` en `mage_counter()`? ¿Qué pasaría con cada alternativa?**

Se usa una lista porque Python no permite modificar variables no locales desde una función anidada sin `nonlocal` (y en algunos contextos esto es restrictivo). Con `count = 0` (entero inmutable), al hacer `count += 1` se crearía una nueva variable local, no se modificarían los datos capturados. Con `count = [0]`, se modifica el contenido de la lista (mutable) sin reasignar la variable, permitiendo que el closure vea los cambios. Alternativamente, podría usarse `nonlocal count` con un entero.

---

### Pregunta 4: Independencia de Instancias

**Si ejecutamos:**
```python
counter_a = mage_counter()
counter_b = mage_counter()
counter_a(); counter_a()
counter_b()
```
**¿Qué valores se retornan? Explica por qué son independientes.**

Se retornan: `counter_a()` = 1, `counter_a()` = 2, `counter_b()` = 1. Son independientes porque cada llamada a `mage_counter()` crea un nuevo entorno léxico con su propia variable `count`. `counter_a` y `counter_b` no comparten estado; son closures separados sobre variables distintas. Esto demuestra que las closures proporcionan encapsulación de instancia similar a objetos.

---

### Pregunta 5: Factory Pattern

**Describe cómo `enchantment_factory` implementa el patrón Factory. ¿Qué ventajas tiene este enfoque?**

`enchantment_factory` es una factory function que genera funciones especializadas según el argumento. Recibe el tipo de encantamiento y retorna una función que aplica ese tipo a cualquier nombre de ítem. Ventajas: evita código duplicado, permite crear múltiples variantes fácilmente, separa la configuración de la ejecución, y usa closures para encapsular parámetros sin clases.

---

### Pregunta 6: Múltiples Funciones Compartiendo Estado

**En `memory_vault()`, las funciones `store` y `recall` comparten `storage`. Explica cómo funciona esto y qué patrón demuestra.**

Ambas funciones cierran sobre la misma variable `storage` (diccionario). Cuando se retorna el diccionario `{'store': store, 'recall': recall}`, ambas funciones mantienen referencia al mismo diccionario. Esto demuestra que un closure puede crear múltiples funciones que comparten estado privado, emulando el patrón módulo/Meyer singleton. El estado es inaccesible desde fuera excepto a través de estas funciones, proporcionando encapsulación.

---

### Pregunta 7: Captura de Parámetros

**¿Qué ocurre con los parámetros de la función externa cuando se retorna la función interna? ¿Se capturan por referencia o por valor?**

Los parámetros (como `initial_power`, `enchantment_type`) se capturan por referencia al ámbito. Sin embargo, como son inmutables (strings, enteros), el efecto es similar a capturar por valor. Si el parámetro fuera mutable y se modificara, el closure vería esos cambios porque mantiene una referencia al ámbito. En `enchantment_factory("Flaming")`, el string "Flaming" queda fijo en el closure, permitiendo que cada instancia tenga su propio tipo de encantamiento sin posibilidad de interferencia entre instancias.

---

## Resumen Rápido de Puntos Clave

1. **Closure** = función interna + entorno léxico capturado
2. **Lexical scoping** = scope determinado por ubicación física del código
3. **Estado mutable** = usar listas/diccionarios para modificar dentro del closure
4. **Instancias independientes** = cada llamada a la factory crea un nuevo entorno
5. **Encapsulación** = estado privado accesible solo via funciones closure
6. **Factory pattern** = funciones que crean y retornan otras funciones configuradas

---

*Documento generado para estudio de Closures y Lexical Scoping*