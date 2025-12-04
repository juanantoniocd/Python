import tkinter as tk
from tkinter import ttk, messagebox
from products import create_product, list_products, update_product, delete_product, toggle_product_status
from gui import apply_style, center_window

def abrir_ventana_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    apply_style(ventana)
    center_window(ventana, width=800, height=600)

    # --- Formulario ---
    frame_form = ttk.LabelFrame(ventana, text="Agregar / Editar Producto")
    frame_form.pack(fill="x", padx=10, pady=10)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = ttk.Entry(frame_form, width=30)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
    entry_precio = ttk.Entry(frame_form, width=30)
    entry_precio.grid(row=1, column=1, padx=5, pady=5)

    # --- Tabla ---
    tabla = ttk.Treeview(ventana, columns=("id", "name", "price", "is_active"), show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("name", text="Nombre")
    tabla.heading("price", text="Precio")
    tabla.heading("is_active", text="Activo")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_productos():
        tabla.delete(*tabla.get_children())
        for p in list_products():
            estado = "Sí" if p["is_active"] else "No"
            tabla.insert("", "end", values=(p["id"], p["name"], p["price"], estado))

    def guardar_producto():
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        try:
            precio = float(precio)
            create_product(nombre, precio)
            cargar_productos()
            entry_nombre.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Precio inválido")

    def editar_producto():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return
        datos = tabla.item(seleccionado)["values"]
        product_id = datos[0]
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        try:
            precio = float(precio)
            update_product(product_id, nombre, precio)
            cargar_productos()
        except ValueError:
            messagebox.showerror("Error", "Precio inválido")

    def eliminar_producto():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return
        datos = tabla.item(seleccionado)["values"]
        product_id = datos[0]
        confirm = messagebox.askyesno("Confirmar", "¿Eliminar este producto?")
        if confirm:
            delete_product(product_id)
            cargar_productos()

    def cambiar_estado():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return
        datos = tabla.item(seleccionado)["values"]
        product_id = datos[0]
        estado_actual = datos[3] == "Sí"
        toggle_product_status(product_id, not estado_actual)
        cargar_productos()

    # --- Botones ---
    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(fill="x", padx=10, pady=5)

    ttk.Button(frame_botones, text="Guardar", command=guardar_producto).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Editar", command=editar_producto).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar_producto).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Activar/Desactivar", command=cambiar_estado).pack(side="left", padx=5)
    # Botón salir para cerrar la ventana
    ttk.Button(frame_botones, text="Salir", command=ventana.destroy).pack(side="right", padx=5)

    cargar_productos()