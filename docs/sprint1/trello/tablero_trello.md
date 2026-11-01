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
2. Fase 1 · Anteproyecto (19–30 oct)
3. Sprint 1 · Base de la aplicación (2–13 nov)
4. Sprint 2 · Sensores de la playa (16–27 nov)
5. Sprint 3 · Supervisión y análisis (30 nov–11 dic)
6. Sprint 4 · Acabado y pruebas (14–25 dic)
7. Fase 6 · Cierre y entrega (28 dic–8 ene)
8. En curso
9. En revisión
10. Hecho

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

## 2. Fase 1 · Anteproyecto

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

## 3. Sprint 1 · Base de la aplicación

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 10 | Proyecto PyCharm + Flet, rutas relativas y Git | Héctor | 2 nov | 4 nov |
| 11 | Diagrama UML de clases (MVC) | Pablo | 2 nov | 5 nov |
| 12 | Login, registro y una vista por rol (HU01, HU02) | Héctor | 5 nov | 13 nov |
| 13 | Modelo y gestor de ficheros JSON | Pablo | 5 nov | 13 nov |
| 14 | Datos realistas: usuarios, zonas y sensores | Jesús | 9 nov | 13 nov |
| ◆ | Hito: Review Sprint 1 | Hito | | 13 nov |

## 4. Sprint 2 · Sensores de la playa

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 15 | Sombrillas: viento y cierre automático (HU05, HU10) | Hugo | 16 nov | 27 nov |
| 16 | Farolas: luz y encendido automático | Héctor | 16 nov | 27 nov |
| 17 | Aparcamiento: plazas libres y ocupadas (HU03, HU06) | Pablo | 16 nov | 27 nov |
| 18 | Vista del socorrista: estado de la playa (HU08) | Jesús | 18 nov | 27 nov |
| ◆ | Hito: Review Sprint 2 | Hito | | 27 nov |

## 5. Sprint 3 · Supervisión y análisis

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 19 | Vista del administrador: panel, umbrales, usuarios y reservas (HU11–HU14) | Héctor | 30 nov | 11 dic |
| 20 | Históricos y gráficas (HU15) | Pablo | 30 nov | 11 dic |
| 21 | Alertas y banderas (HU09) | Hugo | 2 dic | 11 dic |
| 22 | Nombre y rol en cada vista, logo y estética (HU17) | Jesús | 30 nov | 9 dic |
| ◆ | Hito: Review Sprint 3 | Hito | | 11 dic |

## 6. Sprint 4 · Acabado y pruebas

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 23 | Diseño responsive en varias resoluciones (HU16) | Jesús | 14 dic | 25 dic |
| 24 | Plan de pruebas y corrección de errores | Hugo | 14 dic | 25 dic |
| 25 | Formulario de sugerencias | Héctor | 14 dic | 18 dic |
| 26 | Revisión de portabilidad en PyCharm | Pablo | 21 dic | 25 dic |
| ◆ | Hito: Review Sprint 4 | Hito | | 25 dic |

## 7. Fase 6 · Cierre y entrega

| # | Tarjeta | Responsable | Inicio | Vence |
|---|---|---|---|---|
| 27 | Memoria final (plantilla UEM) | Pablo | 28 dic | 7 ene |
| 28 | Presentación y demo | Jesús | 30 dic | 8 ene |
| 29 | Revisión de calidad del código y la memoria | Equipo | 4 ene | 8 ene |
| ◆ | Hito: Entrega final | Hito | | 8 ene |

## 8. En curso (tareas transversales)

| # | Tarjeta | Responsable | Periodo |
|---|---|---|---|
| 30 | Reunión semanal y acta | Equipo | 19 oct – 8 ene (repetir cada semana) |
| 31 | Tablero Trello y Sprint Backlog | Hugo | 19 oct – 8 ene |

Además, a 23 oct, mover aquí las tarjetas 4, 7 y 8 de la Fase 1.
