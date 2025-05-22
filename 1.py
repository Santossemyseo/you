import tkinter as tk
from tkinter import messagebox

def mostrar_popup():
    ventana = tk.Tk()
    ventana.withdraw()  # Oculta la ventana principal

    messagebox.showinfo("Mensaje", "¡Este es un mensaje popup!")

if __name__ == "__main__":
    mostrar_popup()