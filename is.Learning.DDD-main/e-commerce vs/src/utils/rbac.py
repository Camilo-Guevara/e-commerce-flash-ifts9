def tiene_permiso(usuario, accion):
    """Valida si un usuario posee permiso para una acción dada, según su rol."""
    rol = getattr(usuario, "rol", "Cliente") or "Cliente"
    permisos = {
        "Cliente": {"ver_productos", "crear_pedido"},
        "Empleado": {"ver_productos", "crear_pedido", "gestionar_pedido"},
        "Administrador": {"ver_productos", "crear_pedido", "gestionar_pedido", "administrar_usuarios"},
    }
    return accion in permisos.get(rol, set())

