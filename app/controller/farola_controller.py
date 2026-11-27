from model.farola import Farola

class FarolaController:

    def __init__(self, repositorio):
        self.repo = repositorio

    def listar(self):

        return [
            Farola.from_dict(f)
            for f in self.repo.cargar("farolas")
        ]

    def encendido_automatico(self, luz):

        umbral = self.repo.cargar_objeto(
            "configuracion"
        )["umbral_luz_lux"]

        farolas = self.listar()

        cambios = False

        if luz < umbral:

            for farola in farolas:

                if farola.encender():
                    cambios = True

        else:

            for farola in farolas:

                if farola.apagar():
                    cambios = True

        if cambios:

            self.repo.guardar(
                "farolas",
                [f.to_dict() for f in farolas]
            )
