from db import get_connection

# Crear cliente
def create_customer(name: str, email: str, phone: str = None):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"
        valores = (name, email, phone)
        cursor.execute(sql, valores)
        conexion.commit()
        print("✅ Cliente agregado correctamente")
        cursor.close()
        conexion.close()

# Listar todos los clientes
def list_customers():
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados

# Actualizar cliente
def update_customer(customer_id: int, name: str, email: str, phone: str):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = "UPDATE customers SET name=%s, email=%s, phone=%s WHERE id=%s"
        valores = (name, email, phone, customer_id)
        cursor.execute(sql, valores)
        conexion.commit()
        print("✅ Cliente actualizado")
        cursor.close()
        conexion.close()

# Eliminar cliente (solo si no tiene pedidos)
def delete_customer(customer_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        try:
            sql = "DELETE FROM customers WHERE id=%s"
            cursor.execute(sql, (customer_id,))
            conexion.commit()
            print("✅ Cliente eliminado")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar el cliente: {e}")
        finally:
            cursor.close()
            conexion.close()
