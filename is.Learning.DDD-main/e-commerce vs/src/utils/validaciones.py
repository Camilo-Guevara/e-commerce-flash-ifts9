import re


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_email(correo: str) -> bool:
    return bool(_EMAIL_RE.match(correo or ""))


def validar_precio(precio: float) -> bool:
    try:
        return float(precio) >= 0
    except (TypeError, ValueError):
        return False


def validar_stock(stock: int) -> bool:
    try:
        return int(stock) >= 0
    except (TypeError, ValueError):
        return False

