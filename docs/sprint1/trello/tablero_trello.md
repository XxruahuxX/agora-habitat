# Tablero Trello · Ágora Hábitat Playa

Basado en `gantt/Gantt_Agora_Habitat.png` y `mockups/Mockups_Agora_Habitat_Playa_v2.pdf`.
Metodología Scrum. 19 oct 2026 – 8 ene 2027. 6 fases de 2 semanas.

## Etiquetas

| Etiqueta | Color |
|---|---|
| Héctor Muñoz | Azul |
| Hugo Rojo | Verde |
| Jesús Guinea | Rojo |
| Pablo Molina | Morado |
| Todo el equipo | Negro |
| Hito | Naranja |
| Historia de usuario | Amarillo |

## Listas (izquierda a derecha)

1. Product Backlog
2. Sprint 1 · Anteproyecto (19–30 oct)
3. Sprint 2 · Base de la aplicación y primer sensor (2–13 nov)
4. Sprint 3 · Sensores y vistas por rol (16–27 nov)
5. Sprint 4 · Supervisión, pruebas y entrega (30 nov–11 dic)
6. En curso
7. En revisión
8. Hecho

Flujo: la tarjeta sale de su lista de fase a «En curso», luego «En revisión» y «Hecho».

---

## 1. Product Backlog (historias de usuario, mockups v2)

| Tarjeta | Checklist |
|---|---|
| HU01 Inicio de sesión | Correo o DNI + contraseña · Bandera y aforo visibles antes de entrar · Redirige a la vista de su rol · Acceso sin cuenta a plazas libres |
| HU02 Registro de usuario | Valida DNI (8 números + letra) · Valida teléfono (9 cifras) · Matrícula opcional · Socorrista y admin los crea el admin |
| HU03 Aparcamiento sin registro | Plazas libres en tiempo real · Sin reservas · Uso guardado como «sin registro» |
| HU04 Reservar acceso a la playa | Día, hora de entrada y personas · Bandera, aforo y reservas por franja · Bloqueo al llegar al aforo máximo · Resumen de próximas reservas |
| HU05 Reservar sombrilla | Plano libres/reservadas/cerradas · Día, franja y fila · Aviso de cierre por viento · Reserva en el histórico |
| HU06 Reservar plaza de aparcamiento | Plano libres/reservadas/ocupadas · Hora de llegada y matrícula · Sensor registra entrada y salida |
| HU07 Mis reservas | Filtrar por tipo · Próximas y anteriores · Cancelar · Último uso con entrada y salida |
| HU08 Socorrista: estado de la playa | Bandera y su origen · Viento vs umbral 60/80/100 % · Maqueta sombrillas, farolas y plazas · Aforo, sombrillas abiertas y luz |
| HU09 Socorrista: alertas y banderas | Cambiar bandera a mano · Alerta con motivo · Lista de alertas del día · Roja automática al 100 % |
| HU10 Socorrista: control de sombrillas | Gráfica viento + umbral · Forzar apertura/cierre · Modo automático/manual · Avisar a usuarios con reserva |
| HU11 Admin: panel en tiempo real | Ocupación, aforo y bandera · Sombrillas y aparcamiento · Afluencia por franja · Últimas banderas y reservas |
| HU12 Admin: umbrales y aforo | Viento 60 % amarilla, 80 % roja, 100 % roja auto · Aforo máximo · Umbral de luz farolas · Guardar o descartar |
| HU13 Admin: usuarios, roles y permisos | Alta, edición y bloqueo · Filtrar por rol · Permisos por rol · Crear socorristas y admins |
| HU14 Admin: gestión de reservas | Reservas por día · Entrada prevista, real y salida · Anular o marcar no presentada · Aforo por franja |
| HU15 Admin: históricos y estadísticas | Visitantes por día · Historial de accesos · Históricos de sombrillas, aparcamiento y alertas · Exportar CSV |
| HU16 Vista móvil | 1280 px y 390 px · Barra lateral → navegación inferior · Tarjetas en una columna |
| HU17 Coherencia estética | Paleta (#0B6E99, #2FB8B0, #F0664A, #F1E2C6, #0B2A43, #FBF8F1) · Logo en menú lateral · Nombre y rol en cabecera · Montserrat + Open Sans |

## 2. Sprint 1 · Anteproyecto (Actividad 3) 19 oct 30 oct

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 1 | Estado del arte: playas y ciudades inteligentes | Héctor | 19 oct | 23 oct |
| 2 | Perfil del usuario principal | Jesús | 19 oct | 22 oct |
| 3 | Contexto, problema y objetivos | Pablo | 19 oct | 23 oct |
| 4 | Matriz de requisitos y descripción de la solución | Héctor | 22 oct | 28 oct |
| 5 | Planificación, metodología y Gantt | Hugo | 19 oct | 23 oct |
| 6 | Presupuesto: recursos y personal | Pablo | 26 oct | 28 oct |
| 7 | Product Backlog en Trello y plan del Sprint 1 | Hugo | 23 oct | 28 oct |
| 8 | Mockups de todas las ventanas (PPT → PDF) | Jesús | 21 oct | 28 oct |
| 9 | Revisión final y exportación de los 3 PDF | Equipo | 29 oct | 30 oct |
| ◆ | Hito: Entrega Actividad 3 | Hito | | 30 oct |

## 3. Sprint 2 · Base de la aplicación y primer sensor 2 nov 13 nov

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 10 | Proyecto PyCharm + Flet, rutas relativas y Git | Héctor | 2 nov | 4 nov |
| 11 | Diagrama UML de clases (MVC) | Pablo | 2 nov | 5 nov |
| 12 | Login, registro y una vista por rol (HU01, HU02) | Héctor | 5 nov | 13 nov |
| 13 | Modelo y gestor de ficheros JSON | Pablo | 5 nov | 13 nov |
| 14 | Datos realistas: usuarios, zonas y sensores | Jesús | 9 nov | 13 nov |
|    |Sombrillas: viento y cierre automático | Hugo | 9 nov | 13 nov |
| ◆ | Hito: Review Sprint 1 | Hito | | 13 nov |

## 4. Sprint 3 · Sensores y vistas por rol 16 nov 27 nov

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 16 | Farolas: luz y encendido automático | Héctor | 16 nov | 27 nov |
| 17 | Aparcamiento: plazas libres y ocupadas (HU03, HU06) | Pablo | 16 nov | 27 nov |
| 18 | Vista del administrado | Hugo y Pablo | 18 nov | 27 nov |
| 19 | Vista del encargado de zona(socorrista) | Jesús | 18 nov | 27 nov |
| 20 | Vista del usuario | Hector | 18 nov | 27 nov |
| 21 | Alertas y averías de sensores | Hector | 18 nov | 27 nov |
| ◆ | Hito: Review Sprint 2 | Hito | | 27 nov |

## 5. Sprint 4 · Supervisión, pruebas y entrega 30 nov 11 dic

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 22 | Nombre y rol en cada vista, logo y estética | Jesús | 30 nov | 10 dic |
| 22 | Formulario de sugerencias | Héctor | 30 nov | 10 dic |
| 24 | Diseño responsive en varias resoluciones | Héctor | 2 dic | 11 dic |
| 25 | Plan de pruebas y correccion de errores | Hugo | 30 nov | 11 dic |
| 26 | Revisión de portabilidad en PyCharm | Pablo | 30 nov | 11 dic |
| 27 | Memoria final (plantilla UEM) | Pablo | 30 nov | 11 dic |
| 28 | Presentación y demo | Jesús | 30 nov | 11 dic |
| 29 | Revisión de calidad del código y la memoria | Equipo | 30 nov | 11 dic |
| ◆ | Hito: Review Sprint 4 | Hito | | 11 dic |


## 6. En curso (tareas transversales)

| # | Tarjeta | Responsable | Periodo |
|---|---|---|---|
| 30 | Reunión semanal y acta | Equipo | 19 oct – 8 ene (repetir cada semana) |
| 31 | Tablero Trello y Sprint Backlog | Hugo | 19 oct – 8 ene |

