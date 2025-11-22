import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# === Configuración por defecto ===
CARPETA_BASE = r"C:\Users\Juan\Desktop\python\Panda"
ARCHIVO_ORIGEN = "Libro1prueba.xlsx"
HOJA_ORIGEN = "Hoja1"


class AppExcel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculador de Puntaje - Excel")
        self.geometry("1000x600")

        # Estado
        self.df = None
        self.selected_file = None

        # Top frame: controles
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        # Label que mostrará la ruta seleccionada o el origen por defecto
        self.lbl_archivo = ttk.Label(top, text="Archivo: (ninguno seleccionado)")
        self.lbl_archivo.pack(side="left", padx=(0, 10))

        # Botones principales
        ttk.Button(top, text="Seleccionar archivo...", command=self.seleccionar_archivo).pack(side="left")
        ttk.Button(top, text="Cargar y calcular", command=self.cargar_y_calcular).pack(side="left", padx=6)
        ttk.Button(top, text="Guardar como...", command=self.guardar_como).pack(side="left", padx=6)
        ttk.Button(top, text="Salir", command=self.confirmar_salida).pack(side="right")

        # Area central: tabla
        mid = ttk.Frame(self, padding=8)
        mid.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(mid, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        yscroll = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        yscroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscroll.set)

        # Barra de estado
        self.status = ttk.Label(self, anchor="w", padding=6, relief="groove")
        self.status.pack(fill="x")

        # Manejo de cierre
        self.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

        # Mostrar origen por defecto en la etiqueta
        default_path = os.path.join(CARPETA_BASE, ARCHIVO_ORIGEN)
        self.lbl_archivo.config(text=f"Archivo: {default_path}  (use 'Seleccionar archivo...' para cambiar)")

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione el archivo Excel",
            initialdir=CARPETA_BASE,
            filetypes=[("Excel files", "*.xlsx;*.xls")]
        )
        if ruta:
            self.selected_file = ruta
            self.lbl_archivo.config(text=f"Archivo: {ruta}")
            self.status.config(text="Archivo seleccionado.")

    def cargar_y_calcular(self):
        # Si el usuario seleccionó un archivo, úsalo; sino usa el archivo por defecto
        ruta = self.selected_file or os.path.join(CARPETA_BASE, ARCHIVO_ORIGEN)

        try:
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"No se encontró el archivo:\n{ruta}")

            df = pd.read_excel(ruta, sheet_name=HOJA_ORIGEN)

            # Estandarizar nombre 'nombre' si existe con mayúsculas/minúsculas
            cols_lower = {c.lower(): c for c in df.columns}
            if 'nombre' in cols_lower:
                df = df.rename(columns={cols_lower['nombre']: 'nombre'})

            # Detectar columnas de puntaje (contienen 'puntaje' en el nombre)
            puntaje_cols = [c for c in df.columns if 'puntaje' in c.lower()]
            if not puntaje_cols:
                raise KeyError("No se encontraron columnas cuyo nombre contenga 'puntaje'.")

            # Hacer copia para detectar conversiones a NaN
            df_orig = df.copy()

            # Convertir a numérico y contar conversiones fallidas
            non_numeric_info = {}
            for c in puntaje_cols:
                df[c] = pd.to_numeric(df[c], errors='coerce')
                # cuentan los que se volvieron NaN pero antes no eran NaN
                converted = df[c].isna() & ~df_orig[c].isna()
                non_numeric_info[c] = int(converted.sum())

            # Si hay conversiones, avisar al usuario y pedir confirmación
            total_converted = sum(non_numeric_info.values())
            if total_converted > 0:
                detalle = '\n'.join([f"{k}: {v} no numérico(s)" for k, v in non_numeric_info.items() if v > 0])
                if not messagebox.askyesno(
                    "Valores no numéricos",
                    f"Se detectaron valores no numéricos en columnas de puntaje:\n{detalle}\n\nSe convertirán a vacío (NaN). ¿Deseas continuar?"
                ):
                    self.status.config(text="Operación cancelada por el usuario (valores no numéricos).")
                    return

            # Calcular puntaje final (promedio simple entre las columnas de puntaje)
            df['puntaje final'] = df[puntaje_cols].mean(axis=1).round(2)

            # Calcular fila de promedios para cada columna de puntaje y puntaje final
            promedios = df[puntaje_cols + ['puntaje final']].mean(axis=0)

            # Construir fila promedio manteniendo otras columnas vacías y escribiendo 'PROMEDIO' en 'nombre' si existe
            promedio_row = {col: '' for col in df.columns}
            for col, val in promedios.items():
                promedio_row[col] = round(float(val), 2)
            if 'nombre' in df.columns:
                promedio_row['nombre'] = 'PROMEDIO'

            # Añadir fila de promedio al final
            df_final = pd.concat([df, pd.DataFrame([promedio_row])], ignore_index=True)

            # Guardar y mostrar
            self.df = df_final
            self._poblar_treeview(df_final)
            self.status.config(text=f"Cargado: {os.path.basename(ruta)} — {len(df)} filas (fila promedio añadida).")

        except Exception as e:
            messagebox.showerror("Error al cargar/procesar", str(e))
            self.status.config(text="Error al cargar/procesar.")

    def _poblar_treeview(self, df: pd.DataFrame):
        # Limpiar
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())

        cols = list(df.columns)
        self.tree["columns"] = cols

        for c in cols:
            self.tree.heading(c, text=c)
            width = 200 if c == 'nombre' else 120
            self.tree.column(c, width=width, anchor='center')

        for row in df.fillna('').values.tolist():
            self.tree.insert('', 'end', values=row)

    def guardar_como(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Nada que guardar", "Primero carga y calcula los datos.")
            return

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar como",
            initialdir=CARPETA_BASE,
            defaultextension='.xlsx',
            filetypes=[('Excel (*.xlsx)', '*.xlsx'), ('Excel 97-2003 (*.xls)', '*.xls')],
            confirmoverwrite=True
        )
        if not ruta_salida:
            return

        try:
            carpeta = os.path.dirname(ruta_salida)
            if carpeta and not os.path.exists(carpeta):
                os.makedirs(carpeta, exist_ok=True)

            # Escribir DataFrame (incluye la fila PROMEDIO)
            self.df.to_excel(ruta_salida, sheet_name=HOJA_ORIGEN, index=False)
            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{ruta_salida}")
            self.status.config(text=f"Guardado: {ruta_salida}")
        except PermissionError:
            messagebox.showerror("Permiso denegado", "No se pudo guardar. ¿Está el archivo abierto en Excel?")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
            self.status.config(text='Error al guardar.')

    def confirmar_salida(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.destroy()


if __name__ == '__main__':
    app = AppExcel()
    app.mainloop()
