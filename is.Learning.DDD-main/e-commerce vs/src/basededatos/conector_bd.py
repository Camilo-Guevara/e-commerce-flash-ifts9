import hashlib
import secrets
from typing import Optional

from .config_bd import conectar_bd
from ..modelos.usuario import Usuario


class RepositorioUsuario:
    """Operaciones de persistencia para usuarios en MySQL."""

    @staticmethod
    def insertar_usuario(correo: str, contrasena: str) -> Usuario:
        db = conectar_bd()
        cursor = db.cursor()
        try:
            salt = secrets.token_hex(16)
            password_hash = hashlib.sha256((contrasena + salt).encode()).hexdigest()
            cursor.execute(
                """
                INSERT INTO usuarios (correo, password_salt, password_hash)
                VALUES (%s, %s, %s)
                """,
                (correo, salt, password_hash),
            )
            db.commit()
            user_id = cursor.lastrowid

            # Construir instancia de dominio con valores persistidos
            usuario = Usuario(user_id, correo, "dummy")
            usuario.passwordSalt = salt
            usuario.passwordHash = password_hash
            return usuario
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def obtener_por_correo(correo: str) -> Optional[Usuario]:
        db = conectar_bd()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT id, correo, password_salt, password_hash FROM usuarios WHERE correo = %s",
                (correo,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            user_id, correo_db, salt, password_hash = row
            usuario = Usuario(user_id, correo_db, "dummy")
            usuario.passwordSalt = salt
            usuario.passwordHash = password_hash
            return usuario
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def actualizar_correo(user_id: int, nuevo_correo: str) -> None:
        db = conectar_bd()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET correo = %s WHERE id = %s",
                (nuevo_correo, user_id),
            )
            db.commit()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def actualizar_contrasena(user_id: int, nueva_contrasena: str) -> None:
        db = conectar_bd()
        cursor = db.cursor()
        try:
            salt = secrets.token_hex(16)
            password_hash = hashlib.sha256((nueva_contrasena + salt).encode()).hexdigest()
            cursor.execute(
                "UPDATE usuarios SET password_salt = %s, password_hash = %s WHERE id = %s",
                (salt, password_hash, user_id),
            )
            db.commit()
        finally:
            cursor.close()
            db.close()
