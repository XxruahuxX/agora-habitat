import tkinter as tk
from tkinter import messagebox

from model.repositorio_json import RepositorioJSON

from controller.usuario_controller import UsuarioController
from controller.sombrilla_controller import SombrillaController
from controller.farola_controller import FarolaController
from controller.playa_controller import PlayaController


# =====================================
# Inicialización
# =====================================

repo = RepositorioJSON()

usuario_controller = UsuarioController()

sombrilla_controller = SombrillaController(repo)

farola_controller = FarolaController(repo)

playa_controller = PlayaController(
    repo,
    sombrilla_controller,
    farola_controller
)


# =====================================
# Funciones
# =====================================

def iniciar_proyecto():

    try:
        luz = playa_controller.evaluar_luz()
        viento = playa_controller.evaluar_viento()

        messagebox.showinfo(
            "Ágora Habitat",
            f"Proyecto iniciado correctamente\n\n"
            f"Luz: {luz} lux\n"
            f"Viento: {viento} km/h"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def iniciar_sesion():

    ventana_login = tk.Toplevel(ventana)
    ventana_login.title("Iniciar sesión")
    ventana_login.geometry("350x250")

    tk.Label(
        ventana_login,
        text="Correo o DNI"
    ).pack(pady=5)

    entrada_usuario = tk.Entry(
        ventana_login
    )
    entrada_usuario.pack()

    tk.Label(
        ventana_login,
        text="Contraseña"
    ).pack(pady=5)

    entrada_contrasena = tk.Entry(
        ventana_login,
        show="*"
    )
    entrada_contrasena.pack()

    def validar():

        identificador = entrada_usuario.get()
        contrasena = entrada_contrasena.get()

        resultado = usuario_controller.login(
            identificador,
            contrasena
        )

        if isinstance(resultado, dict):

            messagebox.showinfo(
                "Bienvenido",
                f"Usuario: {resultado['nombre']}\n"
                f"Rol: {resultado['rol']}"
            )

        elif resultado == "BLOQUEADO":

            messagebox.showerror(
                "Error",
                "Usuario bloqueado"
            )

        elif resultado == "CONTRASENA_INCORRECTA":

            messagebox.showerror(
                "Error",
                "Contraseña incorrecta"
            )

        else:

            messagebox.showerror(
                "Error",
                "Usuario no encontrado"
            )

    tk.Button(
        ventana_login,
        text="Acceder",
        command=validar
    ).pack(pady=15)


# =====================================
# Ventana principal
# =====================================

ventana = tk.Tk()

ventana.title("Ágora Habitat")

ventana.geometry("450x300")

tk.Label(
    ventana,
    text="Ágora Habitat",
    font=("Arial", 18, "bold")
).pack(pady=20)

tk.Button(
    ventana,
    text="Iniciar Proyecto",
    width=20,
    command=iniciar_proyecto
).pack(pady=10)

tk.Button(
    ventana,
    text="Iniciar Sesión",
    width=20,
    command=iniciar_sesion
).pack(pady=10)

tk.Button(
    ventana,
    text="Salir",
    width=20,
    command=ventana.destroy
).pack(pady=10)

ventana.mainloop()