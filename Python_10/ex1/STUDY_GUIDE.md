# Study Guide: Higher-Order Functions in Python

## Nivel
**Principiante / Intermedio**

---

## Tema principal
**Funciones de orden superior y funciones como ciudadanos de primera clase**

---

## Código de referencia

```python
from collections.abc import Callable


SpellType = Callable[[str, int], str]


def spell_combiner(
    spell1: SpellType,
    spell2: SpellType
) -> Callable[[str, int], tuple[str, str]]:
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: SpellType, multiplier: int) -> SpellType:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: SpellType, spell: SpellType) -> SpellType:
    def conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return conditional


def spell_sequence(
    spells: list[SpellType]
) -> Callable[[str, int], list[str]]:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"
```

---

## Resumen de conceptos

### ¿Qué son las funciones de orden superior?
Una función de orden superior es aquella que cumple al menos una de estas condiciones:
1. Recibe una o más funciones como argumentos
2. Devuelve una función como resultado

### Funciones como ciudadanos de primera clase
En Python, las funciones son "ciudadanos de primera clase" (first-class citizens), lo que significa que:
- Se pueden asignar a variables
- Se pueden pasar como argumentos a otras funciones
- Se pueden devolver desde otras funciones
- Se pueden almacenar en estructuras de datos (listas, diccionarios, etc.)

Esto permite un estilo de programación funcional donde las funciones son valores que pueden manipulares dinámicamente.

### Type alias paraCallable
```python
SpellType = Callable[[str, int], str]
```
`Callable[[str, int], str]` significa: una función que recibe (str, int) y devuelve str.

---

## Explicación de cada función

### spell_combiner
Recibe dos funciones de hechizo y返回一个闭包 que ejecuta ambas en secuencia. La función interna tiene acceso a `spell1` y `spell2` mediante closure.

```python
combined = spell_combiner(fireball, heal)
result = combined("Dragon", 10)  # Devuelve tuple: ("Fireball hits Dragon", "Heals Dragon")
```

### power_amplifier
Recibe una función base y un multiplicador, y devuelve una nueva función que multiplica el poder antes de llamar al hechizo original. Ejemplo de transformación de funciones.

```python
amplified = power_amplifier(fireball, 3)
result = amplified("Dragon", 10)  # Ejecuta fireball con power=30
```

### conditional_caster
Recibe una función de condición y un hechizo. Devuelve una función que solo ejecuta el hechizo si la condición es verdadera; de lo contrario devuelve "Spell fizzled".

### spell_sequence
Recibe una lista de funciones de hechizo y返回一个闭包 que ejecuta todas en orden, recolectando los resultados en una lista.

```python
sequence = spell_sequence([fireball, heal, fireball])
results = sequence("Dragon", 10)  # Lista con 3 resultados
```

---

## Guía de evaluación

### Puntos clave que debe mencionar el estudiante

1. **Definición de función de orden superior**
   - Función que toma funciones como argumento o devuelve funciones

2. **Ciudadanos de primera clase**
   - Las funciones en Python se pueden asignar, pasar y retornar

3. **Closure**
   - Las funciones internas capturan variables del scope exterior (`spell1`, `spell2`, `base_spell`, etc.)

4. **Type alias con Callable**
   - `SpellType = Callable[[str, int], str]` define un tipo reusable para referenciar firmas de función

5. **Decoradores**
   - Estas funciones son la base conceptual de los decoradores en Python

6. **Transformación de funciones**
   - Las funciones de orden superior permiten crear nuevas funciones a partir de existentes sin modificar las originales

7. **List comprehensions en funciones**
   - `spell_sequence` usa `[spell(target, power) for spell in spells]`

---

## Preguntas de evaluación

### 1. ¿Qué define a una función de orden superior? Da un ejemplo del archivo.

**Respuesta:** Una función de orden superior es aquella que recibe funciones como parámetro o devuelve una función. En el archivo, `power_amplifier` recibe `base_spell: SpellType` y devuelve `amplified`, una nueva función. `spell_combiner` recibe dos funciones y devuelve una tercera.

---

### 2. ¿Qué es un closure y cómo se usa en este código?

**Respuesta:** Un closure ocurre cuando una función interna captura variables del scope donde fue definida. En `spell_combiner`, la función `combined` captura `spell1` y `spell2`. Cuando `spell_combiner` termina, `combined` sigue teniendo acceso a esas variables. Esto permite crear funciones con "memoria" del contexto donde fueron creadas.

---

### 3. Explica qué hace `SpellType = Callable[[str, int], str]` y por qué es útil.

**Respuesta:** Define un alias de tipo donde `SpellType` representa cualquier función que reciba un `str` y un `int`, y devuelva un `str`. Es útil para reutilizar la firma de función en múltiples lugares (`spell_combiner`, `power_amplifier`, etc.), mejorando la legibilidad y permitiendo verificación de tipos con mypy.

---

### 4. ¿Qué diferencia hay entre `spell_combiner` y `spell_sequence`?

**Respuesta:** `spell_combiner` recibe exactamente dos funciones y devuelve una tupla de dos resultados. `spell_sequence` recibe una lista de funciones (puede ser cualquier cantidad) y devuelve una lista con todos los resultados. `spell_combiner` tiene firma fija, `spell_sequence` tiene firma variable.

---

### 5. ¿Cómo funciona `power_amplifier`? Explica el flujo de ejecución.

**Respuesta:** Se llama `power_amplifier(fireball, 3)` que devuelve la función `amplified`. Cuando se llama `amplified("Dragon", 10)`, internamente ejecuta `base_spell(target, power * multiplier)` = `fireball("Dragon", 30)`. El resultado es aplicar el triple de poder al hechizo original, sin modificar la función `fireball` original.

---

### 6. ¿Qué sucede en `conditional_caster` si la condición devuelve False?

**Respuesta:** La función interna `conditional` evalúa `if condition(target, power)`. Si devuelve `False`, no ejecuta el hechizo sino que retorna la cadena `"Spell fizzled"`. El hechizo original nunca se llama en ese caso.

---

### 7. ¿Cómo se relaciona este código con el patrón decorador?

**Respuesta:** `power_amplifier` es conceptualmente similar a un decorador: envolvemos una función (`base_spell`) con lógica adicional (multiplicar poder) y devolvemos una nueva función. En un decorador con `@`, sería `@power_amplifier(multiplier=3)`. El closure permite "envolver" la función original sin modificarla.

---

## Ejercicios de práctica sugeridos

1. Crear una función `spell_filter` que reciba una lista de hechizos y un predicado, devolviendo solo los hechizos que cumplan la condición.

2. Modificar `spell_combiner` para aceptar cualquier número de hechizos usando `*args`.

3. Implementar un `spell_delay` que aplique un retardo multiplicativo al poder (similar a `power_amplifier` pero restando en lugar de multiplicando).

4. Crear un `spell_reverser` que invierta el orden de ejecución de una lista de hechizos.