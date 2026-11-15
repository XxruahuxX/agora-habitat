import json
import hashlib
from model.repositorio_json import RepositorioJSON


class UsuarioController:

    def __init__(self):
        self.repositorio = RepositorioJSON()

    def cargar_usuarios(self):
        return self.repositorio.cargar("usuarios")

    def login(self, correo, contrasena):

        usuarios = self.cargar_usuarios()

        hash_contrasena = hashlib.sha256(
            contrasena.encode()
        ).hexdigest()

        for usuario in usuarios:

            if usuario["correo"] == correo:

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
            rol):

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
            "rol": rol
        }

        usuarios.append(nuevo_usuario)

        self.repositorio.guardar(
            "usuarios",
            usuarios
        )

        return True