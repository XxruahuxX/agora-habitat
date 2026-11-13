"""Estado de la playa. De momento solo la lectura del viento (HU05)."""
from __future__ import annotations

from datetime import date, datetime

from app.controller.sombrilla_controller import SombrillaController
from app.model.repositorio_json import RepositorioJSON
from app.model.sensor_viento import SensorViento


class PlayaController:
    SENSOR_VIENTO_ID = "se01"

    def __init__(self, repositorio: RepositorioJSON,
                 sombrilla_controller: SombrillaController,
                 sensor: SensorViento | None = None) -> None:
        self.repo = repositorio
        self.sombrillas = sombrilla_controller
        if sensor is None:
            previas = self._medidas_viento()
            sensor = SensorViento(self.SENSOR_VIENTO_ID, previas[-1]["valor"] if previas else 15.0)
        self.sensor = sensor

    def evaluar_viento(self) -> float:
        """Lee el sensor, guarda la medida y aplica el cierre automático."""
        viento = self.sensor.leer()
        self._guardar_medida(viento)
        self.sombrillas.cierre_automatico(viento)
        return viento

    def viento_hoy(self) -> list[dict]:
        """Medidas de viento de hoy, para la gráfica de la vista del socorrista."""
        hoy = date.today().isoformat()
        return [m for m in self._medidas_viento() if m["fecha"].startswith(hoy)]

    def _medidas_viento(self) -> list[dict]:
        return [m for m in self.repo.cargar("medidas") if m["sensor_id"] == self.SENSOR_VIENTO_ID]

    def _guardar_medida(self, valor: float) -> None:
        ahora = datetime.now().isoformat(timespec="seconds")
        medidas = self.repo.cargar("medidas")
        medidas.append({
            "id": self.repo.siguiente_id("m"),
            "sensor_id": self.SENSOR_VIENTO_ID,
            "valor": valor,
            "fecha": ahora,
        })
        self.repo.guardar("medidas", medidas)

        sensores = self.repo.cargar("sensores")
        for s in sensores:
            if s["id"] == self.SENSOR_VIENTO_ID:
                s["ultima_lectura"] = ahora
        self.repo.guardar("sensores", sensores)
