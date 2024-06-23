import tkinter as tk
import pandas as pd
import hashlib
from tkinter import messagebox
from Check_passwords import LogIn
from IU_Class import Game

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.title = self.root.title("Inicio de Sesion")
        self.root.geometry('500x500')
        self.root.configure(bg = '#824AB5')

        self.inicio = tk.Button(self.root, text = "Iniciar Sesion", font = ('Lucida Console', 16), command = self.login_screen)
        self.inicio.pack()

        self.reg = tk.Button(self.root, text = "Registrarse", font = ('Lucida Console', 16), command = self.reg_screen)
        self.reg.pack()

        self.root.mainloop()
    
    def check_password(self):
        LogIn(False, self.user.get(), self.password.get())

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label = tk.Label(self.root, text = "Inicie Sesion", font = ('Lucida Console', 16))

        self.user = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.user.pack()

        self.password = tk.Entry(self.root, font =('Lucida Console', 16), show = '*')
        self.password.pack()

        self.button = tk.Button(self.root, text = "Iniciar Sesion", font = ('Lucida Console', 16), command = self.check_password)
        self.button.pack()
    
    def reg_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label = tk.Label(self.root, text = 'Registro', font = ('Lucida Console', 16))
        self.user = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.user.pack()

        self.password = tk.Entry(self.root, font = ('Lucida Console', 16), show = '*')
        self.password.pack()

        self.button = tk.Button(self.root, text = "Registro", font = ('Lucida Console', 16))
        self.button.pack()



GUI()

