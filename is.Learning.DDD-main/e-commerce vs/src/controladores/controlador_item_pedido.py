from modelos.item_pedido import ItemPedido

class ControladorItemPedido:
    def crear_item(self, pedido, producto, cantidad):
        return ItemPedido(pedido.id, producto.id, cantidad, producto.precio)

    def guardar_en_bd(self, item_pedido):
        item_pedido.agregar()
