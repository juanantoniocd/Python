# analizar datos de un archivo csv, el usuario puede seleccionar archivo mediante una interfaz que contenga botón abrir csv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def on_closing():
    """Función para manejar el cierre de la ventana"""
    pass

#muestra datos en una tabla
def mostrar_datos_en_tabla(datos):
    ventana = tk.Tk()
    ventana.title("Datos en Tabla")
    ventana.geometry("800x600")
    ventana.resizable(True, True)
    ventana.configure(bg="white")
    try:
        ventana.iconbitmap("icono.ico")
    except:
        pass  # Si no existe el icono, continúa sin él
    ventana.protocol("WM_DELETE_WINDOW", lambda: ventana.destroy())
    ventana.mainloop()

# Calcula estadísticas simples: media, mediana, desviación estándar de cada columna
def calcular_estadisticas(datos):
    media = datos.mean()
    mediana = datos.median()
    desviacion = datos.std()
    return media, mediana, desviacion

# Genera una gráfica de dispersión de una columna vs. la otra, Traza un scatter plot de col1 vs. col2
def generar_grafica_dispersión(datos, columna1, columna2):
    sns.scatterplot(x=columna1, y=columna2, data=datos)
    plt.xlabel(columna1)
    plt.ylabel(columna2)
    plt.title(f"Gráfica de Dispersión de {columna1} vs. {columna2}")
    plt.show()

def abrir_csv():
    """Abre un diálogo para seleccionar un archivo CSV"""
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    
    if archivo:
        try:
            # Cargar el archivo CSV
            datos = pd.read_csv(archivo)
            
            # Mostrar información del archivo
            messagebox.showinfo("Éxito", f"Archivo cargado correctamente.\nFilas: {len(datos)}\nColumnas: {len(datos.columns)}")
            
            # Actualizar la interfaz con los datos
            actualizar_interfaz(datos)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")

def actualizar_interfaz(datos):
    """Actualiza la interfaz con los datos cargados"""
    global datos_actuales
    datos_actuales = datos
    
    # Obtener columnas numéricas
    columnas_numericas = datos.select_dtypes(include=[np.number]).columns.tolist()
    columnas_texto = datos.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # Limpiar el área de texto
    texto_datos.delete(1.0, tk.END)
    
    # Mostrar información básica
    texto_datos.insert(tk.END, f"Archivo cargado: {len(datos)} filas, {len(datos.columns)} columnas\n\n")
    texto_datos.insert(tk.END, "Columnas numéricas (para gráficas y estadísticas):\n")
    if columnas_numericas:
        for col in columnas_numericas:
            texto_datos.insert(tk.END, f"  ✓ {col} ({datos[col].dtype})\n")
    else:
        texto_datos.insert(tk.END, "  (No hay columnas numéricas)\n")
    
    if columnas_texto:
        texto_datos.insert(tk.END, "\nColumnas de texto:\n")
        for col in columnas_texto:
            texto_datos.insert(tk.END, f"  - {col} ({datos[col].dtype})\n")
    
    texto_datos.insert(tk.END, "\n" + "="*50 + "\n\n")
    texto_datos.insert(tk.END, "Primeras 10 filas:\n\n")
    texto_datos.insert(tk.END, datos.head(10).to_string())
    
    # Actualizar los comboboxes de columnas SOLO con columnas numéricas
    if columnas_numericas:
        combo_col1['values'] = columnas_numericas
        combo_col2['values'] = columnas_numericas
        combo_col1.current(0)
        if len(columnas_numericas) > 1:
            combo_col2.current(1)
        else:
            combo_col2.current(0)
        btn_grafica.config(state=tk.NORMAL, fg="white")
    else:
        combo_col1['values'] = []
        combo_col2['values'] = []
        combo_col1.set("")
        combo_col2.set("")
        btn_grafica.config(state=tk.DISABLED, fg="white")
        texto_datos.insert(tk.END, "\n\n⚠ ADVERTENCIA: No hay columnas numéricas para generar gráficas.\n")
    
    # Habilitar botones
    if columnas_numericas:
        btn_estadisticas.config(state=tk.NORMAL, fg="white")
    else:
        btn_estadisticas.config(state=tk.DISABLED, fg="white")
    btn_tabla.config(state=tk.NORMAL, fg="white")

def mostrar_estadisticas():
    """Muestra las estadísticas de los datos"""
    if 'datos_actuales' not in globals():
        messagebox.showwarning("Advertencia", "Por favor, carga un archivo CSV primero")
        return
    
    try:
        media, mediana, desviacion = calcular_estadisticas(datos_actuales)
        
        ventana_stats = tk.Toplevel(ventana)
        ventana_stats.title("Estadísticas")
        ventana_stats.geometry("600x400")
        ventana_stats.configure(bg="white")
        
        texto_stats = scrolledtext.ScrolledText(ventana_stats, wrap=tk.WORD, width=70, height=20,
                                                bg="white", fg="black", font=("Arial", 10))
        texto_stats.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        texto_stats.insert(tk.END, "ESTADÍSTICAS DESCRIPTIVAS\n")
        texto_stats.insert(tk.END, "="*50 + "\n\n")
        
        for col in datos_actuales.select_dtypes(include=[np.number]).columns:
            texto_stats.insert(tk.END, f"Columna: {col}\n")
            texto_stats.insert(tk.END, f"  Media: {media[col]:.2f}\n")
            texto_stats.insert(tk.END, f"  Mediana: {mediana[col]:.2f}\n")
            texto_stats.insert(tk.END, f"  Desviación Estándar: {desviacion[col]:.2f}\n")
            texto_stats.insert(tk.END, "\n")
        
        texto_stats.config(state=tk.DISABLED)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular estadísticas:\n{str(e)}")

def mostrar_grafica():
    """Muestra la gráfica de dispersión"""
    if 'datos_actuales' not in globals():
        messagebox.showwarning("Advertencia", "Por favor, carga un archivo CSV primero")
        return
    
    col1 = combo_col1.get()
    col2 = combo_col2.get()
    
    if not col1 or not col2:
        messagebox.showwarning("Advertencia", "Por favor, selecciona dos columnas")
        return
    
    try:
        # Intentar convertir a numérico si es necesario
        datos_temp = datos_actuales.copy()
        
        # Convertir columna 1 si no es numérica
        if not pd.api.types.is_numeric_dtype(datos_temp[col1]):
            datos_temp[col1] = pd.to_numeric(datos_temp[col1], errors='coerce')
        
        # Convertir columna 2 si no es numérica
        if not pd.api.types.is_numeric_dtype(datos_temp[col2]):
            datos_temp[col2] = pd.to_numeric(datos_temp[col2], errors='coerce')
        
        # Verificar que las conversiones fueron exitosas
        if datos_temp[col1].isna().all() or datos_temp[col2].isna().all():
            messagebox.showerror("Error", 
                f"No se pueden convertir las columnas a valores numéricos.\n\n"
                f"Columna 1 ({col1}): {datos_actuales[col1].dtype}\n"
                f"Columna 2 ({col2}): {datos_actuales[col2].dtype}\n\n"
                f"Por favor, selecciona columnas que contengan números.")
            return
        
        # Eliminar filas con valores NaN para la gráfica
        datos_grafica = datos_temp[[col1, col2]].dropna()
        
        if len(datos_grafica) == 0:
            messagebox.showerror("Error", "No hay datos válidos para graficar después de eliminar valores faltantes.")
            return
        
        generar_grafica_dispersión(datos_grafica, col1, col2)
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráfica:\n{str(e)}")

def mostrar_tabla_completa():
    """Muestra los datos en una tabla"""
    if 'datos_actuales' not in globals():
        messagebox.showwarning("Advertencia", "Por favor, carga un archivo CSV primero")
        return
    
    ventana_tabla = tk.Toplevel(ventana)
    ventana_tabla.title("Datos en Tabla")
    ventana_tabla.geometry("900x600")
    ventana_tabla.configure(bg="white")
    
    # Crear un Treeview para mostrar los datos
    frame_tabla = tk.Frame(ventana_tabla, bg="white")
    frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    scrollbar_y = tk.Scrollbar(frame_tabla)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    scrollbar_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    
    tree = ttk.Treeview(frame_tabla, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)
    
    # Configurar columnas
    tree['columns'] = list(datos_actuales.columns)
    tree['show'] = 'headings'
    
    for col in datos_actuales.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    # Insertar datos
    for index, row in datos_actuales.iterrows():
        tree.insert('', tk.END, values=list(row))

def salir():
    """Cierra la aplicación"""
    ventana.quit()
    ventana.destroy()

def main():
    """Función principal que crea la interfaz"""
    global ventana, texto_datos, combo_col1, combo_col2, btn_estadisticas, btn_grafica, btn_tabla
    
    ventana = tk.Tk()
    ventana.title("Análisis de Datos CSV")
    ventana.geometry("800x600")
    ventana.resizable(True, True)
    ventana.configure(bg="white")
    
    # Frame superior con botón para abrir CSV
    frame_superior = tk.Frame(ventana, bg="white", pady=10)
    frame_superior.pack(fill=tk.X)
    
    btn_abrir = tk.Button(frame_superior, text="Abrir CSV", command=abrir_csv, 
                         bg="#0066CC", fg="white", activeforeground="white",
                         disabledforeground="white", font=("Arial", 12, "bold"), 
                         padx=20, pady=5)
    btn_abrir.pack(side=tk.LEFT, padx=10)
    
    btn_salir = tk.Button(frame_superior, text="Salir", command=salir, 
                         bg="#0066CC", fg="white", activeforeground="white",
                         disabledforeground="white", font=("Arial", 12, "bold"), 
                         padx=20, pady=5)
    btn_salir.pack(side=tk.RIGHT, padx=10)
    
    # Frame para selección de columnas
    frame_columnas = tk.Frame(ventana, bg="white", pady=10)
    frame_columnas.pack(fill=tk.X, padx=10)
    
    tk.Label(frame_columnas, text="Columna 1:", font=("Arial", 10), bg="white", fg="black").pack(side=tk.LEFT, padx=5)
    combo_col1 = ttk.Combobox(frame_columnas, state="readonly", width=20)
    combo_col1.pack(side=tk.LEFT, padx=5)
    
    tk.Label(frame_columnas, text="Columna 2:", font=("Arial", 10), bg="white", fg="black").pack(side=tk.LEFT, padx=5)
    combo_col2 = ttk.Combobox(frame_columnas, state="readonly", width=20)
    combo_col2.pack(side=tk.LEFT, padx=5)
    
    # Frame para botones de acciones
    frame_botones = tk.Frame(ventana, bg="white", pady=10)
    frame_botones.pack(fill=tk.X, padx=10)
    
    btn_estadisticas = tk.Button(frame_botones, text="Ver Estadísticas", 
                                 command=mostrar_estadisticas, state=tk.DISABLED,
                                 bg="#0066CC", fg="white", activeforeground="white",
                                 disabledforeground="white", padx=15, pady=5, font=("Arial", 10))
    btn_estadisticas.pack(side=tk.LEFT, padx=5)
    
    btn_grafica = tk.Button(frame_botones, text="Generar Gráfica", 
                           command=mostrar_grafica, state=tk.DISABLED,
                           bg="#0066CC", fg="white", activeforeground="white",
                           disabledforeground="white", padx=15, pady=5, font=("Arial", 10))
    btn_grafica.pack(side=tk.LEFT, padx=5)
    
    btn_tabla = tk.Button(frame_botones, text="Ver Tabla Completa", 
                         command=mostrar_tabla_completa, state=tk.DISABLED,
                         bg="#0066CC", fg="white", activeforeground="white",
                         disabledforeground="white", padx=15, pady=5, font=("Arial", 10))
    btn_tabla.pack(side=tk.LEFT, padx=5)
    
    # Área de texto para mostrar datos
    frame_texto = tk.Frame(ventana, bg="white")
    frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    texto_datos = scrolledtext.ScrolledText(frame_texto, wrap=tk.WORD, width=80, height=20,
                                            bg="white", fg="black", font=("Arial", 10))
    texto_datos.pack(fill=tk.BOTH, expand=True)
    texto_datos.insert(tk.END, "Bienvenido al Analizador de Datos CSV\n\n")
    texto_datos.insert(tk.END, "Por favor, haz clic en 'Abrir CSV' para cargar un archivo.\n")
    
    ventana.mainloop()

if __name__ == "__main__":
    main()