from basededatos.config_bd import obtener_conexion

class Producto:
    def __init__(self, id=None, nombre=None, precio=None, stock=None, categoria="General"):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

    def insertar(self):
        con = obtener_conexion()
        cur = con.cursor()
        cur.execute("INSERT INTO Producto (nombre, precio, stock, categoria) VALUES (%s,%s,%s,%s)",
                    (self.nombre, self.precio, self.stock, self.categoria))
        con.commit()
        con.close()

    @staticmethod
    def buscar_por_id(pid):
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Producto WHERE id=%s", (pid,))
        p = cur.fetchone()
        con.close()
        return Producto(**p) if p else None
