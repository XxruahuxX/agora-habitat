import tkinter as tk

ventana = tk.Tk()
ventana.title("Usuario Registrado")
ventana.geometry("400x200")

etiqueta = tk.Label(
    ventana,
    text="Vista Usuario Registrado"
)

etiqueta.pack()

ventana.mainloop()