import tkinter as tk
from tkinter import ttk
from customers_ui import abrir_ventana_clientes
from products_ui import abrir_ventana_productos
from orders_ui import abrir_ventana_pedidos
from queries_ui import abrir_ventana_consultas
from gui import apply_style, center_window


def main():
    root = tk.Tk()
    root.title("Gestión MyShop")
    # Aplicar estilo y centrar la ventana principal
    apply_style(root)
    center_window(root, width=700, height=500)
    root.resizable(False, False)

    ttk.Label(root, text="Menú Principal", font=("Arial", 18)).pack(pady=20)

    ttk.Button(root, text="Clientes", width=36, command=abrir_ventana_clientes).pack(pady=6)
    ttk.Button(root, text="Productos", width=36, command=abrir_ventana_productos).pack(pady=6)
    ttk.Button(root, text="Pedidos", width=36, command=abrir_ventana_pedidos).pack(pady=6)
    ttk.Button(root, text="Consultas", width=36, command=abrir_ventana_consultas).pack(pady=6)

    ttk.Button(root, text="Salir", width=36, command=root.quit).pack(pady=18)
    root.mainloop()

if __name__ == "__main__":
    main()