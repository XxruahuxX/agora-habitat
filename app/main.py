import tkinter as tk
from tkinter import messagebox


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