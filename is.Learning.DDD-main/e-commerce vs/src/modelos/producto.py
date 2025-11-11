from basededatos.config_bd import obtener_conexion


class Producto:
    def __init__(
        self,
        id=None,
        nombre=None,
        precio=None,
        stock=None,
        categoria="Otros",
        descripcion=None,
        imagenURL=None,
        destacado=False,
        nuevo=False,
        **kwargs,
    ):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.descripcion = descripcion
        self.imagenURL = imagenURL
        self.destacado = bool(destacado)
        self.nuevo = bool(nuevo)

    def insertar(self):
        con = obtener_conexion()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO Producto (nombre, descripcion, categoria, precio, stock, imagenURL, destacado, nuevo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                self.nombre,
                self.descripcion,
                self.categoria,
                self.precio,
                self.stock,
                self.imagenURL,
                int(bool(self.destacado)),
                int(bool(self.nuevo)),
            ),
        )
        con.commit()
        con.close()

    @staticmethod
    def _from_row(row: dict):
        # Toma solo las claves conocidas para el constructor
        campos = {
            k: row.get(k)
            for k in [
                "id",
                "nombre",
                "precio",
                "stock",
                "categoria",
                "descripcion",
                "imagenURL",
                "destacado",
                "nuevo",
            ]
        }
        return Producto(**campos)

    @staticmethod
    def buscar_por_id(pid):
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Producto WHERE id=%s", (pid,))
        p = cur.fetchone()
        con.close()
        return Producto._from_row(p) if p else None

    @staticmethod
    def listar_todos():
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT id, nombre, precio, stock, categoria, imagenURL, destacado, nuevo FROM Producto ORDER BY id DESC"
        )
        rows = cur.fetchall()
        con.close()
        return [Producto._from_row(r) for r in rows]

    @staticmethod
    def buscar_por_nombre_o_categoria(q: str):
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        like = f"%{q}%"
        cur.execute(
            """
            SELECT id, nombre, precio, stock, categoria, imagenURL, destacado, nuevo
            FROM Producto
            WHERE nombre LIKE %s OR categoria LIKE %s
            ORDER BY id DESC
            """,
            (like, like),
        )
        rows = cur.fetchall()
        con.close()
        return [Producto._from_row(r) for r in rows]

    @staticmethod
    def actualizar_stock(pid: int, nuevo_stock: int) -> bool:
        """Actualiza el stock absoluto del producto. Devuelve True si afectó 1 fila."""
        con = obtener_conexion()
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE Producto SET stock = %s WHERE id = %s",
                (int(nuevo_stock), int(pid)),
            )
            con.commit()
            return cur.rowcount == 1
        finally:
            con.close()

    @staticmethod
    def descontar_stock(pid: int, cantidad: int) -> bool:
        """Descuenta stock de forma segura si hay stock suficiente (condición en SQL)."""
        con = obtener_conexion()
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE Producto SET stock = stock - %s WHERE id = %s AND stock >= %s",
                (int(cantidad), int(pid), int(cantidad)),
            )
            con.commit()
            return cur.rowcount == 1
        finally:
            con.close()
