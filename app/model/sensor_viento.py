"""Sensor de viento simulado (capa Modelo)."""
from __future__ import annotations

import random


class SensorViento:
    VARIACION_MIN = -5.0
    VARIACION_MAX = 5.0
    VALOR_MAX = 90.0

    def __init__(self, id: str, ultimo_valor: float = 15.0) -> None:
        self.id = id
        self.ultimo_valor = ultimo_valor

    def leer(self) -> float:
        """Devuelve una lectura en km/h cercana a la anterior (paseo aleatorio)."""
        nuevo = self.ultimo_valor + random.uniform(self.VARIACION_MIN, self.VARIACION_MAX)
        self.ultimo_valor = round(max(0.0, min(nuevo, self.VALOR_MAX)), 1)
        return self.ultimo_valor
