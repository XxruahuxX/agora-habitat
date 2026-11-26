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

    identificador = input("Correo o DNI: ")
    contrasena = input("Contraseña: ")

    resultado = controlador.login(identificador,contrasena)

    if isinstance(resultado, dict):

        print("Bienvenido", resultado["nombre"])
        print("Rol:", resultado["rol"])

        if resultado["rol"] == "ADMINISTRADOR":
            import view.vista_administrador

        elif resultado["rol"] == "SOCORRISTA":
            import view.vista_socorrista

        elif resultado["rol"] == "USUARIO_REGISTRADO":
            import view.vista_usuario

    elif resultado == "BLOQUEADO":

        print("Error: usuario bloqueado")

    elif resultado == "CONTRASENA_INCORRECTA":

        print("Error: contraseña incorrecta")

    elif resultado == "USUARIO_NO_ENCONTRADO":

        print("Error: usuario no encontrado")

elif opcion == "2":

    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    dni = input("DNI: ")
    telefono = input("Teléfono: ")

    respuesta = input(
        "¿Desea registrar una matrícula para el aparcamiento? (S/N): "
    ).upper()

    if respuesta == "S":

        matricula = input("Matrícula: ")

    else:

        matricula = None

    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    registrado = controlador.registrar_usuario(
        nombre,
        apellidos,
        dni,
        telefono,
        correo,
        contrasena,
        "USUARIO_REGISTRADO",
        matricula
    )

    if registrado == True:

        print("Usuario registrado correctamente")

    elif registrado == "DNI_INVALIDO":

        print("Error: el DNI debe tener 8 números y una letra")

    elif registrado == "TELEFONO_INVALIDO":

        print("Error: el teléfono debe tener 9 dígitos")

    else:

        print("Ya existe un usuario con ese correo")

else:

    print("Opción no válida")