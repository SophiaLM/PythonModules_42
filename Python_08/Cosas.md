# The Matrix — Guía de Estudio (Español)

> *"Bienvenido al mundo real."* — Morpheus

Esta guía resume los conceptos clave del módulo y anticipa las preguntas difíciles que puede hacer un evaluador.

---

## Conceptos clave por ejercicio

---

## Ejercicio 0 — Entornos virtuales

### ¿Qué es un entorno virtual?

Un entorno virtual es un directorio aislado que contiene su propia copia del intérprete Python y sus propias carpetas de paquetes. Los cambios (instalaciones, desinstalaciones) dentro del entorno **no afectan** la instalación global de Python ni a otros entornos.

### ¿Por qué son necesarios?

- **Aislamiento de dependencias**: el proyecto A puede usar `pandas==1.5` y el proyecto B `pandas==2.1` sin conflicto.
- **Reproducibilidad**: otro desarrollador (o el servidor de producción) instala exactamente las mismas versiones.
- **Seguridad**: no se necesitan permisos de root/admin para instalar paquetes.
- **Limpieza**: se puede borrar el entorno sin tocar el sistema.

### ¿Cómo se crea y activa?

```bash
python3 -m venv matrix_env          # crea la carpeta
source matrix_env/bin/activate      # activa en Unix/macOS
matrix_env\Scripts\activate         # activa en Windows
deactivate                          # desactiva
```

### ¿Cómo detectamos si estamos dentro de un venv en Python?

```python
import sys
in_venv = sys.prefix != sys.base_prefix
```

- `sys.prefix` — ruta del entorno Python actualmente activo
- `sys.base_prefix` — ruta del Python del sistema (nunca cambia)
- Si son iguales → estamos en el sistema global
- Si son distintos → estamos en un venv

### ¿Qué pasa con `VIRTUAL_ENV`?

La variable de entorno `VIRTUAL_ENV` también se puede usar, pero no siempre está definida (depende del shell). La comparación `sys.prefix != sys.base_prefix` es la forma canónica y más robusta.

### ¿Qué son `site-packages`?

Es la carpeta donde `pip` instala los paquetes. Cada entorno virtual tiene la suya propia, completamente separada del sistema. `site.getsitepackages()` devuelve la lista de rutas donde Python busca paquetes instalados.

---

## Ejercicio 1 — Gestión de dependencias: pip vs Poetry

### pip

- Herramienta **estándar** incluida con Python.
- Instala paquetes en el entorno activo.
- Las dependencias se listan en `requirements.txt`.
- **No genera lock file automáticamente** — hay que hacer `pip freeze > requirements.txt` para fijar versiones exactas.

```bash
pip install pandas numpy matplotlib
pip freeze > requirements.txt    # captura versiones exactas
pip install -r requirements.txt  # instala desde el fichero
```

### Poetry

- Herramienta de **terceros** que gestiona: venv, dependencias, empaquetado y publicación.
- Usa `pyproject.toml` (estándar PEP 518) como fichero de configuración.
- Genera automáticamente `poetry.lock` con versiones exactas de todas las dependencias transitivas.
- Separa las dependencias de producción de las de desarrollo.

```bash
poetry init            # crea pyproject.toml interactivamente
poetry add pandas      # añade dependencia
poetry add --group dev flake8  # dependencia solo de desarrollo
poetry install         # instala todo
poetry run python loading.py   # ejecuta en el entorno de Poetry
```

### Comparativa rápida

| Característica | pip | Poetry |
|---|---|---|
| Incluido en Python | ✅ | ❌ (instalar aparte) |
| Archivo de config | `requirements.txt` | `pyproject.toml` |
| Lock file automático | ❌ | ✅ `poetry.lock` |
| Gestiona el venv | ❌ (manual) | ✅ automático |
| Deps de dev separadas | ❌ | ✅ |
| Publicar en PyPI | ❌ (usar twine) | ✅ integrado |

### ¿Por qué numpy debe ser la fuente de datos?

El enunciado pide que los datos se generen con numpy (no con listas hardcodeadas ni `range()`). Esto demuestra que se entiende el propósito de numpy: operaciones vectorizadas eficientes sobre arrays numéricos.

```python
rng = np.random.default_rng(seed=42)
data = rng.standard_normal(1000)   # correcto ✅

data = list(range(1000))           # incorrecto ❌
```

### ¿Por qué se usan imports tardíos en `loading.py`?

Las importaciones de `numpy`, `pandas` y `matplotlib` se hacen **dentro de la función `run_analysis()`**, no al inicio del módulo. Esto permite que el programa arranque, compruebe las dependencias con `importlib`, e informe al usuario de qué falta — sin que el propio `import` falle y lance un `ImportError` no controlado.

```python
def run_analysis() -> None:
    import numpy as np   # solo llega aquí si check_dependencies() pasó
```

---

## Ejercicio 2 — Variables de entorno y ficheros `.env`

### ¿Qué es una variable de entorno?

Un par clave-valor definido en el sistema operativo, accesible por cualquier proceso hijo. En Python se leen con `os.environ.get("CLAVE")`.

### ¿Por qué no hardcodear secretos en el código?

1. El código va a un repositorio git → **los secretos quedan en el historial para siempre**.
2. El historial de git es casi imposible de limpiar completamente.
3. Los bots escanean GitHub/GitLab continuamente en busca de API keys expuestas.
4. Un secreto comprometido puede implicar costes económicos y legales graves.

### ¿Qué es `python-dotenv`?

Una librería que lee un fichero `.env` y carga sus pares clave=valor en `os.environ`.

```python
from dotenv import load_dotenv
load_dotenv(override=False)
# override=False → las vars ya definidas en el shell NO se sobreescriben
# override=True  → el .env tiene prioridad sobre el shell
```

### ¿Por qué `.env` debe estar en `.gitignore`?

Porque `.env` contiene secretos reales (contraseñas, API keys). El fichero **`.env.example`** actúa de plantilla segura: documenta las variables necesarias pero con valores ficticios, y sí se puede commitear.

### ¿Cuál es la prioridad de las variables?

Con `override=False` (comportamiento recomendado):

```
Variables del shell > .env file > valores por defecto en el código
```

Esto permite que en producción los secretos lleguen desde la infraestructura (variables del sistema, secretos de Kubernetes, etc.) sin necesidad de un `.env`.

### Diferencia desarrollo vs producción

| | Desarrollo | Producción |
|---|---|---|
| `MATRIX_MODE` | `development` | `production` |
| Logs | `DEBUG` (verbose) | `WARNING` o superior |
| Base de datos | local / SQLite | servidor remoto |
| `.env` | sí (en local) | no (vars del sistema) |
| Errores visibles | sí | no (van a monitorización) |

---

## Preguntas difíciles del evaluador — con respuestas

### Sobre entornos virtuales

**P: ¿Qué pasa si instalo un paquete sin activar el venv?**
R: Se instala en el Python global (o falla si no tienes permisos). El venv no lo verá.

**P: ¿Puedo tener dos venvs activos al mismo tiempo en la misma terminal?**
R: No. Activar un segundo venv desactiva el primero (modifica `$PATH` y `sys.prefix`).

**P: ¿Por qué no se debería commitear el venv al repositorio?**
R: Son miles de archivos generables en segundos con `python -m venv`. Son específicos del sistema operativo y la arquitectura. El `requirements.txt` o `pyproject.toml` ya contiene toda la información necesaria para reproducirlo.

**P: ¿`sys.prefix` y `sys.base_prefix` son siempre distintos dentro de un venv?**
R: Sí, por diseño. El módulo `venv` de Python los separa explícitamente al crear el entorno.

### Sobre pip y Poetry

**P: ¿Cuál es la diferencia entre `pip freeze` y `requirements.txt`?**
R: `pip freeze` genera la lista de todos los paquetes instalados con sus versiones exactas. Si mantienes el `requirements.txt` a mano con rangos (`>=`), puede haber diferencias. La práctica habitual es: desarrollar con rangos, hacer `pip freeze` para producción.

**P: ¿Qué es `poetry.lock` y por qué es importante?**
R: Es un fichero generado automáticamente que registra las versiones exactas de cada paquete y sus dependencias transitivas. Garantiza que `poetry install` da exactamente el mismo resultado en cualquier máquina, sin importar cuándo se ejecute.

**P: ¿Puedo usar pip y Poetry en el mismo proyecto?**
R: Técnicamente sí, pero no es recomendable. Se puede instalar con pip los paquetes definidos en `pyproject.toml` usando `pip install .`, pero mezclar los dos flujos crea confusión sobre qué versiones están instaladas realmente.

**P: ¿Por qué `importlib.metadata.version()` en lugar de acceder a `__version__`?**
R: Porque no todos los paquetes exponen `__version__`. `importlib.metadata` es el estándar oficial (PEP 566) y funciona con cualquier paquete instalado correctamente.

### Sobre variables de entorno

**P: ¿Qué diferencia hay entre `os.environ.get("KEY")` y `os.environ["KEY"]`?**
R: `.get()` devuelve `None` (o un default) si la clave no existe. `[]` lanza `KeyError`. Para variables opcionales se usa `.get()`; para variables obligatorias es mejor validar explícitamente y dar un mensaje de error útil.

**P: ¿Puede `load_dotenv` sobreescribir variables ya definidas en el sistema?**
R: Con `override=False` (por defecto) no las sobreescribe. Con `override=True` sí. En producción siempre se usa `override=False` para que las variables del sistema (más seguras) tengan prioridad.

**P: Si alguien borró accidentalmente el `.env`, ¿cómo sabe el equipo qué variables necesita?**
R: Gracias al `.env.example` commiteado en el repositorio. Por eso siempre hay que mantenerlo actualizado.

**P: ¿`python-dotenv` es seguro para producción?**
R: En producción generalmente no se usa `.env` ni `python-dotenv`. Las variables las inyecta la infraestructura (Kubernetes Secrets, AWS Parameter Store, variables del sistema del servidor). `python-dotenv` es una herramienta de conveniencia para desarrollo local.

### Sobre flake8 y mypy

**P: ¿Por qué `mypy --strict` y no solo `mypy`?**
R: `--strict` activa todas las comprobaciones opcionales: `disallow_untyped_defs`, `disallow_any_generics`, `warn_return_any`, etc. Obliga a que el código esté completamente anotado, lo que elimina una categoría entera de bugs en tiempo de ejecución.

**P: ¿Por qué en `loading.py` se permiten errores de import de mypy?**
R: Porque `numpy`, `pandas` y `matplotlib` no incluyen anotaciones de tipos completas en todas sus versiones. Se usa `# type: ignore[import-untyped]` para suprimir solo ese error sin relajar el resto de comprobaciones.

**P: ¿Qué diferencia hay entre un error de flake8 y uno de mypy?**
R: flake8 detecta problemas de **estilo y formato** (líneas largas, imports no usados, etc.). mypy detecta **errores de tipos** (pasar un `str` donde se espera un `int`, variables sin anotar, etc.). Son complementarios: uno cuida la forma, el otro la corrección semántica.