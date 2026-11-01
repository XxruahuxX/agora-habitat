# Ágora Hábitat Playa

Sistema IoT para la gestión de una playa inteligente: acceso con aforo, sombrillas con cierre por viento, farolas con encendido automático y aparcamiento con sensores. Aplicación de escritorio en **Python** con **Flet**, patrón **Modelo-Vista-Controlador** y datos en ficheros **JSON**.

*Vivir en comunidad, a pie de playa.*

## Equipo

Héctor Muñoz · Hugo Rojo · Jesús Guinea · Pablo Molina

## Roles

- **Usuario**: reserva acceso, sombrilla y aparcamiento; consulta sus reservas.
- **Socorrista**: estado de la playa, banderas, alertas y control de sombrillas.
- **Administrador**: panel en tiempo real, umbrales, usuarios, reservas e históricos.

## Planificación (Scrum)

19 oct 2026 – 8 ene 2027. Tablero: [Trello](https://trello.com/b/V0ux5SeW/%C3%A1gora-h%C3%A1bitat-playa-scrum).

| Sprint | Objetivo |
|---|---|
| Sprint 1 · Anteproyecto (19–30 oct) | Análisis, requisitos, presupuesto, product backlog, Gantt y mockups |
| Sprint 2 (2–13 nov) | Proyecto Flet, UML, login, registro, modelo JSON, datos y sombrillas |
| Sprint 3 | Farolas, aparcamiento, socorrista, reservas, alertas y administrador |
| Sprint 4 | Estética, históricos, responsive, pruebas y portabilidad |
| Cierre | Memoria, presentación y demo |

Fechas detalladas en el Gantt.

## Documentación

- `docs/Gantt_Agora_Habitat.png`: diagrama de Gantt.
- `docs/mockups/Mockups_Agora_Habitat_Playa_v2.pdf`: mockups de todas las ventanas.
- `docs/sprint1/actas/`: actas de reunión del Sprint 1.
- `docs/sprint1/trello/`: capturas del tablero al inicio y al final del Sprint 1.

## Ejecución

```bash
pip install -r requirements.txt
python main.py
```

El código actual es la estructura MVC inicial. Su adaptación a la versión Playa (roles, modelo y datos) es trabajo del Sprint 2 (T10–T14).
