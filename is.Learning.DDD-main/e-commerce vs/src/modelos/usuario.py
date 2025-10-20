import hashlib, secrets
from basededatos.config_bd import obtener_conexion

class Usuario:
    def __init__(self, id=None, correo=None, rol="Cliente", passwordHash=None, passwordSalt=None):
        self.id = id
        self.correo = correo
        self.rol = rol
        self.passwordHash = passwordHash
        self.passwordSalt = passwordSalt

    @staticmethod
    def hash_password(password):
        salt = secrets.token_hex(16)
        hashed = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()
        return hashed, salt

    def registrar(self, password):
        hashed, salt = self.hash_password(password)
        con = obtener_conexion()
        cur = con.cursor()
        cur.execute("INSERT INTO Usuario (correo, rol, passwordHash, passwordSalt) VALUES (%s,%s,%s,%s)",
                    (self.correo, self.rol, hashed, salt))
        con.commit()
        con.close()

    @staticmethod
    def autenticar(correo, password):
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Usuario WHERE correo=%s", (correo,))
        u = cur.fetchone()
        con.close()
        if not u: return None
        hashed = hashlib.sha512((password + u["passwordSalt"]).encode("utf-8")).hexdigest()
        if hashed == u["passwordHash"]:
            return Usuario(**u)
        return None


    
