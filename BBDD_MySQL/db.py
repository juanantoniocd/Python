import mysql.connector
from mysql.connector import Error

# Función para obtener conexión a la base de datos
def get_connection():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Jc2025mS$03",
            database="myshop",
            port=3306
        )
        return conexion
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return None
