# Proyecto integrador semana 3: Lineal vs Polinómica con exportación a Excel y PNG

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os

# ============================
# 1. Dataset (ventas mensuales con variaciones)
# ============================
data = {
    "Mes": [1, 2, 3, 4, 5, 6],
    "Ventas": [200, 215, 240, 280, 290, 310]  # valores con ruido
}
df = pd.DataFrame(data)

print("=== Dataset ===")
print(df, "\n")

X = df[["Mes"]]
y = df["Ventas"]

# ============================
# 2. Modelo Lineal
# ============================
modelo_lineal = LinearRegression()
modelo_lineal.fit(X, y)
y_pred_lineal = modelo_lineal.predict(X)

# ============================
# 3. Modelo Polinómico (grado 2)
# ============================
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

modelo_poly = LinearRegression()
modelo_poly.fit(X_poly, y)
y_pred_poly = modelo_poly.predict(X_poly)

# ============================
# 4. Predicciones futuras
# ============================
futuro = np.array([[7], [8]])
pred_lineal = modelo_lineal.predict(futuro)
pred_poly = modelo_poly.predict(poly.transform(futuro))

print("=== Predicciones Futuras (Lineal) ===")
for mes, venta in zip([7, 8], pred_lineal):
    print(f"Mes {mes}: {venta:.2f} ventas")

print("\n=== Predicciones Futuras (Polinómica) ===")
for mes, venta in zip([7, 8], pred_poly):
    print(f"Mes {mes}: {venta:.2f} ventas")
print()

# ============================
# 5. Evaluación de modelos
# ============================
def evaluar_modelo(y_true, y_pred, nombre):
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {"Modelo": nombre, "R²": r2, "MAE": mae, "RMSE": rmse}

resultados = []
resultados.append(evaluar_modelo(y, y_pred_lineal, "Lineal"))
resultados.append(evaluar_modelo(y, y_pred_poly, "Polinómica"))

print("=== Evaluación de Modelos ===")
for r in resultados:
    print(r)

# ============================
# 6. Exportar a Excel
# ============================
df_report = pd.DataFrame(resultados)

df_predicciones = pd.DataFrame({
    "Mes": [7, 8],
    "Predicción Lineal": pred_lineal,
    "Predicción Polinómica": pred_poly
})

# Crear carpeta si no existe
carpeta = r"C:\Users\Juan\Desktop\python\Numpy"
os.makedirs(carpeta, exist_ok=True)

ruta_excel = os.path.join(carpeta, "reporte.xlsx")
ruta_png = os.path.join(carpeta, "grafico.png")

with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Dataset", index=False)
    df_report.to_excel(writer, sheet_name="Métricas", index=False)
    df_predicciones.to_excel(writer, sheet_name="Predicciones Futuras", index=False)

print(f"✅ Reporte Excel guardado en: {ruta_excel}")

# ============================
# 7. Visualización y guardar PNG
# ============================
plt.figure(figsize=(8,5))

plt.scatter(X, y, color="blue", label="Datos reales")
plt.plot(X, y_pred_lineal, color="red", label="Modelo Lineal")
plt.plot(X, y_pred_poly, color="green", linestyle="--", label="Modelo Polinómico")
plt.scatter([7, 8], pred_lineal, color="red", marker="x", s=100, label="Predicciones Lineales")
plt.scatter([7, 8], pred_poly, color="green", marker="o", s=100, facecolors="none", edgecolors="green", label="Predicciones Polinómicas")

plt.title("Predicción de Ventas: Lineal vs Polinómica")
plt.xlabel("Mes")
plt.ylabel("Ventas")
plt.legend()
plt.grid(True)

# Guardar como imagen
plt.savefig(ruta_png, dpi=300)
print(f"✅ Gráfico guardado en: {ruta_png}")

plt.show()
