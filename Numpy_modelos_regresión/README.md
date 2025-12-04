# Regresión Lineal y Polinómica con Reporte

## Descripción
Este programa implementa modelos de regresión lineal y polinómica para analizar y predecir ventas mensuales. Genera un reporte con las métricas de evaluación de los modelos, predicciones futuras y una visualización gráfica.

## Funcionalidades
- **Creación de dataset**: Genera un conjunto de datos de ventas mensuales con variaciones.
- **Modelos de regresión**: Ajusta modelos de regresión lineal y polinómica (grado 2).
- **Predicciones futuras**: Realiza predicciones para meses futuros.
- **Evaluación de modelos**: Calcula métricas como R², MAE y RMSE.
- **Exportación**: Guarda los datos, métricas y predicciones en un archivo Excel.
- **Visualización**: Genera un gráfico comparativo y lo guarda como imagen PNG.

## Requisitos
- Python 3.10 o superior
- Bibliotecas necesarias:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `scikit-learn`
  - `openpyxl`

## Instalación
1. Clona este repositorio o descarga el archivo `Numpy_Reg_Lineal_Poli_Reporte.py`.
2. Asegúrate de tener instaladas las bibliotecas necesarias. Puedes instalarlas ejecutando:
   ```bash
   pip install pandas numpy matplotlib scikit-learn openpyxl
   ```

## Uso
1. Ejecuta el script:
   ```bash
   python Numpy_Reg_Lineal_Poli_Reporte.py
   ```
2. El programa generará:
   - Un archivo Excel con el dataset, métricas y predicciones futuras en:
     ```
     C:\Users\Juan\Desktop\python\Numpy\reporte.xlsx
     ```
   - Un gráfico comparativo guardado como imagen PNG en:
     ```
     C:\Users\Juan\Desktop\python\Numpy\grafico.png
     ```

## Notas
- Asegúrate de tener conexión a internet si necesitas instalar bibliotecas.
- Puedes modificar el dataset inicial o los parámetros de los modelos directamente en el script.

## Autor
Juan