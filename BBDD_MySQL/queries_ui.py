import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
from gui import apply_style, center_window


def abrir_ventana_consultas():
    ventana = tk.Toplevel()
    ventana.title("Consultas - MyShop")
    apply_style(ventana)
    center_window(ventana, width=900, height=600)

    frame_top = ttk.Frame(ventana)
    frame_top.pack(fill='x', padx=10, pady=10)

    ttk.Label(frame_top, text="Tipo de consulta:").grid(row=0, column=0, padx=5, pady=5)
    combo = ttk.Combobox(frame_top, state='readonly', values=[
        "Buscar cliente por nombre",
        "Buscar cliente por email",
        "Buscar cliente por ID",
        "Listar todos los clientes",
        "Buscar pedido por ID",
        "Listar pedidos por cliente",
        "Listar productos activos",
        "Listar productos inactivos",
        "Listar todos los productos"
    ], width=40)
    combo.grid(row=0, column=1, padx=5, pady=5)

    entry_param = ttk.Entry(frame_top, width=40)
    entry_param.grid(row=0, column=2, padx=5, pady=5)

    frame_tabla = ttk.Frame(ventana)
    frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)

    tabla = ttk.Treeview(frame_tabla, show='headings')
    tabla.pack(fill='both', expand=True)

    def ejecutar_consulta():
        tipo = combo.get()
        param = entry_param.get()
        tabla.delete(*tabla.get_children())
        if not tipo:
            messagebox.showwarning("Atención", "Selecciona un tipo de consulta")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return
        cursor = conn.cursor(dictionary=True)
        try:
            if tipo == "Buscar cliente por nombre":
                sql = "SELECT * FROM customers WHERE name LIKE %s"
                cursor.execute(sql, (f"%{param}%",))
                rows = cursor.fetchall()
                cols = ["id", "name", "email", "phone"]
            elif tipo == "Buscar cliente por email":
                sql = "SELECT * FROM customers WHERE email LIKE %s"
                cursor.execute(sql, (f"%{param}%",))
                rows = cursor.fetchall()
                cols = ["id", "name", "email", "phone"]
            elif tipo == "Buscar cliente por ID":
                sql = "SELECT * FROM customers WHERE id = %s"
                cursor.execute(sql, (param,))
                rows = cursor.fetchall()
                cols = ["id", "name", "email", "phone"]
            elif tipo == "Listar todos los clientes":
                sql = "SELECT * FROM customers"
                cursor.execute(sql)
                rows = cursor.fetchall()
                cols = ["id", "name", "email", "phone"]
            elif tipo == "Buscar pedido por ID":
                sql = "SELECT * FROM orders WHERE id = %s"
                cursor.execute(sql, (param,))
                rows = cursor.fetchall()
                cols = ["id", "customer_id", "total", "created_at"]
            elif tipo == "Listar pedidos por cliente":
                sql = "SELECT * FROM orders WHERE customer_id = %s"
                cursor.execute(sql, (param,))
                rows = cursor.fetchall()
                cols = ["id", "customer_id", "total", "created_at"]
            elif tipo == "Listar productos activos":
                sql = "SELECT * FROM products WHERE is_active=1"
                cursor.execute(sql)
                rows = cursor.fetchall()
                cols = ["id", "name", "price", "is_active"]
            elif tipo == "Listar productos inactivos":
                sql = "SELECT * FROM products WHERE is_active=0"
                cursor.execute(sql)
                rows = cursor.fetchall()
                cols = ["id", "name", "price", "is_active"]
            elif tipo == "Listar todos los productos":
                sql = "SELECT * FROM products"
                cursor.execute(sql)
                rows = cursor.fetchall()
                cols = ["id", "name", "price", "is_active"]
            else:
                rows = []
                cols = []

            tabla.config(columns=cols)
            for c in cols:
                tabla.heading(c, text=c.capitalize())

            for r in rows:
                vals = tuple(r.get(col) for col in cols)
                tabla.insert('', 'end', values=vals)
        except Exception as e:
            messagebox.showerror("Error", f"Error en la consulta: {e}")
        finally:
            cursor.close()
            conn.close()

    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(fill='x', padx=10, pady=5)

    ttk.Button(frame_botones, text="Ejecutar", command=ejecutar_consulta).pack(side='left', padx=5)
    ttk.Button(frame_botones, text="Salir", command=ventana.destroy).pack(side='right', padx=5)
