"""Control de sombrillas: cierre automático por viento y control manual (HU05, HU10)."""
from __future__ import annotations

from datetime import date, datetime

from app.model.repositorio_json import RepositorioJSON
from app.model.sombrilla import Sombrilla


class SombrillaController:
    # Se reabren cuando el viento baja del 80 % del umbral (histéresis):
    # entre el 80 % y el 100 % no se toca nada, para que no abran y cierren
    # en cada lectura si el viento oscila alrededor del umbral.
    MARGEN_REAPERTURA = 0.8

    def __init__(self, repositorio: RepositorioJSON) -> None:
        self.repo = repositorio

    # ---------- consulta ----------

    def listar(self) -> list[Sombrilla]:
        return self._cargar()

    def modo(self) -> str:
        return self.repo.cargar_objeto("playa").get("modo_sombrillas", "AUTOMATICO")

    # ---------- HU05: cierre automático ----------

    def cierre_automatico(self, viento_kmh: float) -> list[Sombrilla]:
        """Cierra o reabre las sombrillas según el viento. Devuelve las que cambian."""
        if self.modo() != "AUTOMATICO":
            return []
        umbral = self.repo.cargar_objeto("configuracion")["umbral_viento_kmh"]
        sombrillas = self._cargar()
        cambiadas: list[Sombrilla] = []

        if viento_kmh >= umbral:
            cambiadas = [s for s in sombrillas if s.cerrar()]
            self._guardar(sombrillas, cambiadas)
            if cambiadas:  # alerta y aviso solo la primera vez, no en cada lectura
                self._crear_alerta(
                    f"Viento {viento_kmh} km/h: cierre automático de sombrillas",
                    origen="REGLA_AUTOMATICA",
                )
                self.avisar_usuarios_con_reserva()
        elif viento_kmh < umbral * self.MARGEN_REAPERTURA:
            # Solo las que cerró el viento (tienen estado_previo); las cerradas
            # de antes (avería, decisión manual previa) se quedan cerradas.
            cambiadas = [s for s in sombrillas if s.estado_previo is not None and s.abrir()]
            self._guardar(sombrillas, cambiadas)
        return cambiadas

    def avisar_usuarios_con_reserva(self,
                                    mensaje: str = "Tu sombrilla se ha cerrado por viento fuerte.") -> int:
        """Notifica una vez a cada usuario con reserva de sombrilla hoy. Devuelve cuántos."""
        hoy = date.today().isoformat()
        usuarios = {
            r["usuario_id"]
            for r in self.repo.cargar("reservas")
            if r.get("tipo") == "SOMBRILLA"
            and r.get("dia") == hoy
            and r.get("estado") in ("CONFIRMADA", "PENDIENTE")
        }
        for u in sorted(usuarios):
            # Se guarda dentro del bucle: siguiente_id lee el fichero.
            notis = self.repo.cargar("notificaciones")
            notis.append({
                "id": self.repo.siguiente_id("n"),
                "usuario_id": u,
                "mensaje": mensaje,
                "fecha": self._ahora(),
                "leida": False,
            })
            self.repo.guardar("notificaciones", notis)
        return len(usuarios)

    # ---------- HU10: control manual del socorrista ----------

    def cambiar_modo(self, modo: str, socorrista_id: str) -> None:
        if modo not in ("AUTOMATICO", "MANUAL"):
            raise ValueError(f"Modo no válido: {modo!r}")
        self._comprobar_permiso(socorrista_id)
        playa = self.repo.cargar_objeto("playa")
        playa["modo_sombrillas"] = modo
        self.repo.guardar_objeto("playa", playa)

    def forzar(self, accion: str, ambito: str | list[str], socorrista_id: str) -> list[Sombrilla]:
        """accion: "CERRAR" o "ABRIR". ambito: "TODAS", "FILA_<n>" o lista de ids."""
        if accion not in ("CERRAR", "ABRIR"):
            raise ValueError(f"Acción no válida: {accion!r}")
        self._comprobar_permiso(socorrista_id)
        sombrillas = self._cargar()
        objetivo = self._filtrar(sombrillas, ambito)

        if accion == "CERRAR":
            cambiadas = [s for s in objetivo if s.cerrar()]
        else:
            cambiadas = [s for s in objetivo if s.abrir()]
        self._guardar(sombrillas, cambiadas)

        if accion == "CERRAR" and cambiadas:
            ids = ", ".join(s.id for s in cambiadas)
            self._crear_alerta(f"Cierre manual de sombrillas: {ids}",
                               origen="SOCORRISTA_MANUAL", autor_id=socorrista_id)
            self.avisar_usuarios_con_reserva("El socorrista ha cerrado tu sombrilla.")
        return cambiadas

    # ---------- internos ----------

    def _cargar(self) -> list[Sombrilla]:
        return [Sombrilla.from_dict(d) for d in self.repo.cargar("sombrillas")]

    def _guardar(self, sombrillas: list[Sombrilla], cambiadas: list[Sombrilla]) -> None:
        if cambiadas:
            self.repo.guardar("sombrillas", [s.to_dict() for s in sombrillas])

    @staticmethod
    def _filtrar(sombrillas: list[Sombrilla], ambito: str | list[str]) -> list[Sombrilla]:
        if isinstance(ambito, list):
            return [s for s in sombrillas if s.id in ambito]
        if ambito == "TODAS":
            return sombrillas
        if ambito.startswith("FILA_") and ambito[5:].isdigit():
            fila = int(ambito[5:])
            return [s for s in sombrillas if s.fila == fila]
        raise ValueError(f"Ámbito no válido: {ambito!r}")

    def _comprobar_permiso(self, usuario_id: str) -> None:
        usuario = next((u for u in self.repo.cargar("usuarios") if u["id"] == usuario_id), None)
        if usuario is None:
            raise PermissionError(f"Usuario {usuario_id} no existe")
        rol = next((r for r in self.repo.cargar("roles") if r["nombre"] == usuario.get("rol")), None)
        if rol is None or "ABRIR_CERRAR_SOMBRILLAS" not in rol["permisos"]:
            raise PermissionError("No tienes permiso para abrir o cerrar sombrillas")

    def _crear_alerta(self, descripcion: str, origen: str, autor_id: str | None = None) -> None:
        alertas = self.repo.cargar("alertas")
        alertas.append({
            "id": self.repo.siguiente_id("a"),
            "hora": self._ahora(),
            "descripcion": descripcion,
            "nivel": "ROJA",
            "origen": origen,
            "autor_id": autor_id,
        })
        self.repo.guardar("alertas", alertas)

    @staticmethod
    def _ahora() -> str:
        return datetime.now().isoformat(timespec="seconds")
