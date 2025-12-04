# -*- coding: utf-8 -*-
"""
Días 1–2: Descriptivos + Percentiles + Visualización (con tu Excel)
Requisitos: pandas, numpy, matplotlib, openpyxl

Instalar (si falta):
    pip install pandas numpy matplotlib openpyxl
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==== 1) Ruta del archivo (ajústala si es necesario) ====
RUTA = r"C:\Users\Juan\Desktop\python\analisis_estadistico\estudiantes_notas_practica.xlsx"
HOJA_CONSOLIDADO = "Consolidado"   # así lo dejé creado
COLUMNA_ANALISIS = "promedio_final"  # métrica principal a analizar

# ==== 2) Cargar datos ====
if not os.path.exists(RUTA):
    raise FileNotFoundError(f"No se encontró el archivo en: {RUTA}")

df = pd.read_excel(RUTA, sheet_name=HOJA_CONSOLIDADO, engine="openpyxl")
if COLUMNA_ANALISIS not in df.columns:
    raise KeyError(f"No existe la columna '{COLUMNA_ANALISIS}' en la hoja '{HOJA_CONSOLIDADO}'.")

x = df[COLUMNA_ANALISIS].dropna().astype(float).values

# ==== 3) Descriptivos Día 1 ====
def varianza(x, poblacional=True):
    # ddof = 0 para población, ddof = 1 para muestra
    ddof = 0 if poblacional else 1
    return np.var(x, ddof=ddof)

def desv_estandar(x, poblacional=True):
    return np.sqrt(varianza(x, poblacional=poblacional))

media = np.mean(x)
mediana = np.median(x)

# Moda (si hay empate, muestra todas)
valores, frec = np.unique(x, return_counts=True)
max_f = frec.max()
if max_f == 1:
    moda_str = "Sin moda (amodal)"
else:
    modas = valores[frec == max_f]
    moda_str = ", ".join(f"{m:.2f}" for m in modas)

var_pobl = varianza(x, poblacional=True)
std_pobl = desv_estandar(x, poblacional=True)
var_mues = varianza(x, poblacional=False)
std_mues = desv_estandar(x, poblacional=False)

# ==== 4) Percentiles Día 2 ====
# método 'linear' = interpolación lineal
try:
    p25 = np.percentile(x, 25, method="linear")
    p50 = np.percentile(x, 50, method="linear")
    p75 = np.percentile(x, 75, method="linear")
except TypeError:
    # compatibilidad con NumPy antiguos
    p25 = np.percentile(x, 25, interpolation="linear")
    p50 = np.percentile(x, 50, interpolation="linear")
    p75 = np.percentile(x, 75, interpolation="linear")

resumen = pd.DataFrame({
    "Métrica": [
        "Media (poblacional)",
        "Mediana",
        "Moda",
        "Varianza (poblacional)",
        "Desv. Estándar (poblacional)",
        "Varianza (muestral)",
        "Desv. Estándar (muestral)",
        "P25 (Q1)",
        "P50 (Mediana)",
        "P75 (Q3)",
        "n"
    ],
    "Valor": [
        media,
        mediana,
        moda_str,
        var_pobl,
        std_pobl,
        var_mues,
        std_mues,
        p25,
        p50,
        p75,
        len(x)
    ]
})

print("\n=== Resumen Día 1–2 sobre", COLUMNA_ANALISIS, "===")
with pd.option_context("display.float_format", "{:,.4f}".format):
    print(resumen.to_string(index=False))

# Guardar resumen a CSV junto al Excel
salida_csv = os.path.join(os.path.dirname(RUTA), "resumen_dia1_2.csv")
resumen.to_csv(salida_csv, index=False, encoding="utf-8-sig")
print(f"\nResumen guardado en: {salida_csv}")

# ==== 5) Visualización (gráficos separados, sin estilos/colores específicos) ====

# Histograma
plt.figure()
plt.hist(x, bins=15, edgecolor="black")
plt.title(f"Histograma de {COLUMNA_ANALISIS}")
plt.xlabel(COLUMNA_ANALISIS)
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.show()

# Boxplot
plt.figure()
plt.boxplot(x, vert=True, showmeans=True)
plt.title(f"Diagrama de Caja (Boxplot) de {COLUMNA_ANALISIS}")
plt.ylabel(COLUMNA_ANALISIS)
plt.tight_layout()
plt.show()
