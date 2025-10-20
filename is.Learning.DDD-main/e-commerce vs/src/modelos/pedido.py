from datetime import datetime # Para manejar fechas y horas

class Pedido:
    ESTADOS_VALIDOS = ["abierto", "en proceso", "pagado", "finalizado", "cancelado"]

    def __init__(self, id_pedido, productos):
        """
        productos: lista de tuplas (Producto, cantidad)
        Inicializa el pedido con estado 'abierto', fecha actual y total calculado.
        """
        self.id_pedido = id_pedido
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.productos = productos  # lista de tuplas (Producto, cantidad)
        self.estado = "abierto"
        self.total = sum(p.precio * cantidad for p, cantidad in productos)

    def marcar_en_proceso(self):
        if self.estado != "abierto":
            raise ValueError("Solo un pedido abierto puede pasar a 'en proceso'.")
        self.estado = "en proceso"

    def procesar_pago(self, monto_pagado):
        """
        Procesa el pago del pedido.
        - Solo pedidos 'en proceso' pueden pagarse.
        - Si el monto es insuficiente, lanza un error y no cambia el estado.
        """
        if self.estado != "en proceso":
            raise ValueError("Solo un pedido 'en proceso' puede ser pagado.")
        if monto_pagado < self.total:
            raise ValueError(f"Monto insuficiente. Total: ${self.total:.2f}, Pagado: ${monto_pagado:.2f}")
        self.estado = "pagado"

    def finalizar_pedido(self):
        if self.estado != "pagado":
            raise ValueError("Solo un pedido pagado puede ser finalizado.")
        self.estado = "finalizado"

    def cancelar_pedido(self):
        if self.estado not in ["abierto", "en proceso"]:
            raise ValueError("Solo pedidos 'abierto' o 'en proceso' pueden cancelarse.")
        # Devolver el stock de los productos
        for producto, cantidad in self.productos:
            producto.stock += cantidad
        self.estado = "cancelado"

    def __str__(self):
        productos_str = "\n".join(
            [f"- {cantidad}x {p.nombre} = ${p.precio * cantidad:.2f}" for p, cantidad in self.productos]
        )
        return f"Pedido #{self.id_pedido}, Estado: {self.estado}, Total: ${self.total:.2f}\n{productos_str}"

