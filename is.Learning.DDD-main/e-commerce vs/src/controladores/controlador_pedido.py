from modelos.pedido import Pedido

class ControladorPedido:
    def crear_pedido(self, usuario, productos):
        pedido = Pedido(idUsuario=usuario.id, estado="Abierto", total=0)
        pedido.crear()
        return pedido

    def guardar_en_bd(self, pedido):
        pedido.crear()

    def calcular_total(self, pedido):
        return pedido.calcular_total()

    def procesar_pago(self, pedido, monto):
        pedido.procesar_pago(monto)

    def cancelar_pedido(self, pedido):
        pedido.cancelar()

    def finalizar_pedido(self, pedido):
        pedido.finalizar()
