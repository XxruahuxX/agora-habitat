import hashlib
from model.repositorio_json import RepositorioJSON


class UsuarioController:

    def __init__(self):
        self.repositorio = RepositorioJSON()

    def cargar_usuarios(self):
        return self.repositorio.cargar("usuarios")

    def validar_dni(self, dni):

        if len(dni) != 9:
            return False

        numeros = dni[:8]
        letra = dni[8]

        if not numeros.isdigit():
            return False

        if not letra.isalpha():
            return False

        return True

    def validar_telefono(self, telefono):

        if len(telefono) != 9:
            return False

        if not telefono.isdigit():
            return False

        return True

    def login(self, identificador, contrasena):

        usuarios = self.cargar_usuarios()

        hash_contrasena = hashlib.sha256(
            contrasena.encode()
        ).hexdigest()

        for usuario in usuarios:

            if (
                usuario["correo"] == identificador
                or usuario["dni"] == identificador
            ):

                if usuario["estado"] != "ACTIVO":
                    return "BLOQUEADO"

                if usuario["contrasena_hash"] == hash_contrasena:
                    return usuario

                return "CONTRASENA_INCORRECTA"

        return "USUARIO_NO_ENCONTRADO"

    def registrar_usuario(
            self,
            nombre,
            apellidos,
            dni,
            telefono,
            correo,
            contrasena,
            rol,
            matricula=None):

        if not self.validar_dni(dni):
            return "DNI_INVALIDO"

        if not self.validar_telefono(telefono):
            return "TELEFONO_INVALIDO"

        usuarios = self.cargar_usuarios()

        for usuario in usuarios:

            if usuario["correo"] == correo:
                return False

        nuevo_id = self.repositorio.siguiente_id("u")

        hash_contrasena = hashlib.sha256(
            contrasena.encode()
        ).hexdigest()

        nuevo_usuario = {
            "id": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "dni": dni,
            "telefono": telefono,
            "correo": correo,
            "contrasena_hash": hash_contrasena,
            "estado": "ACTIVO",
            "rol": rol,
            "matricula": matricula
        }

        usuarios.append(nuevo_usuario)

        self.repositorio.guardar(
            "usuarios",
            usuarios
        )

        return True