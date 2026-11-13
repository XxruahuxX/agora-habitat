# Guía: viento y cierre automático de sombrillas (tarea 15, HU05 y HU10)

Guía para implementarlo tú. Parte de la rama `development` tal como está hoy:
`app/model/repositorio_json.py` (de Pablo) y los JSON de `data/`.

## 0. Qué hay que conseguir

Regla (sale de `adm_umbral` y `configuracion.json`):

| Viento | % del umbral (50 km/h) | Qué pasa |
|---|---|---|
| ≥ 50 km/h | 100 % | Se cierran **todas** las sombrillas, alerta y aviso a usuarios con reserva |
| < 40 km/h | < 80 % | Se reabren las que cerró el viento ("se abre cuando vuelve a ser seguro", mockup `usu_somb`) |
| Entre 40 y 50 | | No se toca nada |

Solo actúa si `playa.json → modo_sombrillas` es `"AUTOMATICO"`. En `"MANUAL"` manda el socorrista (`soc_somb`).

**¿Por qué no reabrir justo al bajar de 50?** Si el viento oscila 49-51-49-51, las sombrillas se abrirían y cerrarían cada lectura. Ese hueco 40-50 se llama *histéresis*. Coméntalo en la memoria: queda bien.

## 1. Flujo completo

```
SensorViento.leer()                 (modelo)  → 52.3 km/h
      ↓
PlayaController.evaluar_viento()    (controlador) guarda la Medida en medidas.json
      ↓
SombrillaController.cierre_automatico(52.3)
      ├─ lee modo y umbral (playa.json, configuracion.json)
      ├─ Sombrilla.cerrar() en cada una   (modelo)
      ├─ guarda sombrillas.json
      ├─ crea Alerta en alertas.json
      └─ avisar_usuarios_con_reserva() → notificaciones.json
```

Encaja con el UML final: `SombrillaController ..> PlayaController : consulta viento`, `cierre_automatico(viento_kmh)`, `avisar_usuarios_con_reserva()`, `Sombrilla.abrir()/cerrar()`, `Sensor.leer()`.

Regla MVC: el **modelo** no abre ficheros ni sabe de Flet. El **controlador** usa `RepositorioJSON` y nunca `open()` directamente. La **vista** solo pinta y llama al controlador.

## 2. Ficheros que vas a crear

```
app/model/sombrilla.py                    Sombrilla + EstadoSombrilla
app/model/sensor_viento.py                SensorViento (simulado)
app/controller/__init__.py                vacío
app/controller/sombrilla_controller.py
app/controller/playa_controller.py        solo evaluar_viento() por ahora
tests/__init__.py                         vacío
tests/test_sombrillas.py
```

## 3. Paso 1: el modelo `Sombrilla`

Problema a resolver: s02 está `RESERVADA`. El viento la cierra → `CERRADA`. Cuando se reabre, ¿vuelve a `LIBRE` o a `RESERVADA`? Hay que recordarlo. Solución: un campo `estado_previo` que solo existe mientras está cerrada por viento.

```python
from enum import Enum

class EstadoSombrilla(Enum):
    LIBRE = "LIBRE"
    RESERVADA = "RESERVADA"
    CERRADA = "CERRADA"

class Sombrilla:
    def __init__(self, id, fila, estado, estado_previo=None):
        self.id = id
        self.fila = fila
        self.estado = estado
        self.estado_previo = estado_previo

    def cerrar(self):
        if self.estado == EstadoSombrilla.CERRADA:
            return False              # ya estaba cerrada: no hago nada
        self.estado_previo = self.estado
        self.estado = EstadoSombrilla.CERRADA
        return True
```

**Hazlo tú:**
- `abrir()`: si está `CERRADA`, vuelve a `estado_previo` (o `LIBRE` si es `None`), pone `estado_previo = None` y devuelve `True`.
- `from_dict(cls, d)` (`@classmethod`) y `to_dict()`. Ojo: en el JSON el estado es el texto `"LIBRE"`, en Python es `EstadoSombrilla.LIBRE`. Se convierte con `EstadoSombrilla(d["estado"])` y `self.estado.value`. Solo escribe `estado_previo` en el dict si no es `None`.

Que `cerrar()` devuelva `True/False` sirve luego para saber cuántas has cambiado de verdad.

> Si el equipo acaba usando `ModeloBase` (`codigo/modelo_base_json/modelo_base.py` en la carpeta del proyecto), hereda de él y te ahorras `from_dict/to_dict`.

## 4. Paso 2: el sensor simulado

No hay sensor real. Simula uno creíble: cada lectura se mueve poco respecto a la anterior (paseo aleatorio). Con `random.uniform(0, 60)` el viento saltaría de 3 a 55 km/h de golpe.

```python
import random

class SensorViento:
    def __init__(self, id, ultimo_valor=15.0):
        self.id = id
        self.ultimo_valor = ultimo_valor

    def leer(self):
        nuevo = self.ultimo_valor + random.uniform(-5, 5)
        self.ultimo_valor = round(max(0.0, min(nuevo, 90.0)), 1)
        return self.ultimo_valor
```

En `sensores.json` el de viento es `se01`. Para probar el cierre rápido, sube el `-5, 5` a `-5, 15` un rato.

## 5. Paso 3: `SombrillaController.cierre_automatico`

Carga y guarda pasando por el modelo:

```python
def _cargar(self):
    return [Sombrilla.from_dict(d) for d in self.repo.cargar("sombrillas")]

def _guardar(self, sombrillas):
    self.repo.guardar("sombrillas", [s.to_dict() for s in sombrillas])
```

El método principal:

```python
MARGEN_REAPERTURA = 0.8

def cierre_automatico(self, viento_kmh):
    playa = self.repo.cargar_objeto("playa")
    if playa.get("modo_sombrillas") != "AUTOMATICO":
        return []
    umbral = self.repo.cargar_objeto("configuracion")["umbral_viento_kmh"]
    sombrillas = self._cargar()
    cambiadas = []
    if viento_kmh >= umbral:
        cambiadas = [s for s in sombrillas if s.cerrar()]
        if cambiadas:                       # solo la primera vez, no en cada lectura
            self._crear_alerta(f"Viento {viento_kmh} km/h: cierre automático de sombrillas")
            self.avisar_usuarios_con_reserva()
    elif viento_kmh < umbral * self.MARGEN_REAPERTURA:
        cambiadas = [s for s in sombrillas
                     if s.estado_previo is not None and s.abrir()]
    if cambiadas:
        self._guardar(sombrillas)
    return cambiadas
```

Fíjate en dos detalles:
- `if cambiadas:` antes de la alerta. Sin él, con viento de 55 durante una hora generas una alerta por lectura.
- Al reabrir solo tocas las que tienen `estado_previo`. Así s04, que ya estaba `CERRADA` antes (avería, decisión manual), no se abre sola.

**Hazlo tú:** `_crear_alerta(descripcion)`. Mira el formato de `alertas.json`. Valores: `nivel="ROJA"`, `origen="REGLA_AUTOMATICA"`, `autor_id=None`, `id=self.repo.siguiente_id("a")`, `hora=datetime.now().isoformat(timespec="seconds")`.

## 6. Paso 4: `avisar_usuarios_con_reserva`

Busca en `reservas.json` las de `tipo == "SOMBRILLA"`, `dia == hoy` y `estado` en `CONFIRMADA` o `PENDIENTE`. Saca los `usuario_id` en un `set` (un usuario con dos reservas recibe un solo aviso). Por cada uno, añade una notificación.

Trampa: `siguiente_id("n")` lee el fichero. Si añades tres notificaciones a la lista y guardas al final, las tres tendrán el mismo id. Guarda dentro del bucle:

```python
for u in usuarios:
    notis = self.repo.cargar("notificaciones")
    notis.append({
        "id": self.repo.siguiente_id("n"),
        "usuario_id": u,
        "mensaje": "Tu sombrilla se ha cerrado por viento fuerte.",
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "leida": False,
    })
    self.repo.guardar("notificaciones", notis)
```

Lo mismo te pasará en `_guardar_medida` si algún día guardas varias de golpe.

## 7. Paso 5: `PlayaController.evaluar_viento`

```python
class PlayaController:
    def __init__(self, repositorio, sombrilla_controller):
        self.repo = repositorio
        self.sombrillas = sombrilla_controller
        previas = [m for m in self.repo.cargar("medidas") if m["sensor_id"] == "se01"]
        self.sensor = SensorViento("se01", previas[-1]["valor"] if previas else 15.0)

    def evaluar_viento(self):
        viento = self.sensor.leer()
        self._guardar_medida(viento)
        self.sombrillas.cierre_automatico(viento)
        return viento
```

**Hazlo tú:** `_guardar_medida(valor)` con el formato de `medidas.json` (`id` con prefijo `"m"`).

Esas medidas son las que pintará la gráfica "Viento hoy" de `soc_somb`: filtra las de `se01` con fecha de hoy.

La bandera (`evaluar_bandera`, 60/80 %) también sale de aquí, pero es de `PlayaController`. Habla con quien lleve HU08 para no pisaros: tú solo necesitas que `evaluar_viento()` llame a `cierre_automatico()`.

## 8. Paso 6: lectura periódica en Flet

El sensor se lee cada X segundos sin bloquear la ventana. En Flet se hace con una tarea `async`:

```python
import asyncio

async def bucle_viento():
    while True:
        playa_ctrl.evaluar_viento()
        vista.actualizar(...)        # repintar gráfica y sombrillas
        page.update()
        await asyncio.sleep(10)

page.run_task(bucle_viento)
```

Lánzalo **una vez** al arrancar la app (en `AppController`), no al abrir la pantalla: si no, cada vez que entres a "Sombrillas" se crea otro bucle. Confirma la firma de `page.run_task` en la doc de Flet 1.0.4 (la versión de `requirements.txt`).

Ojo: el `main.py` de la raíz importa `app.controller.app_controller`, que aún no existe, y `app/main.py` es un ejemplo en Tkinter. Hasta que alguien cree `AppController`, la app no arranca.

## 9. Paso 7 (HU10, socorrista): forzar y cambiar modo

Del UML: `forzar(accion, ambito)` y `cambiar_modo(modo)`.

- `cambiar_modo("MANUAL")`: cambia `modo_sombrillas` en `playa.json` con `cargar_objeto` / `guardar_objeto`.
- `forzar("CERRAR", "TODAS" | "FILA_1" | [ids])`: igual que el cierre automático pero sin mirar el viento ni el modo. Según `soc_somb`, al forzar el cierre también se crea alerta (`origen="SOCORRISTA_MANUAL"`, `autor_id` = socorrista) y se avisa a los usuarios.
- Comprueba el permiso `ABRIR_CERRAR_SOMBRILLAS` (está en `roles.json`) antes de hacer nada.

Reutiliza `cerrar()`, `_crear_alerta()` y `avisar_usuarios_con_reserva()`. Si te sale código repetido, sácalo a un método privado `_cerrar(sombrillas, origen)`.

## 10. Paso 8: probarlo

Los tests usan una **copia** de `data/` en una carpeta temporal. Así no estropeas los JSON del repo.

```python
import shutil, tempfile, unittest
from pathlib import Path
from app.model.repositorio_json import RepositorioJSON
from app.controller.sombrilla_controller import SombrillaController

DATA = Path(__file__).resolve().parents[1] / "data"

class TestCierreAutomatico(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        shutil.copytree(DATA, self.tmp.name, dirs_exist_ok=True)
        self.repo = RepositorioJSON(self.tmp.name)
        self.ctrl = SombrillaController(self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def estados(self):
        return {s["id"]: s["estado"] for s in self.repo.cargar("sombrillas")}

    def test_viento_alto_cierra_todas(self):
        self.ctrl.cierre_automatico(55)
        self.assertEqual(set(self.estados().values()), {"CERRADA"})
```

**Hazlo tú**, un test por caso:

| Test | Llamadas | Qué compruebas |
|---|---|---|
| Viento bajo | `cierre_automatico(20)` | Nada cambia |
| Crea alerta | `(55)` | `alertas.json` tiene 1 más |
| Sin alertas repetidas | `(55)` y `(60)` | Solo 1 alerta nueva |
| Histéresis | `(55)`, `(45)`, `(30)` | Tras 45 s02 sigue `CERRADA`; tras 30 vuelve a `RESERVADA` |
| s04 no se abre | igual | s04 sigue `CERRADA` |
| Modo manual | pon `MANUAL` en playa y `(80)` | s01 sigue `LIBRE` |
| Aviso | cambia `r003.dia` a hoy y `(60)` | 1 notificación más |
| Modelo | `Sombrilla(...RESERVADA)`, `cerrar()`, `abrir()` | Vuelve a `RESERVADA` |

Ejecutar desde la raíz del repo:

```
python -m unittest discover tests -v
```

Prueba a mano sin interfaz:

```
python -c "from app.model.repositorio_json import RepositorioJSON as R; from app.controller.sombrilla_controller import SombrillaController as S; from app.controller.playa_controller import PlayaController as P; r=R('/tmp/copia_data'); p=P(r,S(r)); print([p.evaluar_viento() for _ in range(10)])"
```

(antes copia `data/` a `/tmp/copia_data`).

## 11. Orden recomendado

1. `Sombrilla` + test del modelo.
2. `cierre_automatico` (sin alerta ni avisos) + tests de cierre, histéresis y modo manual.
3. Alerta y avisos + sus tests.
4. `SensorViento` y `evaluar_viento`.
5. Bucle en Flet y vista `ControlSombrillasView`.
6. `forzar` y `cambiar_modo`.

Un commit por paso en tu rama `feature/T15-hugo`.
