import tkinter as tk
from tkinter import messagebox
from controller.usuario_controller import UsuarioController

def iniciar_proyecto():
    messagebox.showinfo("Proyecto", "¡Inicio del proyecto!")


ventana = tk.Tk()
ventana.title("Ágora Habitat")
ventana.geometry("400x200")

boton = tk.Button(
    ventana,
    text="Iniciar Proyecto",
    command=iniciar_proyecto
)

boton.pack(expand=True)

ventana.mainloop()


from controller.usuario_controller import UsuarioController

controlador = UsuarioController()

print("1. Iniciar sesión")
print("2. Registrarse")

opcion = input("Elige una opción: ")

if opcion == "1":

    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    resultado = controlador.login(correo, contrasena)

    if isinstance(resultado, dict):
        print("Bienvenido", resultado["nombre"])
        print("Rol:", resultado["rol"])

    elif resultado == "BLOQUEADO":
        print("Error: usuario bloqueado")

    elif resultado == "CONTRASENA_INCORRECTA":
        print("Error: contraseña incorrecta")

    elif resultado == "USUARIO_NO_ENCONTRADO":
        print("Error: usuario no encontrado")

elif opcion == "2":

    id = input("ID: ")
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    dni = input("DNI: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    registrado = controlador.registrar_usuario(
        id,
        nombre,
        apellidos,
        dni,
        telefono,
        correo,
        contrasena,
        "USUARIO_REGISTRADO"
    )

    if registrado:
        print("Usuario registrado correctamente")
    else:
        print("Ya existe un usuario con ese correo")

else:
    print("Opción no válida")

    