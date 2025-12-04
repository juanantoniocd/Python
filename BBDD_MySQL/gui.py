import tkinter as tk
from tkinter import ttk

def apply_style(root: tk.Tk | tk.Toplevel):
    """Aplica un estilo simple: fondo blanco y texto negro para ttk y para la ventana."""
    style = ttk.Style(root)
    try:
        style.theme_use('default')
    except Exception:
        pass

    style.configure('TLabel', background='white', foreground='black')
    style.configure('TFrame', background='white')
    style.configure('TButton', background='white', foreground='black')
    style.configure('TCombobox', fieldbackground='white', background='white', foreground='black')
    style.configure('Treeview', background='white', fieldbackground='white', foreground='black')
    style.configure('Treeview.Heading', background='white', foreground='black')

    # Aseguramos que la ventana tenga fondo blanco
    try:
        root.configure(bg='white')
    except Exception:
        pass


def center_window(win: tk.Tk | tk.Toplevel, width: int | None = None, height: int | None = None, frac: float = 0.6, max_w: int = 1100, max_h: int = 800):
    """Centra la ventana en pantalla.

    - Si width/height son None se toma un porcentaje de la pantalla (frac).
    - Se aplican tamaños máximos para que no ocupe toda la pantalla.
    - Se fija un tamaño mínimo razonable.
    """
    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    if width is None:
        width = int(screen_w * frac)
    if height is None:
        height = int(screen_h * frac)

    width = min(width, max_w)
    height = min(height, max_h)

    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")
    # Tamaños mínimos para asegurar que se vean los botones
    try:
        win.minsize(480, 320)
    except Exception:
        pass
