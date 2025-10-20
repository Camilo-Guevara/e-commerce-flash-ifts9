from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Podés pasar productos o datos aquí si querés
    return render_template('index.html', productos=[])

if __name__ == '__main__':
    app.run(debug=True)


from controladores.controlador_usuario import ControladorUsuario
from controladores.controlador_producto import ControladorProducto
from controladores.controlador_pedido import ControladorPedido
from controladores.controlador_item_pedido import ControladorItemPedido

controlador_usuario = ControladorUsuario()
controlador_producto = ControladorProducto()
controlador_pedido = ControladorPedido()
controlador_item_pedido = ControladorItemPedido()

usuario = None  # variable global para el usuario autenticado

def menu():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Registrar Usuario")
        print("2. Autenticar Usuario")
        print("3. Crear Producto")
        print("4. Crear Pedido")
        print("5. Agregar Item al Pedido")
        print("6. Calcular Total del Pedido")
        print("7. Procesar Pago del Pedido")
        print("8. Cancelar Pedido")
        print("9. Finalizar Pedido")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            correo = input("Ingrese el correo del usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            controlador_usuario.registrar_usuario(1, correo, contraseña)
            print(f"Usuario registrado: {correo}")

        elif opcion == "2":
            correo = input("Correo: ")
            contraseña = input("Contraseña: ")
            global usuario
            usuario = controlador_usuario.autenticar_usuario(correo, contraseña)

        elif opcion == "3":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            producto = controlador_producto.crear_producto(nombre, precio)
            controlador_producto.guardar_en_bd(producto)
            print(f"Producto guardado: {producto.nombre}")

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")
