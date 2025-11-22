Uso rápido

1. Crear y activar un entorno virtual e instalar dependencias:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r c:\Users\Juan\Desktop\python\Panda\requirements.txt
```

2. Ejecutar la aplicación GUI:

```powershell
python c:\Users\Juan\Desktop\python\Panda\calculapuntajeagregacolumnaexcel.py
```

3. Uso desde la GUI:
- Pulsa `Seleccionar archivo...` para escoger tu `Libro1prueba.xlsx` (o cualquier otro Excel).
- Pulsa `Cargar y calcular` para que la aplicación lea la hoja `Hoja1`, detecte columnas que contengan `puntaje` y calcule la columna `puntaje final` (promedio entre las columnas de puntaje).
- La aplicación añadirá una última fila con el promedio de cada columna de puntaje y del `puntaje final`.
- Pulsa `Guardar como...` para elegir dónde guardar el resultado (incluye la fila `PROMEDIO`).

Notas importantes:
- La aplicación detecta automáticamente columnas cuyo nombre contiene la palabra `puntaje` (insensible a mayúsculas).
- Si se encuentran valores no numéricos en columnas de puntaje, la app preguntará si deseas convertirlos a vacío (NaN) antes de continuar.
- Requiere `pandas` y `openpyxl` para lectura/escritura de Excel.
