from db import get_connection

# Crear producto
def create_product(name: str, price: float):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = "INSERT INTO products (name, price) VALUES (%s, %s)"
        cursor.execute(sql, (name, price))
        conexion.commit()
        print("✅ Producto agregado correctamente")
        cursor.close()
        conexion.close()

# Listar todos los productos
def list_products():
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos

# Actualizar producto
def update_product(product_id: int, name: str, price: float):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = "UPDATE products SET name=%s, price=%s WHERE id=%s"
        cursor.execute(sql, (name, price, product_id))
        conexion.commit()
        print("✅ Producto actualizado")
        cursor.close()
        conexion.close()

# Cambiar disponibilidad (activar/desactivar)
def toggle_product_status(product_id: int, is_active: bool):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = "UPDATE products SET is_active=%s WHERE id=%s"
        cursor.execute(sql, (int(is_active), product_id))
        conexion.commit()
        estado = "activado" if is_active else "desactivado"
        print(f"✅ Producto {estado}")
        cursor.close()
        conexion.close()

# Eliminar producto (solo si no está en pedidos)
def delete_product(product_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        try:
            sql = "DELETE FROM products WHERE id=%s"
            cursor.execute(sql, (product_id,))
            conexion.commit()
            print("✅ Producto eliminado")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar el producto: {e}")
        finally:
            cursor.close()
            conexion.close()