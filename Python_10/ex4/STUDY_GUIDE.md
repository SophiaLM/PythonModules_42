# STUDY GUIDE: Decoradores y Métodos Estáticos en Python

**Nivel:** Avanzado
**Tema principal:** Decoradores y métodos estáticos

---

## Código de Referencia

```python
import functools
import time
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result
    return wrapper


def power_validator(
    min_power: int
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if 'power' in kwargs:
                power = kwargs['power']
            elif len(args) >= 3 and isinstance(args[2], int):
                power = args[2]
            elif len(args) >= 1 and isinstance(args[0], int):
                power = args[0]
            else:
                return "Insufficient power for this spell"
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(
    max_attempts: int
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print("Spell failed, retrying...")
                    else:
                        return "Spell casting failed"
            return "Spell casting failed"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return all(c.isalpha() or c.isspace() for c in name)

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball(power: int) -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(3)
def failing_spell() -> str:
    raise Exception("Spell failed!")


@spell_timer
def waagh() -> str:
    time.sleep(0.001)
    return "Waaaaaaagh spelled !"
```

---

## 1. Resumen de Conceptos

### ¿Qué son los decoradores?

Un decorador es una función que toma otra función como argumento y extiende su comportamiento sin modificar explícitamente su código. Se utiliza la sintaxis `@decorator` sobre la función a decorar. El decorador envuelve la función original en una función wrapper que puede ejecutar código antes y después de la función original, o modificar sus argumentos y resultado.

En el código de referencia:
- `spell_timer` mide el tiempo de ejecución de una función
- `retry_spell` reintenta ejecutar una función si falla
- `power_validator` valida parámetros antes de ejecutar la función

### functools.wraps

El módulo `functools` de Python proporciona la función `wraps` que se utiliza como decorador dentro del wrapper para copiar los atributos de la función original (`__name__`, `__doc__`, `__annotations__`, etc.) al wrapper. Esto es crucial para:
- Mantener el nombre correcto de la función cuando se usa `func.__name__`
- Preservar la documentación de la función original
- Evitar problemas con herramientas de introspección como `inspect`

### Decoradores Factory (Decoradores con parámetros)

Los decoradores factory son funciones que retornan un decorador. Permiten pasar parámetros al decorador. Su estructura es:
1. Una función externa que recibe los parámetros de configuración
2. Una función decoradora interna que recibe la función a decorar
3. Un wrapper que implementa la lógica adicional

En el código:
- `power_validator(min_power)` recibe `min_power` y retorna el decorador
- `retry_spell(max_attempts)` recibe `max_attempts` y retorna el decorador
- `spell_timer` no es un factory porque no recibe parámetros adicionales

### @staticmethod vs métodos de instancia

**@staticmethod:**
- No recibe `self` como primer parámetro
- Se puede llamar directamente desde la clase `Clase.metodo()` sin crear una instancia
- No tiene acceso a la instancia ni a la clase
- Se usa para funcionalidad relacionada con la clase pero que no necesita acceder a sus atributos

**Métodos de instancia:**
- Reciben `self` como primer parámetro
- Requieren una instancia de la clase para llamarse `instancia.metodo()`
- Tienen acceso a todos los atributos y métodos de la instancia

En el código de referencia:
- `validate_mage_name` es un `@staticmethod` que valida nombres sin necesidad de una instancia
- `cast_spell` es un método de instancia que usa el decorador `@power_validator(10)` y recibe `self`

---

## 2. Explicación de Cada Componente

### spell_timer
Decorador simple que envolviendo una función, imprime el nombre de la función antes de ejecutarla, mide el tiempo de ejecución con `time.perf_counter()`, y prints el tiempo requerido. Usa `functools.wraps` para preservar metadatos de la función original.

### power_validator
Decorador factory que recibe `min_power` como parámetro. Examina los argumentos de tres maneras diferentes: primero busca `power` en kwargs, luego verifica si hay un tercer argumento posicional que sea un entero, y finalmente verifica si el primer argumento es un entero. Si el power es menor al mínimo, retorna un mensaje de error; de lo contrario, ejecuta la función.

### retry_spell
Decorador factory que reintenta ejecutar la función hasta `max_attempts` veces. Itera en un rango y captura cualquier excepción. Si falla, imprime un mensaje de reintento; si agota los intentos, retorna un mensaje de error.

### MageGuild
Clase que contiene:
- `validate_mage_name`:staticmethod que valida que el nombre tenga al menos 3 caracteres y solo contenga letras o espacios
- `cast_spell`: método de instancia decorado con `@power_validator(10)` que valida que el poder sea al menos 10

---

## 3. Guía de Evaluación

El estudiante debe ser capaz de:

1. **Identificar decoradores simples vs factory**: Reconocer cuándo un decorador recibe parámetros (factory) y cuándo no.

2. **Explicar functools.wraps**: Describir por qué es importante y qué problema resuelve.

3. **Comprender el flujo de ejecución**: Explicar cómo los decoradores modifican el comportamiento de las funciones sin cambiar su código fuente.

4. **Diferenciar @staticmethod de métodos de instancia**: Saber cuándo usar cada uno y sus diferencias técnicas.

5. **Analizar decoradores con parámetros**: Entender cómo los decoradores factory reciben configuración y cómo se aplican múltiples decoradores.

6. **Rastrear la ejecución**: Seguir el flujo de datos a través de decoradores anidados o múltiples.

---

## 4. Preguntas de Evaluación

### Pregunta 1
**¿Cuál es la diferencia fundamental entre un decorador simple y un decorador factory?**

Un decorador simple toma solo la función a modificar como argumento (como `spell_timer`), mientras que un decorador factory es una función que recibe parámetros de configuración y retorna un decorador (como `power_validator(min_power)` y `retry_spell(max_attempts)`). El factory permite personalizar el comportamiento del decorador para cada función que decora.

### Pregunta 2
**¿Por qué es importante usar `@functools.wraps(func)` dentro del wrapper?**

`@functools.wraps` copia los atributos de la función original (nombre, documentación, módulo, etc.) al wrapper. Sin esto, herramientas como `help()`, `inspect`, y depuradores mostrarán incorrectamente el nombre del wrapper en lugar de la función original. También permite que `func.__name__` dentro del wrapper devuelva el nombre real de la función decorada.

### Pregunta 3
**¿Qué sucede cuando se ejecuta `MageGuild.validate_mage_name("AB")`?**

Se llama al método estático `validate_mage_name` sin crear una instancia de `MageGuild`. Como "AB" tiene solo 2 caracteres, la condición `len(name) < 3` es verdadera, por lo que retorna `False`. El método funciona correctamente porque los métodos estáticos pueden llamarse directamente desde la clase.

### Pregunta 4
**Explica el orden de ejecución cuando se llama `guild.cast_spell("Lightning", 15)`**

Primero, `power_validator(10)` retorna un decorador que envolvió a `cast_spell`. Cuando se llama el método:
1. El wrapper de `power_validator` recibe los argumentos
2. Extrae el valor de `power` del tercer argumento posicional (15)
3. Compara: ¿15 >= 10? Sí
4. Ejecuta la función original `cast_spell` con los argumentos
5. Retorna el resultado: "Successfully cast Lightning with 15 power"

### Pregunta 5
**¿Qué retorna `failing_spell()` y por qué?**

Retorna "Spell casting failed" porque:
1. `@retry_spell(3)` crea un wrapper que intenta ejecutar `failing_spell` hasta 3 veces
2. En el primer intento, la función lanza una excepción
3. El wrapper la captura e intenta de nuevo (intento 2 y 3)
4. Después del tercer fallo, retorna el mensaje de error en lugar de volver a lanzar la excepción

### Pregunta 6
**¿Cómo modifica `power_validator` el comportamiento de la función decorada?**

El decorador intercepta la llamada a la función y verifica el valor de `power` antes de ejecutar la función original. Si `power` es menor al mínimo, retorna un mensaje de error sin ejecutar la función. Esto añade validación de parámetros sin modificar el código de la función decorada, siguiendo el principio de開放/cierre (open/closed principle).

### Pregunta 7
**¿Por qué `cast_spell` puede usar `@power_validator(10)` siendo un método de instancia?**

Los decoradores funcionan igual con métodos de instancia que con funciones normales. El wrapper recibe `self` como parte de `*args`. Cuando se aplica `@power_validator(10)` a `cast_spell`, el decorador se ejecuta en tiempo de definición de la clase y el método decorado queda disponible para todas las instancias de `MageGuild`. El `self` se pasa normalmente a través de los argumentos posicionales.

---

## 5. Ejemplo de Uso

```python
from decorator_mastery import MageGuild, spell_timer, retry_spell, power_validator

@spell_timer
def nuevo_hechizo() -> str:
    return "Nuevo hechizo!"

guild = MageGuild()

print(MageGuild.validate_mage_name("Gandalf"))
print(guild.cast_spell("Fire", 20))
print(guild.cast_spell("Fire", 5))

nuevo_hechizo()
```