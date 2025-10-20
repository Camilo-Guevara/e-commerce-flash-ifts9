import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Devuelve una conexión a la base de datos MySQL"""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TU_PASSWORD',   # reemplazá con tu contraseña real
            database='ecommerce_db'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print("Error al conectar con MySQL:", e)
        return None

#⚠️ Si usás XAMPP o WAMP, asegurate de que el servicio de MySQL esté iniciado.
