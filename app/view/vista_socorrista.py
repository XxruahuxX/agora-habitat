import tkinter as tk

ventana = tk.Tk()
ventana.title("Socorrista")
ventana.geometry("400x200")

etiqueta = tk.Label(
    ventana,
    text="Vista Socorrista"
)

etiqueta.pack()

ventana.mainloop()
