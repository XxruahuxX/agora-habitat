"""Sombrilla de la playa (capa Modelo)."""
from __future__ import annotations

from enum import Enum


class EstadoSombrilla(Enum):
    LIBRE = "LIBRE"
    RESERVADA = "RESERVADA"
    CERRADA = "CERRADA"


class Sombrilla:
    def __init__(self, id: str, fila: int, estado: EstadoSombrilla,
                 estado_previo: EstadoSombrilla | None = None) -> None:
        self.id = id
        self.fila = fila
        self.estado = estado
        # Solo tiene valor mientras está cerrada por viento o por el socorrista:
        # guarda el estado al que debe volver al reabrirse.
        self.estado_previo = estado_previo

    def cerrar(self) -> bool:
        """Cierra la sombrilla. Devuelve False si ya estaba cerrada."""
        if self.estado == EstadoSombrilla.CERRADA:
            return False
        self.estado_previo = self.estado
        self.estado = EstadoSombrilla.CERRADA
        return True

    def abrir(self) -> bool:
        """Reabre la sombrilla a su estado anterior. Devuelve False si no estaba cerrada."""
        if self.estado != EstadoSombrilla.CERRADA:
            return False
        self.estado = self.estado_previo or EstadoSombrilla.LIBRE
        self.estado_previo = None
        return True

    @classmethod
    def from_dict(cls, d: dict) -> "Sombrilla":
        previo = d.get("estado_previo")
        return cls(
            id=d["id"],
            fila=d["fila"],
            estado=EstadoSombrilla(d["estado"]),
            estado_previo=EstadoSombrilla(previo) if previo else None,
        )

    def to_dict(self) -> dict:
        d = {"id": self.id, "fila": self.fila, "estado": self.estado.value}
        if self.estado_previo is not None:
            d["estado_previo"] = self.estado_previo.value
        return d
