"""Pruebas de configuracion local que no requieren servidor MySQL."""
import os
import unittest
from unittest.mock import MagicMock, patch

from src.basededatos.config_bd import obtener_conexion


class ConexionMySQLTests(unittest.TestCase):
    def test_falta_configuracion_no_se_conecta(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("src.basededatos.config_bd.mysql.connector.connect") as connect:
                with self.assertRaises(RuntimeError):
                    obtener_conexion()
                connect.assert_not_called()

    def test_conecta_con_variables_de_entorno(self):
        variables = {
            "MYSQL_HOST": "db-local",
            "MYSQL_USER": "usuario_prueba",
            "MYSQL_PASSWORD": "solo-prueba-no-secreto",
            "MYSQL_DATABASE": "db_prueba",
        }
        conexion = MagicMock()
        conexion.is_connected.return_value = True
        with patch.dict(os.environ, variables, clear=True):
            with patch("src.basededatos.config_bd.mysql.connector.connect", return_value=conexion) as connect:
                self.assertIs(obtener_conexion(), conexion)
                connect.assert_called_once_with(
                    host="db-local",
                    user="usuario_prueba",
                    password="solo-prueba-no-secreto",
                    database="db_prueba",
                )


if __name__ == "__main__":
    unittest.main()
