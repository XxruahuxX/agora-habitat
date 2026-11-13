import json
import hashlib


class UsuarioController:

    def cargar_usuarios(self):

        with open("data/usuarios.json", "r", encoding="utf-8") as fichero:
            return json.load(fichero)

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
            id,
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

        hash_contrasena = hashlib.sha256(
            contrasena.encode()
        ).hexdigest()

        nuevo_usuario = {
            "id": id,
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

        with open("data/usuarios.json", "w", encoding="utf-8") as fichero:
            json.dump(
                usuarios,
                fichero,
                indent=2,
                ensure_ascii=False
            )

        return True