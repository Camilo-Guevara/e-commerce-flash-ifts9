from modelos.producto import Producto

class ControladorProducto:
    def __init__(self):
        self.productos = []

    def crear_producto(self, nombre, precio):
        producto = Producto(nombre=nombre, precio=precio, stock=10)
        return producto

    def guardar_en_bd(self, producto):
        producto.insertar()

    def obtener_producto_por_id(self, id_producto):
        return Producto.buscar_por_id(id_producto)
