"""Ágora Hábitat. Ejecutar con: python main.py"""
import flet as ft


def main(page: ft.Page):
    page.title = "Ágora Hábitat"
    page.add(ft.Button("Hola"))


if __name__ == "__main__":
    ft.run(main)
