from database.db_config import obtener_conexion

class ItemPedido:
    def __init__(self, idPedido, idProducto, cantidad, precioUnitario):
        self.idPedido = idPedido
        self.idProducto = idProducto
        self.cantidad = cantidad
        self.precioUnitario = precioUnitario

    def agregar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO ItemPedido (idPedido, idProducto, cantidad, precioUnitario)
            VALUES (%s, %s, %s, %s)
        """, (self.idPedido, self.idProducto, self.cantidad, self.precioUnitario))
        conexion.commit()
        conexion.close()