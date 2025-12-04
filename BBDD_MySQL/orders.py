from db import get_connection

# Crear pedido vacío para un cliente
def create_order(customer_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = "INSERT INTO orders (customer_id) VALUES (%s)"
        cursor.execute(sql, (customer_id,))
        conexion.commit()
        order_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        print(f"✅ Pedido creado con ID {order_id}")
        return order_id

# Agregar ítem al pedido
def add_order_item(order_id: int, product_id: int, quantity: int, unit_price: float):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Si el mismo producto ya existe en el pedido, aumentamos la cantidad
            sql_check = "SELECT id, quantity FROM order_items WHERE order_id=%s AND product_id=%s"
            cursor.execute(sql_check, (order_id, product_id))
            existing = cursor.fetchone()
            if existing:
                item_id = existing[0]
                nueva_cantidad = existing[1] + quantity
                sql_update = "UPDATE order_items SET quantity=%s, unit_price=%s WHERE id=%s"
                cursor.execute(sql_update, (nueva_cantidad, unit_price, item_id))
            else:
                sql = (
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price)"
                    " VALUES (%s, %s, %s, %s)"
                )
                cursor.execute(sql, (order_id, product_id, quantity, unit_price))

            conexion.commit()
            print("✅ Ítem agregado/actualizado en el pedido")
        except Exception as e:
            print(f"⚠️ Error al agregar ítem: {e}")
        finally:
            cursor.close()
            conexion.close()

# Calcular y actualizar total del pedido
def update_order_total(order_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT SUM(quantity * unit_price) FROM order_items
            WHERE order_id = %s
        """
        cursor.execute(sql, (order_id,))
        total = cursor.fetchone()[0] or 0.00

        sql_update = "UPDATE orders SET total = %s WHERE id = %s"
        cursor.execute(sql_update, (total, order_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        print(f"✅ Total actualizado: ${total:.2f}")

# Listar pedidos por cliente
def list_orders_by_customer(customer_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT * FROM orders WHERE customer_id = %s"
        cursor.execute(sql, (customer_id,))
        pedidos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return pedidos

# Ver detalle de un pedido
def get_order_details(order_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT oi.id, p.name, oi.quantity, oi.unit_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """
        cursor.execute(sql, (order_id,))
        detalles = cursor.fetchall()
        cursor.close()
        conexion.close()
        return detalles


def get_order_total(order_id: int):
    """Devuelve el total del pedido (usa SUM sobre order_items)."""
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT SUM(quantity * unit_price) FROM order_items
            WHERE order_id = %s
        """
        cursor.execute(sql, (order_id,))
        total = cursor.fetchone()[0] or 0.00
        # También actualizamos la tabla orders para mantener consistencia
        try:
            sql_update = "UPDATE orders SET total = %s WHERE id = %s"
            cursor.execute(sql_update, (total, order_id))
            conexion.commit()
        except Exception:
            pass
        cursor.close()
        conexion.close()
        return float(total)


def delete_order_item(item_id: int):
    """Elimina un ítem del pedido y actualiza el total del pedido asociado."""
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Obtener order_id antes de borrar
            cursor.execute("SELECT order_id FROM order_items WHERE id = %s", (item_id,))
            row = cursor.fetchone()
            if row:
                order_id = row[0]
                cursor.execute("DELETE FROM order_items WHERE id = %s", (item_id,))
                conexion.commit()
                # Actualizar total del pedido
                update_order_total(order_id)
                print(f"✅ Ítem {item_id} eliminado del pedido {order_id}")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar el ítem: {e}")
        finally:
            cursor.close()
            conexion.close()


def update_order_item(item_id: int, new_quantity: int):
    """Actualiza la cantidad de un ítem del pedido. Si new_quantity <= 0 elimina el ítem."""
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT order_id FROM order_items WHERE id = %s", (item_id,))
            row = cursor.fetchone()
            if not row:
                return
            order_id = row[0]
            if new_quantity <= 0:
                cursor.execute("DELETE FROM order_items WHERE id = %s", (item_id,))
            else:
                cursor.execute("UPDATE order_items SET quantity = %s WHERE id = %s", (new_quantity, item_id))
            conexion.commit()
            # actualizar total del pedido
            update_order_total(order_id)
            print(f"✅ Ítem {item_id} actualizado (cantidad={new_quantity})")
        except Exception as e:
            print(f"⚠️ Error actualizando ítem: {e}")
        finally:
            cursor.close()
            conexion.close()

# Eliminar pedido (y sus ítems)
def delete_order(order_id: int):
    conexion = get_connection()
    if conexion:
        cursor = conexion.cursor()
        try:
            sql = "DELETE FROM orders WHERE id = %s"
            cursor.execute(sql, (order_id,))
            conexion.commit()
            print("✅ Pedido eliminado")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar el pedido: {e}")
        finally:
            cursor.close()
            conexion.close()