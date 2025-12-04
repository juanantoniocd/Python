# Entorno de desarrollo para el proyecto MyShop

Instrucciones rápidas para configurar un entorno virtual en Windows (PowerShell) y ejecutar la aplicación.

Requisitos:
- Python 3.8+ instalado y accesible (ej. `C:\Users\...\Python\Python3xx\python.exe`).

Pasos (PowerShell):

1) Crear y activar entorno virtual (desde la carpeta del proyecto):

```powershell
# Crear entorno virtual en la carpeta .venv
python -m venv .venv

# Activar (PowerShell)
.\.venv\Scripts\Activate.ps1
# Si usas cmd.exe: .\.venv\Scripts\activate.bat
```

2) Actualizar pip e instalar dependencias:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3) Ejecutar la aplicación:

```powershell
python .\main.py
```

Notas:
- `tkinter` normalmente está incluido con Python en Windows (no requiere pip).
- Si tu instalación de Python no está en `PATH`, usa la ruta absoluta del ejecutable (ej.: `C:\Users\Juan\AppData\Local\Programs\Python\Python313\python.exe -m venv .venv`).
- `.gitignore` ya contiene `.venv/` y `__pycache__/` para evitar subir binarios.

Si quieres, puedo:
- Crear el entorno virtual aquí y ejecutar la instalación (ya puedo usar tu intérprete absoluto),
- Añadir instrucciones para Visual Studio Code (archivo `.vscode/settings.json`) para usar `.venv` automáticamente.
