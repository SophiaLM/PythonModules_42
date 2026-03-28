# RAII:

El concepto de RAII (Resource Acquisition Is Initialization) es el corazón
de la seguridad en sistemas críticos.Aunque RAII nació en C++, en Python 
aplicamos la misma filosofía, pero de una forma mucho más "limpia" gracias
a una estructura que ya conoces bien: el Context Manager (la sentencia with).

# 1. El Problema: El "Olvido" del Archivista
En el vídeo mencionan que el problema principal es la limpieza explícita. 
En Python, si abres un archivo o una conexión a una base de datos y olvidas
cerrarla, el recurso se queda "colgado".

def codigo_peligroso_estilo_c():
    vault = open("top_secret.txt", "w")
    # Si aquí ocurre un error o un 'return' inesperado...
    vault.write("Data...") 
    # ...esta línea NUNCA se ejecuta. Puerta abierta.
    vault.close()

# 2. ¿Qué es RAII en Python?
En C++, RAII liga el recurso al ciclo de vida de un objeto 
(Constructor/Destructor). En Python (Context Manager): El dueño
es el Bloque de Código. La linterna se enciende cuando entras
en una "habitación" específica (with) y se apaga obligatoriamente
cuando sales de esa habitación, sin importar si saliste caminando
o si saliste volando por una explosión (excepción).

# 3. Ejemplos Reales en Python:

----> Gestión de Archivos (Este proyecto)
Es el ejemplo más puro de RAII. El "recurso" es el descriptor del
archivo del sistema operativo, que es limitado.

def gestion_de_archivos():
RAII en acción: La adquisición es la inicialización del 'with'
with open("ancient_vault.txt", "r") as vault:
    data = vault.read()
Al salir de este bloque, el 'destructor' (__exit__) se activa solo.

# 4. Python: El Protocolo del Context Manager (with)
Python no es tan determinista con los objetos (tiene un recolector
de basura que decide cuándo borrar cosas), por eso usa el bloque
de ejecución como ancla de seguridad.

Cuando escribes with open(...) as f:, Python ejecuta un "baile" de dos pasos:

__enter__ (La entrada): Se ejecuta justo al empezar el with.
Aquí es donde se "adquiere" el recurso (se abre el archivo).

__exit__ (La salida): Se ejecuta siempre al terminar el bloque
indentado, incluso si hubo un error de tipo ValueError o 
IndexError. Es el equivalente al destructor de C++ pero atado
al tiempo de ejecución del bloque.

Python dice: """No me importa cuánto viva el objeto en la memoria 
             lo que me importa es que dentro de estas líneas de
             código el recurso está abierto, y al salir, lo cierro sí o sí"""
