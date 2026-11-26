import random

class SensorLuz:

    VARIACION_MIN = -30
    VARIACION_MAX = 30

    def __init__(self, id, ultimo_valor=100):
        self.id = id
        self.ultimo_valor = ultimo_valor

    def leer(self):

        nuevo = (
            self.ultimo_valor
            + random.uniform(
                self.VARIACION_MIN,
                self.VARIACION_MAX
            )
        )

        self.ultimo_valor = max(0, round(nuevo, 1))

        return self.ultimo_valor