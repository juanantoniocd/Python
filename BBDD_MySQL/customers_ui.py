import tkinter as tk
from tkinter import ttk, messagebox
from customers import create_customer, list_customers, update_customer, delete_customer
from gui import apply_style, center_window

def abrir_ventana_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    # aplicar estilo y centrar ventana
    apply_style(ventana)
    center_window(ventana, width=800, height=600)

    # --- Formulario ---
    frame_form = ttk.LabelFrame(ventana, text="Agregar / Editar Cliente")
    frame_form.pack(fill="x", padx=10, pady=10)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = ttk.Entry(frame_form, width=30)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
    entry_email = ttk.Entry(frame_form, width=30)
    entry_email.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
    entry_telefono = ttk.Entry(frame_form, width=30)
    entry_telefono.grid(row=2, column=1, padx=5, pady=5)

    # --- Tabla ---
    tabla = ttk.Treeview(ventana, columns=("id", "name", "email", "phone"), show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("name", text="Nombre")
    tabla.heading("email", text="Email")
    tabla.heading("phone", text="Teléfono")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_clientes():
        tabla.delete(*tabla.get_children())
        for c in list_customers():
            tabla.insert("", "end", values=(c["id"], c["name"], c["email"], c["phone"]))

    def guardar_cliente():
        nombre = entry_nombre.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        if not nombre or not email:
            messagebox.showwarning("Atención", "Nombre y email son obligatorios")
            return
        create_customer(nombre, email, telefono)
        cargar_clientes()
        entry_nombre.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

    def editar_cliente():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente")
            return
        datos = tabla.item(seleccionado)["values"]
        cliente_id = datos[0]
        nombre = entry_nombre.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        update_customer(cliente_id, nombre, email, telefono)
        cargar_clientes()

    def eliminar_cliente():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente")
            return
        datos = tabla.item(seleccionado)["values"]
        cliente_id = datos[0]
        confirm = messagebox.askyesno("Confirmar", "¿Eliminar este cliente?")
        if confirm:
            delete_customer(cliente_id)
            cargar_clientes()

    # --- Botones ---
    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(fill="x", padx=10, pady=5)

    ttk.Button(frame_botones, text="Guardar", command=guardar_cliente).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Editar", command=editar_cliente).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar_cliente).pack(side="left", padx=5)
    # Botón salir para cerrar la ventana actual
    ttk.Button(frame_botones, text="Salir", command=ventana.destroy).pack(side="right", padx=5)

    cargar_clientes()