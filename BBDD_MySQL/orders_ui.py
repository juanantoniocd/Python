import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from orders import create_order, add_order_item, update_order_total, list_orders_by_customer, get_order_details, delete_order, get_order_total, delete_order_item, update_order_item
from customers import list_customers
from products import list_products
from gui import apply_style, center_window

def abrir_ventana_pedidos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Pedidos")
    apply_style(ventana)
    center_window(ventana, width=900, height=700)

    # --- Selección de cliente ---
    frame_cliente = ttk.LabelFrame(ventana, text="Cliente")
    frame_cliente.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_cliente, text="Seleccionar cliente:").grid(row=0, column=0, padx=5, pady=5)
    combo_clientes = ttk.Combobox(frame_cliente, width=40, state="readonly")
    combo_clientes.grid(row=0, column=1, padx=5, pady=5)

    clientes = list_customers()
    clientes_dict = {f"{c['name']} ({c['email']})": c["id"] for c in clientes}
    combo_clientes["values"] = list(clientes_dict.keys())

    # --- Crear pedido ---
    frame_pedido = ttk.LabelFrame(ventana, text="Nuevo Pedido")
    frame_pedido.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_pedido, text="Producto:").grid(row=0, column=0, padx=5, pady=5)
    combo_productos = ttk.Combobox(frame_pedido, width=30, state="readonly")
    combo_productos.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_pedido, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
    entry_cantidad = ttk.Entry(frame_pedido, width=10)
    entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

    productos = list_products()
    # mantener todos los productos en la lista, pero indicamos su estado en el diccionario
    productos_dict = {p["name"]: (p["id"], p["price"], bool(p.get("is_active", False))) for p in productos}
    # solo mostrar activos en el combobox
    combo_productos["values"] = [p["name"] for p in productos if p.get("is_active")]
    combo_productos["values"] = list(productos_dict.keys())

    pedido_actual = {"id": None, "items": []}

    def crear_pedido():
        cliente_nombre = combo_clientes.get()
        if not cliente_nombre:
            messagebox.showwarning("Atención", "Selecciona un cliente")
            return
        cliente_id = clientes_dict[cliente_nombre]
        pedido_id = create_order(cliente_id)
        pedido_actual["id"] = pedido_id
        pedido_actual["items"] = []
        messagebox.showinfo("Pedido creado", f"ID del pedido: {pedido_id}")
        cargar_pedidos(cliente_id)
        cargar_items_pedido(pedido_id)

    def agregar_item():
        if not pedido_actual["id"]:
            messagebox.showwarning("Atención", "Primero crea un pedido")
            return
        producto_nombre = combo_productos.get()
        cantidad = entry_cantidad.get()
        if not producto_nombre or not cantidad:
            messagebox.showwarning("Atención", "Completa todos los campos")
            return
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que 0")
                return
            product_id, unit_price, is_active = productos_dict[producto_nombre]
            if not is_active:
                messagebox.showerror("Error", "No se puede agregar un producto inactivo")
                return
            add_order_item(pedido_actual["id"], product_id, cantidad, unit_price)
            update_order_total(pedido_actual["id"])
            cargar_items_pedido(pedido_actual["id"])
            messagebox.showinfo("Ítem agregado", f"{cantidad} x {producto_nombre}")
            entry_cantidad.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")

    ttk.Button(frame_pedido, text="Crear Pedido", command=crear_pedido).grid(row=2, column=0, padx=5, pady=10)
    ttk.Button(frame_pedido, text="Agregar Ítem", command=agregar_item).grid(row=2, column=1, padx=5, pady=10)

    # --- Tabla de pedidos ---
    frame_tabla = ttk.LabelFrame(ventana, text="Pedidos del Cliente")
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    tabla_pedidos = ttk.Treeview(frame_tabla, columns=("id", "total", "created_at"), show="headings")
    tabla_pedidos.heading("id", text="ID")
    tabla_pedidos.heading("total", text="Total")
    tabla_pedidos.heading("created_at", text="Fecha")
    tabla_pedidos.pack(fill="both", expand=True)

    # --- Tabla de ítems del pedido actual ---
    frame_items = ttk.LabelFrame(ventana, text="Ítems del Pedido")
    frame_items.pack(fill="both", expand=True, padx=10, pady=10)

    tabla_items = ttk.Treeview(frame_items, columns=("id", "name", "quantity", "unit_price", "subtotal"), show="headings")
    tabla_items.heading("id", text="ID")
    tabla_items.heading("name", text="Producto")
    tabla_items.heading("quantity", text="Cantidad")
    tabla_items.heading("unit_price", text="Precio Unit.")
    tabla_items.heading("subtotal", text="Subtotal")
    tabla_items.pack(fill="both", expand=True)

    label_total_var = tk.StringVar(value="$0.00")
    label_total = ttk.Label(ventana, textvariable=label_total_var, font=("Arial", 12, "bold"))
    label_total.pack(pady=5)

    def cargar_items_pedido(order_id):
        tabla_items.delete(*tabla_items.get_children())
        detalles = get_order_details(order_id)
        for d in detalles:
            subtotal = d["quantity"] * float(d["unit_price"])
            tabla_items.insert("", "end", values=(d["id"], d["name"], d["quantity"], f"${d['unit_price']:.2f}", f"${subtotal:.2f}"))
        total = get_order_total(order_id)
        label_total_var.set(f"Total: ${total:.2f}")

    def editar_cantidad_item():
        seleccionado = tabla_items.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un ítem del pedido")
            return
        datos = tabla_items.item(seleccionado)["values"]
        item_id = datos[0]
        cantidad_actual = int(datos[2])
        nuevo = simpledialog.askinteger("Editar cantidad", "Nueva cantidad:", initialvalue=cantidad_actual, minvalue=0)
        if nuevo is None:
            return
        # si nuevo == 0 se eliminará el ítem
        update_order_item(item_id, nuevo)
        if pedido_actual["id"]:
            cargar_items_pedido(pedido_actual["id"])

    # permitir editar con doble click
    tabla_items.bind("<Double-1>", lambda e: editar_cantidad_item())

    def cargar_pedidos(cliente_id):
        tabla_pedidos.delete(*tabla_pedidos.get_children())
        pedidos = list_orders_by_customer(cliente_id)
        for p in pedidos:
            tabla_pedidos.insert("", "end", values=(p["id"], f"${p['total']:.2f}", p["created_at"]))

    def ver_detalle():
        seleccionado = tabla_pedidos.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un pedido")
            return
        pedido_id = tabla_pedidos.item(seleccionado)["values"][0]
        detalles = get_order_details(pedido_id)
        texto = "\n".join([f"{d['quantity']} x {d['name']} @ ${d['unit_price']:.2f}" for d in detalles])
        messagebox.showinfo(f"Detalle del pedido {pedido_id}", texto)

    def eliminar_pedido():
        seleccionado = tabla_pedidos.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un pedido")
            return
        pedido_id = tabla_pedidos.item(seleccionado)["values"][0]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar pedido {pedido_id}?")
        if confirm:
            delete_order(pedido_id)
            cliente_nombre = combo_clientes.get()
            cliente_id = clientes_dict[cliente_nombre]
            cargar_pedidos(cliente_id)

    def eliminar_item():
        seleccionado = tabla_items.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un ítem del pedido")
            return
        datos = tabla_items.item(seleccionado)["values"]
        item_id = datos[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar ítem {item_id}?")
        if confirm:
            delete_order_item(item_id)
            if pedido_actual["id"]:
                cargar_items_pedido(pedido_actual["id"])

    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(fill="x", padx=10, pady=5)

    ttk.Button(frame_botones, text="Ver Detalle", command=ver_detalle).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Eliminar Pedido", command=eliminar_pedido).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Eliminar Ítem", command=eliminar_item).pack(side="left", padx=5)
    # Botón salir
    ttk.Button(frame_botones, text="Salir", command=ventana.destroy).pack(side="right", padx=5)