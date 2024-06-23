import tkinter as tk
import pandas as pd
import hashlib
from tkinter import messagebox
from Check_passwords import LogIn, Register, Pregunta, Respuesta

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

        self.button = tk.Button(self.root, text = "Olvidé mi contraseña", font = ('Lucida Console', 16), command = self.res_pswd)
        self.button.pack()
    
    def reg_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label = tk.Label(self.root, text = 'Registro', font = ('Lucida Console', 16))
        self.user = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.user.pack()

        self.password = tk.Entry(self.root, font = ('Lucida Console', 16), show = '*')
        self.password.pack()

        self.quest = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.quest.pack()

        self.answ = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.answ.pack()

        self.button = tk.Button(self.root, text = "Registro", font = ('Lucida Console', 16), command = self.register)
        self.button.pack()

    def res_pswd(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.label = tk.Label(self.root, text = "Reiniciar contraseña", font = ('Lucida Console', 16))
        self.label.pack()

        self.user = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.user.pack()
        
        self.quest = tk.Button(self.root, text = "Ver pregunta secreta", font = ('Lucida Console', 16), command = self.get_quest)
        self.quest.pack()

        self.label2 = tk.Label(self.root, text = "Respuesta secreta", font = ('Lucida Console', 16))
        self.label2.pack()

        self.answer = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.answer.pack()

        self.label3 = tk.Label(self.root, text = "Nueva contraseña", font = ('Lucida Console', 16))
        self.label3.pack()

        self.new_pswd = tk.Entry(self.root, font = ('Lucida Console', 16))
        self.new_pswd.pack()

        self.submit = tk.Button(self.root, text = "Enviar", font = ('Lucida console', 16), command = self.change_pswd)
        self.submit.pack()
    

    def check_password(self):
        LogIn(self.user.get().lower(), self.password.get())
    
    def register(self):
         if Register(self.user.get().lower(), self.password.get(), self.quest.get(), self.answ.get().lower()) == True:
             self.login_screen()

    def get_quest(self):
        Pregunta(self.user.get().lower())
    
    def change_pswd(self):
        Respuesta(self.user.get().lower(), self.answer.get().lower(), self.new_pswd.get())


GUI()

