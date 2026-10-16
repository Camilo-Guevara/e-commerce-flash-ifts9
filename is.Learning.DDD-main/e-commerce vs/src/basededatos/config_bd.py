"""Conexión MySQL del proyecto académico mediante variables de entorno."""
import os

import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    """Devuelve una conexión activa o lanza un error explícito.

    Nunca devuelve None, para evitar fallos secundarios al llamar .cursor().
    MYSQL_PASSWORD puede estar vacía únicamente si está definida explícitamente
    (por compatibilidad con algunos servidores de desarrollo locales).
    """
    usuario = os.environ.get("MYSQL_USER", "").strip()
    password = os.environ.get("MYSQL_PASSWORD")
    if not usuario or password is None:
        raise RuntimeError("Configura MYSQL_USER y MYSQL_PASSWORD en el entorno")

    try:
        conexion = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST") or "localhost",
            user=usuario,
            password=password,
            database=os.environ.get("MYSQL_DATABASE") or "ecommerce_db",
        )
        if not conexion.is_connected():
            conexion.close()
            raise RuntimeError("MySQL no devolvió una conexión activa")
        return conexion
    except Error as error:
        raise RuntimeError(
            "No se pudo conectar a MySQL; verifica el servicio y la configuración"
        ) from error
