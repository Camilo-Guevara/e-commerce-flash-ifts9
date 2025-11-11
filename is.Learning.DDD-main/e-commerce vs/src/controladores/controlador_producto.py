from modelos.producto import Producto


class ControladorProducto:
    def __init__(self):
        self.productos = []

    def crear_producto(self, nombre, precio, stock=10, categoria="Otros"):
        producto = Producto(nombre=nombre, precio=precio, stock=stock, categoria=categoria)
        return producto

    def guardar_en_bd(self, producto: Producto):
        producto.insertar()

    def obtener_producto_por_id(self, id_producto):
        return Producto.buscar_por_id(id_producto)

    def listar_productos(self):
        return Producto.listar_todos()

    def buscar_productos(self, q: str):
        if not q:
            return Producto.listar_todos()
        return Producto.buscar_por_nombre_o_categoria(q)

    # --- Reglas de stock para el flujo de pedido ---
    def hay_stock(self, id_producto: int, cantidad: int) -> bool:
        producto = Producto.buscar_por_id(id_producto)
        if not producto:
            return False
        try:
            return int(producto.stock) >= int(cantidad)
        except (TypeError, ValueError):
            return False

    def descontar_stock(self, id_producto: int, cantidad: int) -> bool:
        return Producto.descontar_stock(int(id_producto), int(cantidad))
