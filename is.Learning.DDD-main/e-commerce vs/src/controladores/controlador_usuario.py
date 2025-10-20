from modelos.usuario import Usuario

class ControladorUsuario:
    def __init__(self):
        self.usuarios = []

    def registrar_usuario(self, id, correo, contraseña):
        nuevo_usuario = Usuario(id=id, correo=correo)
        nuevo_usuario.registrar(contraseña)
        self.usuarios.append(nuevo_usuario)
        return nuevo_usuario

    def autenticar_usuario(self, correo, contraseña):
        return Usuario.autenticar(correo, contraseña)
