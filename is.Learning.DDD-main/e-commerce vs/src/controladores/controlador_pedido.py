from modelos.pedido import Pedido


class ControladorPedido:
    def crear_pedido(self, id_pedido, productos):
        """Crea un pedido en memoria a partir de una lista de (Producto, cantidad)."""
        return Pedido(id_pedido=id_pedido, productos=productos)

    def calcular_total(self, pedido: Pedido):
        return pedido.total

    def procesar_pago(self, pedido: Pedido, monto: float):
        # Para pagar, el pedido debe pasar a "en proceso" primero
        if pedido.estado == "abierto":
            pedido.marcar_en_proceso()
        pedido.procesar_pago(monto)

    def cancelar_pedido(self, pedido: Pedido):
        pedido.cancelar_pedido()

    def finalizar_pedido(self, pedido: Pedido):
        pedido.finalizar_pedido()

