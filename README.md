# Buscaminas en MARIE.js con generador en Python

Proyecto académico de **Organización de Computadoras** para implementar una versión funcional de **Buscaminas** en **MARIE.js** sobre un tablero de **16×16**, usando un generador externo en Python para construir el mapa del juego y exportar el archivo `.mas` listo para ejecutar.

## Autores

- **Mateo Diaz**
- **Ayelen Jaramillo**

---

## Descripción del proyecto

Este proyecto implementa el juego **Buscaminas** en la arquitectura educativa **MARIE.js**, respetando sus limitaciones de entrada, memoria y visualización.

La solución está dividida en dos partes:

### 1. Generación del tablero en Python
Python se encarga de:

- crear un tablero de **16×16**
- ubicar minas
- calcular el número de minas vecinas de cada celda
- generar el bloque de memoria compatible con MARIE
- generar una **máscara de forma** para modificar la geometría visible del tablero
- exportar el archivo final `.mas`
- exportar archivos auxiliares `.mem`
- generar una imagen de vista previa del tablero

### 2. Ejecución del juego en MARIE.js
El programa en MARIE se encarga de:

- leer **fila**
- leer **columna**
- leer **acción**
- revelar celdas
- colocar o quitar banderas
- mostrar el tablero en el display 16×16
- controlar inicio y fin del juego
- contar cuántas banderas han sido colocadas

---

## Características principales

- tablero de **16×16**
- generación automática de minas y vecinos
- exportación automática a **MARIE.js**
- salida visual del tablero en imagen
- notebook autosuficiente para presentación en **Google Colab**
- estructura organizada para desarrollo local en **PyCharm** o cualquier entorno Python

---

## Estructura del proyecto

```text
buscaminas-marie/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── buscaminas_colab_actualizado.ipynb
│
├── src/
│   ├── __init__.py
│   ├── generador_tablero.py
│   ├── exportador_marie.py
│   └── utilidades.py
│
├── marie/
│   ├── plantillas/
│   │   └── buscaminas_template_mod.mas
│   └── generados/
│       ├── buscaminas_generado_mod.mas
│       ├── tablero_marie_generado.mem
│       └── shape_preset_generado.mem
│
├── outputs/
│   └── vista_tablero_buscaminas.png
│
└── docs/
    └── enunciado_proyecto.md
```
## Cómo funciona el juego

En MARIE.js, cada turno del jugador se realiza mediante tres entradas consecutivas:

1. **fila**
2. **columna**
3. **acción**

### Convención de acciones

- `1` → revelar celda
- `2` → colocar o quitar bandera

### Ejemplo de jugada

Revelar la celda fila 6, columna 10:

```text
6
10
1
```
Colocar o quitar bandera en fila 3, columna 7:
```text
3
7
2
```
Rango de coordenadas

Como el tablero es de 16×16, las coordenadas válidas son:

- filas: 0 a 15
- columnas: 0 a 15

## Ejecución local

### Requisitos

- Python 3.10 o superior
- Jupyter Notebook o PyCharm con soporte para notebooks
- Marie.js para ejecutar el archivo `.mas`

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd buscaminas-marie
```
### 2. Crear entorno virtual (opcional, recomendado)
### Windows 

```bash
python -m venv .venv
.venv\Scripts\activate
```
### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Ejecutar el notebook
Abrir:

```bash
notebooks/buscaminas_colab_actualizado.ipynb
```
y ejecutar todas las celdas.
### 5. Archivos generados
Después de ejecutar el notebook, se generan automáticamente:
- marie/generados/buscaminas_generado_mod.mas
- marie/generados/tablero_marie_generado.mem
- marie/generados/shape_preset_generado.mem
- outputs/vista_tablero_buscaminas.png
### 6. Ejecutar en MARIE.js
Abrir en Marie.js el archivo:
```bash
marie/generados/buscaminas_generado_mod.mas
```
Ejecución desde Google Colab

El proyecto incluye un notebook independiente pensado para presentación.

Ventajas del notebook
- no depende de rutas locales
- no requiere archivos auxiliares obligatorios
- incluye la plantilla .mas embebida
- puede ejecutarse directamente en Colab
  Pasos:
 ### 1. Abrir Google Colab
### 2. Subir el archivo:
```bash
notebooks/buscaminas_colab_actualizado.ipynb
```
### 3. Ejecutar todas las celdas
### 4. Descargar o usar el archivo generado:

```bash
marie/generados/buscaminas_generado_mod.mas
```
### 5. Abrir ese archivo en Marie.js

## Parámetros configurables

Dentro del notebook se pueden modificar fácilmente los parámetros del tablero:

- número de minas
- semilla aleatoria
- lista manual de minas
- forma del tablero

### Formas soportadas

- `llena`
- `rombo`
- `cruz`
- `marco`
- `personalizada`

Esto permite que durante la presentación se pueda mostrar cómo cambia la forma del tablero partiendo de la base 16×16.

## Archivos importantes

### `src/generador_tablero.py`
Contiene la lógica para:

- crear el tablero
- colocar minas
- calcular vecinos
- generar máscaras de forma

### `src/exportador_marie.py`
Contiene la lógica para:

- convertir matrices a formato `DEC`
- exportar `.mem`
- insertar bloques en la plantilla `.mas`
- exportar el archivo final `.mas`

### `src/utilidades.py`
Contiene funciones para:

- imprimir el tablero en texto
- mostrar máscaras
- generar la visualización en imagen

### `marie/plantillas/buscaminas_template_mod.mas`
- marie/plantillas/buscaminas_template_mod.mas: Plantilla base con Lógica V6. Implementa un direccionamiento de memoria exacto (post-cabecera) para las matrices de juego, asegurando que B_REAL, B_SHAPE y B_REGIONS coincidan exactamente con la inyección de datos desde Python.

## Resultados esperados

Al ejecutar correctamente el notebook, el usuario obtiene:

- un tablero Buscaminas válido
- una máscara de forma
- un archivo `.mas` listo para abrir en MARIE.js
- archivos `.mem` de apoyo
- una imagen del tablero generado

## Observaciones

- El display 16×16 de MARIE.js se usa principalmente como representación visual del tablero.
- La plantilla está preparada para trabajar con colores y estados del juego.
- Dependiendo de la variante exacta de MARIE.js, puede ser necesario ajustar detalles menores de ensamblado o de direcciones del display.

## Licencia

Proyecto académico desarrollado con fines educativos.
