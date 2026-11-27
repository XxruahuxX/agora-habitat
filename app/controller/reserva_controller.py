from datetime import date, datetime

from model.repositorio_json import RepositorioJSON


class ReservaController:

    def __init__(self, repositorio: RepositorioJSON):
        self.repo = repositorio

    # =====================================
    # CONSULTAS
    # =====================================

    def listar(self):
        return self.repo.cargar("reservas")

    def reservas_usuario(self, usuario_id):
        return [
            r
            for r in self.repo.cargar("reservas")
            if r["usuario_id"] == usuario_id
        ]
    # RESERVAR SOMBRILLA

    def reservar_sombrilla(
        self,
        usuario_id,
        sombrilla_id,
        dia=None
    ):

        if dia is None:
            dia = date.today().isoformat()

        # Comprobar que existe el usuario
        usuarios = self.repo.cargar("usuarios")

        existe_usuario = any(
            u["id"] == usuario_id
            for u in usuarios
        )

        if not existe_usuario:
            raise ValueError(
                f"El usuario {usuario_id} no existe"
            )

        # Comprobar que existe la sombrilla
        sombrillas = self.repo.cargar("sombrillas")

        existe_sombrilla = any(
            s["id"] == sombrilla_id
            for s in sombrillas
        )

        if not existe_sombrilla:
            raise ValueError(
                f"La sombrilla {sombrilla_id} no existe"
            )

        reservas = self.repo.cargar("reservas")

        # Comprobar disponibilidad
        for reserva in reservas:

            if (
                reserva["tipo"] == "SOMBRILLA"
                and reserva.get("sombrilla_id") == sombrilla_id
                and reserva["dia"] == dia
                and reserva["estado"] != "CANCELADA"
            ):
                return False

        nueva_reserva = {
            "id": self.repo.siguiente_id("r"),
            "tipo": "SOMBRILLA",
            "usuario_id": usuario_id,
            "dia": dia,
            "estado": "PENDIENTE",
            "fecha_creacion": datetime.now().isoformat(timespec="seconds"),
            "sombrilla_id": sombrilla_id,
            "desde": "10:00",
            "hasta": "20:00"
        }

        reservas.append(nueva_reserva)

        self.repo.guardar(
            "reservas",
            reservas
        )

        self._reservar_sombrilla(sombrilla_id)

        return True

    # =====================================
    # CANCELAR RESERVA
    # =====================================

    def cancelar_reserva(self, reserva_id):

        reservas = self.repo.cargar("reservas")

        for reserva in reservas:

            if reserva["id"] == reserva_id:

                reserva["estado"] = "CANCELADA"

                self.repo.guardar(
                    "reservas",
                    reservas
                )

                if reserva["tipo"] == "SOMBRILLA":
                    self._liberar_sombrilla(
                        reserva["sombrilla_id"]
                    )

                return True

        return False

    # =====================================
    # DISPONIBILIDAD
    # =====================================

    def disponible(
        self,
        sombrilla_id,
        dia=None
    ):

        if dia is None:
            dia = date.today().isoformat()

        reservas = self.repo.cargar("reservas")

        for reserva in reservas:

            if (
                reserva["tipo"] == "SOMBRILLA"
                and reserva.get("sombrilla_id") == sombrilla_id
                and reserva["dia"] == dia
                and reserva["estado"] != "CANCELADA"
            ):
                return False

        return True

    # =====================================
    # MÉTODOS INTERNOS
    # =====================================

    def _reservar_sombrilla(self, sombrilla_id):

        sombrillas = self.repo.cargar("sombrillas")

        encontrada = False

        for sombrilla in sombrillas:

            if sombrilla["id"] == sombrilla_id:

                sombrilla["estado"] = "RESERVADA"
                encontrada = True

        if not encontrada:
            raise ValueError(
                f"La sombrilla {sombrilla_id} no existe"
            )

        self.repo.guardar(
            "sombrillas",
            sombrillas
        )

    def _liberar_sombrilla(self, sombrilla_id):

        sombrillas = self.repo.cargar("sombrillas")

        encontrada = False

        for sombrilla in sombrillas:

            if sombrilla["id"] == sombrilla_id:

                sombrilla["estado"] = "LIBRE"
                encontrada = True

        if not encontrada:
            raise ValueError(
                f"La sombrilla {sombrilla_id} no existe"
            )

        self.repo.guardar(
            "sombrillas",
            sombrillas
        )