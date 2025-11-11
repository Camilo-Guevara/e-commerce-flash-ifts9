from flask import Flask, render_template, request, redirect, url_for, session, flash
from controladores.controlador_producto import ControladorProducto
from controladores.controlador_pedido import ControladorPedido
from modelos.producto import Producto
from modelos.usuario import Usuario

# Configurar Flask: templates en 'templates' y estáticos en 'img'
app = Flask(__name__, template_folder='templates', static_folder='img')
app.secret_key = "dev-secret-key"
productos_ctrl = ControladorProducto()
pedido_ctrl = ControladorPedido()


@app.route('/')
def index():
    productos = productos_ctrl.listar_productos()
    return render_template('index.html', productos=productos)


@app.route('/productos')
def listar_productos():
    productos = productos_ctrl.listar_productos()
    return render_template('index.html', productos=productos)


@app.route('/buscar')
def buscar():
    q = request.args.get('q', '').strip()
    productos = productos_ctrl.buscar_productos(q)
    return render_template('index.html', productos=productos)


# ------------------- Autenticación -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    correo = request.form.get('correo', '').strip()
    password = request.form.get('password', '')
    usuario = Usuario.autenticar(correo, password)
    if not usuario:
        return render_template('login.html', error='Credenciales incorrectas')
    session['usuario'] = {'id': usuario.id, 'correo': usuario.correo, 'rol': usuario.rol}
    session.setdefault('pedido', [])  # lista de items {id, nombre, precio, cantidad}
    return redirect(url_for('listar_productos'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('listar_productos'))


# ------------------- Flujo de Pedido -------------------
def _requerir_login():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return None


@app.route('/pedido/agregar', methods=['POST'])
def pedido_agregar():
    redir = _requerir_login()
    if redir:
        return redir
    try:
        pid = int(request.form.get('id'))
        cantidad = int(request.form.get('cantidad', '1'))
    except (TypeError, ValueError):
        flash('Cantidad inválida', 'error')
        return redirect(url_for('listar_productos'))

    if cantidad <= 0:
        flash('Cantidad inválida', 'error')
        return redirect(url_for('listar_productos'))

    # ¿Stock suficiente?
    if not productos_ctrl.hay_stock(pid, cantidad):
        flash('Stock insuficiente', 'error')
        return redirect(url_for('listar_productos'))

    # Descontar stock (seguro en DB)
    if not productos_ctrl.descontar_stock(pid, cantidad):
        flash('Stock insuficiente', 'error')
        return redirect(url_for('listar_productos'))

    producto = Producto.buscar_por_id(pid)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('listar_productos'))

    # Agregar ítem al pedido en sesión
    items = session.get('pedido', [])
    # fusionar si ya existe
    found = False
    for it in items:
        if it['id'] == pid:
            it['cantidad'] += cantidad
            found = True
            break
    if not found:
        items.append({'id': pid, 'nombre': producto.nombre, 'precio': float(producto.precio), 'cantidad': cantidad})
    session['pedido'] = items

    flash('Producto agregado al pedido', 'ok')
    # ¿Agregar otro producto? → volver al catálogo
    return redirect(url_for('listar_productos'))


@app.route('/pedido/resumen', methods=['GET'])
def pedido_resumen():
    redir = _requerir_login()
    if redir:
        return redir
    items = session.get('pedido', [])
    total = sum(i['precio'] * i['cantidad'] for i in items)
    vacio = (len(items) == 0)
    return render_template('resumen.html', items=items, total=total, vacio=vacio)


@app.route('/pedido/confirmar', methods=['POST'])
def pedido_confirmar():
    redir = _requerir_login()
    if redir:
        return redir
    items = session.get('pedido', [])
    if not items:
        # Pedido vacío → error
        return render_template('resumen.html', items=items, total=0.0, vacio=True, error='Pedido inválido')

    # Crear pedido de dominio en memoria para cálculo/estado
    productos = []
    for it in items:
        p = Producto.buscar_por_id(it['id'])
        if p:
            productos.append((p, it['cantidad']))
    pedido = pedido_ctrl.crear_pedido(id_pedido=1, productos=productos)  # id ficticio en memoria
    total = pedido_ctrl.calcular_total(pedido)

    # En este demo confirmamos directamente sin pago
    pedido_ctrl.finalizar_pedido(pedido)  # Estado finalizado como en diagrama
    session['pedido'] = []  # limpiar
    return render_template('resumen.html', items=[], total=total, vacio=False, confirmado=True)


if __name__ == '__main__':
    app.run(debug=True)


# CLI de desarrollo: sembrar productos de ejemplo
@app.cli.command('seed-products')
def seed_products():
    """Inserta productos de ejemplo si la tabla está vacía."""
    existentes = productos_ctrl.listar_productos()
    if existentes:
        print(f"Ya hay {len(existentes)} productos. Nada que hacer.")
        return

    muestras = [
        ("Zapatillas Runner", 59.99, 25, "Calzado", "producto 1.jpeg"),
        ("Campera Urban", 89.90, 12, "Ropa", "producto 2.jpeg"),
        ("Mochila Trek", 39.50, 30, "Accesorios", "producto 3.jpeg"),
        ("Cinturón Cuero", 19.99, 100, "Accesorios", "producto 4.jpeg"),
        ("Remera Basic", 12.99, 80, "Ropa", "producto 5.jpeg"),
        ("Gorra Sport", 14.99, 60, "Accesorios", "producto 6.jpeg"),
    ]

    for nombre, precio, stock, categoria, imagen in muestras:
        p = Producto(nombre=nombre, precio=precio, stock=stock, categoria=categoria, imagenURL=imagen)
        p.insertar()

    print("Productos de ejemplo insertados.")
