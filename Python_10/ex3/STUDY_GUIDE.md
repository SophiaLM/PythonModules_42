# Study Guide: Módulo functools

**Nivel:** Intermedio/Avanzado  
**Tema principal:** Módulo functools de Python  
**Archivos de referencia:** `functools_artifacts.py`

---

## 1. Resumen de Conceptos

### functools.reduce

`functools.reduce(function, iterable[, initializer])` aplica una función acumulativa a elementos de un iterable, reduciéndolos a un único valor.

**Casos de uso:**
- Operar sobre una lista para producir un solo resultado (suma, producto, máximo, mínimo)
- Transformar estructuras de datos
- Implementar algoritmos que procesan secuencialmente

```python
from functools import reduce
import operator

result = reduce(operator.add, [1, 2, 3, 4])  # 10
```

---

### functools.partial

`functools.partial(func, *args, **keywords)` crea una nueva función con algunos argumentos predefinidos.

**Casos de uso:**
- Preconfigurar funciones con parámetros fijos
- Crear callbacks especializados
- Componer funciones de orden superior

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(5))  # 25
```

---

### functools.lru_cache

Decorador que implementa memorización (memoización) usando el algoritmo Least Recently Used (LRU).

**Casos de uso:**
- Optimizar funciones recursivas (evitar cálculos重复)
- Cachear resultados de operaciones costosas
- Evitar llamadas redundantes a APIs o bases de datos

**Parámetros:**
- `maxsize`: Número máximo de entradas en cache (`None` = ilimitado)
- `typed`: Si `True`, distingue tipos (ej: `5` y `5.0` son distintos)

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(x):
    return x * x
```

---

### functools.singledispatch

Decorador que convierte una función en un dispatcher genérico basado en el tipo del primer argumento.

**Casos de uso:**
- Implementar polimorfismo
- Manejar diferentes tipos de datos con una sola interfaz
- Reemplazar series de `isinstance()`/`type()` con patrones más limpios

```python
from functools import singledispatch

@singledispatch
def process(arg):
    return f"Unknown: {arg}"

@process.register(int)
def _(arg):
    return f"Integer: {arg}"

@process.register(str)
def _(arg):
    return f"String: {arg}"
```

---

## 2. Guía de Evaluación

El estudiante debe ser capaz de:

| Concepto | Puntos clave |
|----------|--------------|
| **reduce** | Firma, necesidad de initializer, función binaria requerida, orden de evaluación |
| **partial** | Creación de funciones parciales, combinación con otras funciones (como reduce), preconfiguración |
| **lru_cache** | Decorador, memorización, parámetros maxsize/typed, que funciones puras son ideales |
| **singledispatch** | Decorador, registro de tipos, firma de funciones registradas, fallback default |

---

## 3. Código de Referencia

```python
import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    def max_op(a: int, b: int) -> int:
        return a if a > b else b

    def min_op(a: int, b: int) -> int:
        return a if a < b else b

    operations: dict[str, Callable[[list[int]], int]] = {
        'add': functools.partial(functools.reduce, operator.add),
        'multiply': functools.partial(functools.reduce, operator.mul),
        'max': functools.partial(functools.reduce, max_op),
        'min': functools.partial(functools.reduce, min_op)
    }
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    return operations[operation](spells)


EnchantFunc = Callable[..., str]


def partial_enchanter(
    base_enchantment: EnchantFunc
) -> dict[str, Callable[[str], str]]:
    fire = functools.partial(base_enchantment, power=50, element='fire')
    ice = functools.partial(base_enchantment, power=50, element='ice')
    ltn = functools.partial(base_enchantment, power=50, element='lightning')
    return {'fire': fire, 'ice': ice, 'lightning': ltn}


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


@functools.singledispatch
def spell_dispatcher(arg: Any) -> str:
    return "Unknown spell type"


@spell_dispatcher.register
def _(arg: int) -> str:
    return f"Damage spell: {arg} damage"


@spell_dispatcher.register
def _(arg: str) -> str:
    return f"Enchantment: {arg}"


@spell_dispatcher.register(list)
def _(_arg: list) -> str:
    return f"Multi-cast: {len(_arg)} spells"


def base_enchantment(power: int, element: str, target: str) -> str:
    return f"{element} enchantment with {power} power on {target}"


if __name__ == "__main__":
    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTesting spell dispatcher...")
    print(spell_dispatcher(42))
    print(spell_dispatcher("fireball"))
    print(spell_dispatcher(["spell1", "spell2", "spell3"]))
    print(spell_dispatcher(3.14))
```

---

## 4. Preguntas y Respuestas

### Pregunta 1: ¿Qué hace `functools.reduce` y qué tipo de función debe recibir como primer argumento?

**Respuesta:** `functools.reduce` aplica una función binaria (que recibe dos argumentos) acumulativamente a los elementos de un iterable, reduciéndolos a un único valor. La función debe aceptar dos argumentos: un acumulador y el siguiente elemento de la secuencia. Opcionalmente puede recibir un initializer como tercer argumento que proporciona el valor inicial del acumulador.

---

### Pregunta 2: En el código, ¿por qué se usa `functools.partial` dentro de `spell_reducer`?

**Respuesta:** Se usa `partial` para crear versiones especializadas de `reduce` preconfiguradas con diferentes operaciones. `'add': functools.partial(functools.reduce, operator.add)` crea una función que aplica `reduce` con `operator.add`. Esto permite almacenar diferentes operaciones en un diccionario y aplicarlas dinámicamente según el parámetro `operation` recibido.

---

### Pregunta 3: ¿Cuál es la ventaja de `@lru_cache` en la función `memoized_fibonacci` y cómo mejora la complejidad?

**Respuesta:** Sin cache, Fibonacci recursivo tiene complejidad exponencial O(2^n) porque recalcula los mismos valores múltiples veces. Con `@lru_cache`, cada resultado se almacena; llamadas futuras con el mismo argumento retornan el valor cacheado instantáneamente. Esto reduce la complejidad a O(n), convirtiendo recursion en un proceso lineal.

---

### Pregunta 4: ¿Qué significa `maxsize=None` en `@lru_cache`?

**Respuesta:** Indica que el cache no tiene límite de tamaño. Se almacenarán todos los resultados calculados. Para funciones con argumentos ilimitados, esto puede consumir memoria excesiva; en tales casos, conviene especificar un `maxsize` numérico para limitar el cache.

---

### Pregunta 5: ¿Cómo funciona `@singledispatch` en `spell_dispatcher`?

**Respuesta:** `singledispatch` permite que una función maneje diferentes tipos de manera polimórfica. La función decorada (`spell_dispatcher`) es el dispatcher default que maneja tipos no registrados. Los `@spell_dispatcher.register` decoran funciones especializadas para tipos específicos. Cuando se llama `spell_dispatcher(arg)`, Python busca la implementación del tipo de `arg` en orden de MRO (Method Resolution Order).

---

### Pregunta 6: ¿Por qué `spell_dispatcher(3.14)` retorna "Unknown spell type"?

**Respuesta:** Porque no existe un registro para `float`. La función base decorada con `@singledispatch` actúa como fallback cuando el tipo del argumento no tiene una implementación registrada. Como `3.14` es `float` y solo se registraron manejadores para `int`, `str` y `list`, se ejecuta la implementación default.

---

### Pregunta 7: ¿Cuál es la diferencia entre usar `functools.partial` con funciones de operadores vs. lambdas?

**Respuesta:** `functools.partial` es preferible por: (1) Mayor legibilidad al reutilizar operadores existentes en lugar de escribir lambdas, (2) Mejor rendimiento ya que `operator.add` está implementado en C, (3) Funciona correctamente con herramientas de tipado estático, (4) Composable con otros constructores como `reduce`. Sin embargo, `partial` tiene limitaciones con funciones variádicas y no puede preconfigurar argumentos posicionales intermedios.