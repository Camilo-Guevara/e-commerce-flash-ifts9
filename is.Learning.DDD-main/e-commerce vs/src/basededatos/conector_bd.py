import hashlib # Para hashing de contraseñas
import secrets # Para generar salt aleatorio
from typing import Optional 

from .config_bd import obtener_conexion 
from ..modelos.usuario import Usuario 


class RepositorioUsuario:
    """Operaciones de persistencia para la tabla Usuario."""

    @staticmethod
    def insertar_usuario(correo: str, contrasena: str, rol: str = "Cliente") -> Usuario:
        con = obtener_conexion() # Obtener conexión a BD
        cur = con.cursor() 
        try:
            # Usa el mismo algoritmo que el modelo Usuario (sha512 + salt)
            hashed, salt = Usuario.hash_password(contrasena)
            cur.execute(
                """
                INSERT INTO Usuario (correo, rol, passwordHash, passwordSalt)
                VALUES (%s, %s, %s, %s)
                """,
                (correo, rol, hashed, salt),
            ) 
            con.commit() # Confirmar cambios
            user_id = cur.lastrowid
            return Usuario(id=user_id, correo=correo, rol=rol, passwordHash=hashed, passwordSalt=salt)
        finally:
            cur.close()
            con.close()

    @staticmethod
    def obtener_por_correo(correo: str) -> Optional[Usuario]: # Devuelve Usuario o None
        con = obtener_conexion()
        cur = con.cursor(dictionary=True) # Diccionario para mapear columnas a atributos
        try:
            cur.execute( # Consulta parametrizada para evitar SQL injection
                "SELECT * FROM Usuario WHERE correo = %s",
                (correo,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return Usuario(**row)
        finally:
            cur.close()
            con.close()

    @staticmethod
    def actualizar_correo(user_id: int, nuevo_correo: str) -> None:
        con = obtener_conexion()
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE Usuario SET correo = %s WHERE id = %s",
                (nuevo_correo, user_id),
            )
            con.commit()
        finally:
            cur.close()
            con.close()

    @staticmethod
    def actualizar_contrasena(user_id: int, nueva_contrasena: str) -> None:
        con = obtener_conexion()
        cur = con.cursor()
        try:
            hashed, salt = Usuario.hash_password(nueva_contrasena)
            cur.execute(
                "UPDATE Usuario SET passwordHash = %s, passwordSalt = %s WHERE id = %s",
                (hashed, salt, user_id),
            )
            con.commit()
        finally:
            cur.close()
            con.close()

