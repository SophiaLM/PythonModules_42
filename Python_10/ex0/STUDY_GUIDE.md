# Guía de Estudio: Expresiones Lambda en Python

**Nivel**: Principiante
**Tema principal**: Programación funcional con lambdas

---

## Resumen de Conceptos

Las **expresiones lambda** son funciones anónimas pequeñas y precisas que se definen con la palabra clave `lambda`. Permiten crear funciones simples sin necesidad de definirlas con `def`. Son especialmente útiles cuando se necesitan funciones pequeñas para usar como argumentos de otras funciones como `map()`, `filter()`, `sorted()`, entre otras.

### ¿Por qué son útiles?
- Permiten escribir código más conciso y legible
- Evitan crear funciones completas para operaciones simples
- Se usan frecuentemente con funciones de orden superior
- Ideales para transformaciones rápidas de datos

---

## Código de Referencia

```python
from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(
    mages: list[dict[str, Any]],
    min_power: int
) -> list[dict[str, Any]]:
    return list(filter(lambda x: x['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    powers = list(map(lambda x: x['power'], mages))
    return {
        'max_power': max(powers),
        'min_power': min(powers),
        'avg_power': round(sum(powers) / len(powers), 2)
    }
```

---

## Explicación de Cada Función

### 1. artifact_sorter(artifacts)
Ordena una lista de diccionarios por la clave `'power'` en orden descendente (de mayor a menor). Utiliza `sorted()` con una función lambda como criterio de ordenamiento.

**Retorna**: Lista de artefactos ordenados por poder

### 2. power_filter(mages, min_power)
Filtra una lista de magos dejando solo aquellos cuyo poder sea mayor o igual al valor mínimo especificado. Utiliza `filter()` con una lambda que evalúa la condición.

**Retorna**: Lista de magos que cumplen el criterio

### 3. spell_transformer(spells)
Transforma cada hechizo agregando un formato con asteriscos al principio y al final. Utiliza `map()` para aplicar la transformación a cada elemento.

**Retorna**: Lista de hechizos formateados

### 4. mage_stats(mages)
Calcula estadísticas de poder de una lista de magos: el poder máximo, el poder mínimo y el promedio. Usa `map()` para extraer los valores de poder, luego `max()`, `min()`, `sum()` y `len()` para calcular las estadísticas.

**Retorna**: Diccionario con max_power, min_power y avg_power

---

## Guía de Evaluación

El estudiante debe ser capaz de:

1. **Identificar lambdas**: Reconocer la sintaxis `lambda x: expresion` en el código
2. **Explicar propósito de cada función**: Describir qué hace cada una de las cuatro funciones
3. **Relacionar lambda con funciones de orden superior**: Entender cómo lambda se combina con `map`, `filter`, `sorted`, `max`, `min`, `sum`, `len`
4. **Analizar comportamiento**: Predecir el resultado de cada función con datos de entrada específicos
5. **Aplicar conceptos**: Modificar o crear nuevas funciones usando lambdas

---

## Preguntas de Evaluación

### Pregunta 1
**¿Qué es una expresión lambda y cuál es su sintaxis básica en Python?**

Una expresión lambda es una función anónima y pequeña que se define sin usar la palabra clave `def`. Su sintaxis básica es: `lambda parametros: expresion`. Por ejemplo, `lambda x: x * 2` toma un parámetro `x` y retorna el doble de su valor. A diferencia de una función definida con `def`, las lambdas están limitadas a una sola expresión y no pueden contener múltiples sentencias.

---

### Pregunta 2
**¿Cuál es la diferencia entre `map()` y `filter()`? Ilustre con ejemplos del código.**

`map()` transforma cada elemento de una secuencia aplicando una función y retorna una nueva secuencia del mismo tamaño. En `spell_transformer`, `map()` convierte cada hechizo en uno formateado con asteriscos.

`filter()` selecciona elementos de una secuencia que cumplen una condición y retorna una nueva secuencia con menos elementos (o igual si todos cumplen). En `power_filter`, `filter()` selecciona solo los magos con poder >= min_power.

La diferencia fundamental: `map()` siempre mantiene la cantidad de elementos, solo los transforma; `filter()` puede reducir la cantidad de elementos según un criterio.

---

### Pregunta 3
**En la función `artifact_sorter`, explique el papel de los parámetros `key` y `reverse` en `sorted()`.**

El parámetro `key` recibe una función que define el criterio de ordenamiento. En este caso, `lambda x: x['power']` indica que el orden se basa en el valor de la clave `'power'` de cada diccionario.

El parámetro `reverse=True` invierte el orden predeterminado (ascendente) a descendente, haciendo que los artefactos con mayor poder aparezcan primero.

Sin `reverse=True`, los artefactos se ordenarían del menor al mayor poder; con `reverse=True`, se ordenan del mayor al menor.

---

### Pregunta 4
**En `mage_stats`, ¿qué operaciones se realizan sobre la lista `powers` extraída con `map()`?**

Se realizan cuatro operaciones:

- `list(map(lambda x: x['power'], mages))`: Extrae los valores de 'power' de cada mago en una lista
- `max(powers)`: Encuentra el valor máximo de la lista
- `min(powers)`: Encuentra el valor mínimo de la lista
- `sum(powers) / len(powers)`: Calcula el promedio (suma dividida por cantidad de elementos)

Finalmente, `round(..., 2)` redondea el promedio a dos decimales.

---

### Pregunta 5
**¿Por qué es necesario convertir el resultado de `filter()` y `map()` a lista con `list()`?**

En Python 3, `filter()` y `map()` retornan objetos iteradores (de tipo `filter` y `map`), no listas. Estos iteradores son "perezosos": calculan los valores bajo demanda y no almacenan todos los resultados en memoria de inmediato.

Para obtener los valores como una lista exploable, es necesario convertir el iterador con `list()`. Si no se convierte, al intentar acceder a los elementos o imprimirlos directamente, no se verá el contenido esperado.

---

### Pregunta 6
**Si ejecutamos `artifact_sorter` con los artefactos del ejemplo, ¿cuál sería el primer resultado y por qué?**

El primer resultado sería `{'name': 'Fire Staff', 'power': 92, 'type': 'weapon'}`.

Esto ocurre porque:
- La función usa `sorted()` con `key=lambda x: x['power']`, ordenando por el valor de 'power'
- Con `reverse=True`, el orden es descendente (mayor a menor)
- De los tres artefactos (92, 85, 78), el de mayor poder es 'Fire Staff' con 92
- Por lo tanto, aparece en la primera posición

---

### Pregunta 7
**¿Cómo modificaría la función `spell_transformer` para que el formato sea diferente, por ejemplo usando corchetes en lugar de asteriscos?**

Simplemente se modificaría la expresión lambda para usar corchetes:

```python
def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"[{x}]", spells))
```

La lambda `lambda x: f"[{x}]"` envuelve cada hechizo entre corchetes. Si los spells son `['fireball', 'heal', 'shield']`, el resultado sería `['[fireball]', '[heal]', '[shield]']`.

Esto demuestra que la lambda puede modificarse fácilmente para cambiar el formato de transformación.

---

## Respuestas Rápidas

| Pregunta | Respuesta Clave |
|----------|-----------------|
| 1 | Función anónima con sintaxis `lambda x: expresión` |
| 2 | `map()` transforma; `filter()` selecciona según condición |
| 3 | `key` define el criterio de orden; `reverse=True` invierte el orden |
| 4 | Extraer con map, luego max/min/sum/len para estadísticas |
| 5 | Retornan iteradores, no listas; se necesita `list()` para materializarlos |
| 6 | Fire Staff con power 92 (mayor, orden descendente) |
| 7 | Cambiar la lambda: `lambda x: f"[{x}]"` |