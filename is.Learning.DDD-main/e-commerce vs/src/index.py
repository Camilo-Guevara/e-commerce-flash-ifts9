from datetime import datetime # Para manejar fechas y horas
import hashlib # Para hashing de contraseñas
import secrets # Para generar salts seguros

class Usuario:
    def __init__(self, id: int, correo: str, contraseña: str): #Definir el constructor de la clase Usuario con los atributos id, correo, contraseña
        if "@" not in correo or sum(c.isalpha() for c in correo) < 2: #c.isalpha() verifica si un carácter es una letra
            raise ValueError("El correo debe contener al menos 2 letras y el símbolo '@'.")
        self.id = id
        self.correo = correo
        self.pedidos = [] # Lista para almacenar los pedidos del usuario
        self.passwordSalt = secrets.token_hex(16) # Generar un salt seguro
        self.passwordHash = self._hash_contraseña(contraseña) # Almacenar el hash de la contraseña

    def agregar_pedido(self, pedido):
        self.pedidos.append(pedido) # Agregar un pedido a la lista de pedidos del usuario

    def _hash_contraseña(self, contraseña): # Función privada para hashear la contraseña con el salt
        return hashlib.sha256((contraseña + self.passwordSalt).encode()).hexdigest() 

    def validar_credenciales(self, correo_ingresado, contraseña_ingresada):
        if self.correo != correo_ingresado: # Verificar si el correo coincide
            return False
        hash_ingresado = hashlib.sha256((contraseña_ingresada + self.passwordSalt).encode()).hexdigest() # Hashear la contraseña ingresada con el mismo salt
        return hash_ingresado == self.passwordHash

class Producto:
    def __init__(self, id: int, nombre: str, precio: float, stock: int):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

class Pedido:
    def __init__(self, id: int, usuario: Usuario, estado: str = "abierto"):
        self.id = id
        self.usuario = usuario
        self.estado = estado
        self.fecha_creacion = datetime.now()
        self.items = []
        usuario.agregar_pedido(self)

    def agregar_item(self, producto: Producto, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")
        if producto.stock < cantidad:
            raise ValueError("No hay suficiente stock para este producto.")
        producto.stock -= cantidad
        item = ItemPedido(len(self.items) + 1, self, producto, cantidad, producto.precio) # Crear un nuevo item de pedido
        self.items.append(item)

    def calcular_total(self):
        return sum(item.subtotal() for item in self.items)

    def procesar_pago(self, monto_pagado):
        total = self.calcular_total()
        if monto_pagado >= total:
            self.estado = "pagado"
            return True
        return False

    def cancelar_pedido(self):
        if self.estado not in ["abierto", "pagado"]: # Solo se puede cancelar si está abierto o pagado
            raise ValueError("El pedido no se puede cancelar en este estado.")
        for item in self.items:
            item.producto.stock += item.cantidad # Devolver el stock al producto
        self.estado = "cancelado"

    def finalizar_pedido(self):
        if self.estado != "pagado":
            raise ValueError("El pedido debe estar pagado para finalizarlo.")
        self.estado = "finalizado"

class ItemPedido:
    def __init__(self, id: int, pedido: Pedido, producto: Producto, cantidad: int, precio_unitario: float):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")
        if precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        self.id = id
        self.pedido = pedido
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def subtotal(self):
        return self.cantidad * self.precio_unitario


# BLOQUE DE PRUEBA
usuario1 = Usuario(1, "camilo@test.com", "MiContraseñaSegura123")

# Valida credenciales con la contraseña correcta
print(usuario1.validar_credenciales("camilo@test.com", "MiContraseñaSegura123"))

# Crear productos
producto1 = Producto(1, "Laptop", 1200.00, 10)
producto2 = Producto(2, "Mouse", 25.50, 50)

# Crear pedido
pedido1 = Pedido(1, usuario1)

# Agregar items
pedido1.agregar_item(producto1, 1)
pedido1.agregar_item(producto2, 2)

# Procesar pago
pedido1.procesar_pago(1251.00)

# Finalizar pedido
pedido1.finalizar_pedido()

# Mostrar resultados
print(f"Usuario: {usuario1.correo}")
print(f"Pedido #{pedido1.id}, Estado: {pedido1.estado}, Total: ${pedido1.calcular_total():.2f}")
for item in pedido1.items:
    print(f"- {item.cantidad}x {item.producto.nombre} = ${item.subtotal():.2f}")

