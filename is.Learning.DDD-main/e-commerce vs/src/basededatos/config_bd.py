"""Conexion MySQL del proyecto academico, configurada mediante variables de entorno."""
import os

import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    """Devuelve una conexion MySQL o None si el servidor informa un error."""
    usuario = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    if not usuario or password is None:
        raise RuntimeError("Configura MYSQL_USER y MYSQL_PASSWORD en el entorno")

    try:
        conexion = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=usuario,
            password=password,
            database=os.environ.get("MYSQL_DATABASE", "ecommerce_db"),
        )
        if conexion.is_connected():
            return conexion
        conexion.close()
    except Error as e:
        print("Error al conectar con MySQL:", e)
    return None
