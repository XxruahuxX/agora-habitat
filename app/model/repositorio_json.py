"""Gestor de ficheros JSON (capa Modelo).

Lee y escribe los ficheros de la carpeta data/ de la raíz del proyecto.
Los controladores usan esta clase y nunca abren los .json directamente.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


class RepositorioJSON:
    # prefijo de id -> (entidad/fichero, número de dígitos del id)
    PREFIJOS: dict[str, tuple[str, int]] = {
        "u": ("usuarios", 3),
        "r": ("reservas", 3),
        "ru": ("registros_uso", 3),
        "n": ("notificaciones", 3),
        "s": ("sombrillas", 2),
        "p": ("plazas", 2),
        "f": ("farolas", 2),
        "se": ("sensores", 2),
        "m": ("medidas", 3),
        "a": ("alertas", 3),
    }

    def __init__(self, ruta: Path | str | None = None) -> None:
        # Por defecto: <raíz del proyecto>/data (este fichero está en app/model/)
        if ruta is None:
            ruta = Path(__file__).resolve().parents[2] / "data"
        self._ruta = Path(ruta)
        self._ruta.mkdir(parents=True, exist_ok=True)

    @property
    def ruta(self) -> Path:
        return self._ruta

    # ---------- ficheros que contienen una LISTA de diccionarios ----------

    def cargar(self, entidad: str) -> list[dict]:
        """Devuelve la lista de registros de la entidad ([] si no existe el fichero)."""
        datos = self._leer(entidad, [])
        if not isinstance(datos, list):
            raise ValueError(f"{entidad}.json debe contener una lista")
        return datos

    def guardar(self, entidad: str, datos: list[dict]) -> None:
        """Sobrescribe el fichero de la entidad con la lista completa."""
        self._escribir(entidad, datos)

    def siguiente_id(self, prefijo: str) -> str:
        """Genera el siguiente id libre: 'u' -> 'u005', 'se' -> 'se05'."""
        if prefijo not in self.PREFIJOS:
            raise ValueError(f"Prefijo de id desconocido: {prefijo!r}")
        entidad, ancho = self.PREFIJOS[prefijo]
        maximo = 0
        for registro in self.cargar(entidad):
            id_ = str(registro.get("id", ""))
            resto = id_[len(prefijo):]
            if id_.startswith(prefijo) and resto.isdigit():
                maximo = max(maximo, int(resto))
        return f"{prefijo}{maximo + 1:0{ancho}d}"

    # ---------- ficheros que contienen UN objeto (playa, configuracion) ----------

    def cargar_objeto(self, entidad: str) -> dict:
        datos = self._leer(entidad, {})
        if not isinstance(datos, dict):
            raise ValueError(f"{entidad}.json debe contener un objeto")
        return datos

    def guardar_objeto(self, entidad: str, datos: dict) -> None:
        self._escribir(entidad, datos)

    # ---------- internos ----------

    def _fichero(self, entidad: str) -> Path:
        if not re.fullmatch(r"[a-z_]+", entidad):
            raise ValueError(f"Nombre de entidad no válido: {entidad!r}")
        return self._ruta / f"{entidad}.json"

    def _leer(self, entidad: str, por_defecto: Any) -> Any:
        fichero = self._fichero(entidad)
        if not fichero.exists():
            return por_defecto
        try:
            with open(fichero, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"{fichero.name} no es un JSON válido: {e}") from e

    def _escribir(self, entidad: str, datos: Any) -> None:
        fichero = self._fichero(entidad)
        # Se escribe en un temporal y se renombra: si la app se cierra a mitad,
        # el fichero original no se queda corrupto.
        fd, tmp = tempfile.mkstemp(dir=self._ruta, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            os.replace(tmp, fichero)
        except Exception:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise