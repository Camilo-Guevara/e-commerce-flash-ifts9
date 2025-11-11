from datetime import datetime


def registrar_evento(accion: str, detalle: str = "") -> None:
    """Registra un evento simple en consola (stub reemplazable por logging/BD)."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {accion}: {detalle}")

