"""Tests of MySQL configuration; the tests do not access a real database."""
import os
import unittest
from unittest.mock import MagicMock, patch

from mysql.connector import Error
from src.basededatos.config_bd import obtener_conexion


MODULE = "src.basededatos.config_bd.mysql.connector.connect"
TEST_ENV = {
    "MYSQL_HOST": "db-local",
    "MYSQL_USER": "usuario_prueba",
    "MYSQL_PASSWORD": "solo-prueba-no-secreto",
    "MYSQL_DATABASE": "db_prueba",
}


class ConexionMySQLTests(unittest.TestCase):
    def test_sin_usuario_no_intenta_conectarse(self):
        env = {"MYSQL_PASSWORD": "demo"}
        with patch.dict(os.environ, env, clear=True), patch(MODULE) as connect:
            with self.assertRaisesRegex(RuntimeError, "MYSQL_USER"):
                obtener_conexion()
            connect.assert_not_called()

    def test_sin_password_no_intenta_conectarse(self):
        env = {"MYSQL_USER": "usuario_prueba"}
        with patch.dict(os.environ, env, clear=True), patch(MODULE) as connect:
            with self.assertRaisesRegex(RuntimeError, "MYSQL_PASSWORD"):
                obtener_conexion()
            connect.assert_not_called()

    def test_usuario_con_espacios_se_rechaza(self):
        env = {"MYSQL_USER": "   ", "MYSQL_PASSWORD": "demo"}
        with patch.dict(os.environ, env, clear=True), patch(MODULE) as connect:
            with self.assertRaises(RuntimeError):
                obtener_conexion()
            connect.assert_not_called()

    def test_conecta_con_variables_de_entorno(self):
        conexion = MagicMock()
        conexion.is_connected.return_value = True
        with patch.dict(os.environ, TEST_ENV, clear=True):
            with patch(MODULE, return_value=conexion) as connect:
                self.assertIs(obtener_conexion(), conexion)
                connect.assert_called_once_with(
                    host="db-local",
                    user="usuario_prueba",
                    password="solo-prueba-no-secreto",
                    database="db_prueba",
                )
                conexion.close.assert_not_called()

    def test_host_y_base_predeterminados(self):
        env = {"MYSQL_USER": "dev", "MYSQL_PASSWORD": "test"}
        conexion = MagicMock()
        conexion.is_connected.return_value = True
        with patch.dict(os.environ, env, clear=True), patch(
            MODULE, return_value=conexion
        ) as connect:
            self.assertIs(obtener_conexion(), conexion)
            connect.assert_called_once_with(
                host="localhost",
                user="dev",
                password="test",
                database="ecommerce_db",
            )

    def test_password_vacio_explicito_es_valido_para_desarrollo(self):
        env = {"MYSQL_USER": "local_test_user", "MYSQL_PASSWORD": ""}
        conexion = MagicMock()
        conexion.is_connected.return_value = True
        with patch.dict(os.environ, env, clear=True), patch(
            MODULE, return_value=conexion
        ) as connect:
            self.assertIs(obtener_conexion(), conexion)
            self.assertEqual(connect.call_args.kwargs["password"], "")

    def test_conexion_inactiva_se_cierra_y_falla(self):
        conexion = MagicMock()
        conexion.is_connected.return_value = False
        with patch.dict(os.environ, TEST_ENV, clear=True), patch(
            MODULE, return_value=conexion
        ):
            with self.assertRaisesRegex(RuntimeError, "conexión activa"):
                obtener_conexion()
            conexion.close.assert_called_once()

    def test_error_del_conector_se_sanitiza_y_conserva_causa(self):
        with patch.dict(os.environ, TEST_ENV, clear=True), patch(
            MODULE, side_effect=Error("contraseña de prueba en mensaje")
        ):
            with self.assertRaises(RuntimeError) as context:
                obtener_conexion()
        self.assertIn("No se pudo conectar a MySQL", str(context.exception))
        self.assertNotIn("contraseña de prueba", str(context.exception))
        self.assertIsInstance(context.exception.__cause__, Error)


if __name__ == "__main__":
    unittest.main()
