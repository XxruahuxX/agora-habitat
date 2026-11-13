"""Tests del cierre automático de sombrillas. Ejecutar: python -m unittest discover tests -v"""
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

from app.controller.playa_controller import PlayaController
from app.controller.sombrilla_controller import SombrillaController
from app.model.repositorio_json import RepositorioJSON
from app.model.sensor_viento import SensorViento
from app.model.sombrilla import EstadoSombrilla, Sombrilla

DATA = Path(__file__).resolve().parents[1] / "data"


class BaseTest(unittest.TestCase):
    """Cada test trabaja sobre una copia de data/ en una carpeta temporal."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        shutil.copytree(DATA, self.tmp.name, dirs_exist_ok=True)
        self.repo = RepositorioJSON(self.tmp.name)
        self.ctrl = SombrillaController(self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def estados(self):
        return {s["id"]: s["estado"] for s in self.repo.cargar("sombrillas")}

    def reserva_sombrilla_hoy(self):
        reservas = self.repo.cargar("reservas")
        for r in reservas:
            if r["id"] == "r003":
                r["dia"] = date.today().isoformat()
        self.repo.guardar("reservas", reservas)


class TestModeloSombrilla(unittest.TestCase):
    def test_cerrar_y_abrir_vuelve_al_estado_previo(self):
        s = Sombrilla("s99", 1, EstadoSombrilla.RESERVADA)
        self.assertTrue(s.cerrar())
        self.assertEqual(s.estado, EstadoSombrilla.CERRADA)
        self.assertTrue(s.abrir())
        self.assertEqual(s.estado, EstadoSombrilla.RESERVADA)
        self.assertIsNone(s.estado_previo)

    def test_cerrar_dos_veces_no_cambia(self):
        s = Sombrilla("s99", 1, EstadoSombrilla.LIBRE)
        s.cerrar()
        self.assertFalse(s.cerrar())
        self.assertEqual(s.estado_previo, EstadoSombrilla.LIBRE)

    def test_dict_ida_y_vuelta(self):
        s = Sombrilla("s99", 2, EstadoSombrilla.RESERVADA)
        s.cerrar()
        d = s.to_dict()
        self.assertEqual(d, {"id": "s99", "fila": 2, "estado": "CERRADA", "estado_previo": "RESERVADA"})
        self.assertEqual(Sombrilla.from_dict(d).to_dict(), d)
        self.assertNotIn("estado_previo", Sombrilla("s1", 1, EstadoSombrilla.LIBRE).to_dict())


class TestCierreAutomatico(BaseTest):
    def test_viento_alto_cierra_todas(self):
        self.ctrl.cierre_automatico(55)
        self.assertEqual(set(self.estados().values()), {"CERRADA"})

    def test_viento_bajo_no_cambia_nada(self):
        antes = self.estados()
        self.assertEqual(self.ctrl.cierre_automatico(20), [])
        self.assertEqual(self.estados(), antes)

    def test_crea_una_sola_alerta(self):
        n = len(self.repo.cargar("alertas"))
        self.ctrl.cierre_automatico(55)
        self.ctrl.cierre_automatico(60)
        alertas = self.repo.cargar("alertas")
        self.assertEqual(len(alertas), n + 1)
        self.assertEqual(alertas[-1]["origen"], "REGLA_AUTOMATICA")
        self.assertEqual(alertas[-1]["nivel"], "ROJA")

    def test_histeresis(self):
        self.ctrl.cierre_automatico(55)
        self.ctrl.cierre_automatico(45)  # entre 40 y 50: no se toca
        self.assertEqual(self.estados()["s02"], "CERRADA")
        self.ctrl.cierre_automatico(30)  # < 40: se reabre
        self.assertEqual(self.estados()["s02"], "RESERVADA")
        self.assertEqual(self.estados()["s01"], "LIBRE")

    def test_s04_cerrada_antes_no_se_abre(self):
        self.ctrl.cierre_automatico(55)
        self.ctrl.cierre_automatico(30)
        self.assertEqual(self.estados()["s04"], "CERRADA")

    def test_modo_manual_no_hace_nada(self):
        playa = self.repo.cargar_objeto("playa")
        playa["modo_sombrillas"] = "MANUAL"
        self.repo.guardar_objeto("playa", playa)
        self.ctrl.cierre_automatico(80)
        self.assertEqual(self.estados()["s01"], "LIBRE")

    def test_avisa_a_usuarios_con_reserva_hoy(self):
        self.reserva_sombrilla_hoy()
        n = len(self.repo.cargar("notificaciones"))
        self.ctrl.cierre_automatico(60)
        notis = self.repo.cargar("notificaciones")
        self.assertEqual(len(notis), n + 1)
        self.assertEqual(notis[-1]["usuario_id"], "u003")

    def test_sin_reservas_hoy_no_avisa(self):
        n = len(self.repo.cargar("notificaciones"))
        self.ctrl.cierre_automatico(60)
        self.assertEqual(len(self.repo.cargar("notificaciones")), n)


class TestControlManual(BaseTest):
    SOCORRISTA = "u002"
    ADMIN = "u001"

    def test_forzar_cierre_fila(self):
        cambiadas = self.ctrl.forzar("CERRAR", "FILA_1", self.SOCORRISTA)
        self.assertEqual({s.id for s in cambiadas}, {"s01", "s02", "s03"})
        self.assertEqual(self.estados()["s05"], "LIBRE")
        alerta = self.repo.cargar("alertas")[-1]
        self.assertEqual(alerta["origen"], "SOCORRISTA_MANUAL")
        self.assertEqual(alerta["autor_id"], self.SOCORRISTA)

    def test_forzar_abrir_por_ids(self):
        self.ctrl.forzar("CERRAR", "TODAS", self.SOCORRISTA)
        self.ctrl.forzar("ABRIR", ["s02"], self.SOCORRISTA)
        self.assertEqual(self.estados()["s02"], "RESERVADA")
        self.assertEqual(self.estados()["s01"], "CERRADA")

    def test_sin_permiso(self):
        with self.assertRaises(PermissionError):
            self.ctrl.forzar("CERRAR", "TODAS", self.ADMIN)
        with self.assertRaises(PermissionError):
            self.ctrl.cambiar_modo("MANUAL", self.ADMIN)

    def test_cambiar_modo(self):
        self.ctrl.cambiar_modo("MANUAL", self.SOCORRISTA)
        self.assertEqual(self.ctrl.modo(), "MANUAL")


class SensorFijo(SensorViento):
    def __init__(self, valores):
        super().__init__("se01")
        self.valores = list(valores)

    def leer(self):
        return self.valores.pop(0)


class TestPlayaController(BaseTest):
    def test_evaluar_viento_guarda_medida_y_cierra(self):
        n = len(self.repo.cargar("medidas"))
        playa = PlayaController(self.repo, self.ctrl, SensorFijo([55.0]))
        hoy_antes = len(playa.viento_hoy())
        self.assertEqual(playa.evaluar_viento(), 55.0)
        medidas = self.repo.cargar("medidas")
        self.assertEqual(len(medidas), n + 1)
        self.assertEqual(medidas[-1]["valor"], 55.0)
        self.assertEqual(len(playa.viento_hoy()), hoy_antes + 1)
        self.assertEqual(set(self.estados().values()), {"CERRADA"})

    def test_sensor_simulado_varia_poco(self):
        sensor = SensorViento("se01", 30.0)
        for _ in range(100):
            anterior = sensor.ultimo_valor
            valor = sensor.leer()
            self.assertLessEqual(abs(valor - anterior), 5.1)
            self.assertGreaterEqual(valor, 0.0)


if __name__ == "__main__":
    unittest.main()
