import tkinter as tk

ventana = tk.Tk()
ventana.title("Administrador")
ventana.geometry("400x200")

etiqueta = tk.Label(
    ventana,
    text="Vista Administrador"
)

etiqueta.pack()

ventana.mainloop()