# Análisis de Datos CSV

Aplicación de escritorio para analizar archivos CSV con interfaz gráfica.

## Requisitos

- Python 3.7 o superior

## Instalación

1. Crear un entorno virtual (recomendado):
```bash
py -m venv venv
```

2. Activar el entorno virtual:
   - En PowerShell:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
   - En CMD:
   ```bash
   venv\Scripts\activate.bat
   ```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar la aplicación:
```bash
python analisisdatos.py
```

## Funcionalidades

- Cargar archivos CSV mediante interfaz gráfica
- Visualizar datos en tabla
- Calcular estadísticas descriptivas (media, mediana, desviación estándar)
- Generar gráficas de dispersión entre columnas numéricas

## Crear Ejecutable

Para crear un ejecutable independiente (no requiere Python instalado):

1. Instalar PyInstaller:
```bash
pip install pyinstaller
```

2. Crear el ejecutable:
```bash
pyinstaller --name="AnalisisDatosCSV" --windowed --onefile --clean analisisdatos.py
```

El ejecutable se encontrará en la carpeta `dist/AnalisisDatosCSV.exe`.

**Nota**: El ejecutable tendrá aproximadamente 48-50 MB debido a que incluye todas las dependencias necesarias (pandas, matplotlib, seaborn, numpy, tkinter).

## Ejecutar el Ejecutable

Simplemente haz doble clic en `AnalisisDatosCSV.exe` en la carpeta `dist/`. No requiere tener Python instalado en el sistema.

