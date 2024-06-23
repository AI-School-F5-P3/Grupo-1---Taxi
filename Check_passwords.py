import pandas as pd
import hashlib
import tkinter as tk
from IU_Class import init_game

#Cuando tengamos una base de datos como tal
#datos_usuarios = pd.read_csv("usuarios.csv")


def LogIn(username, password):    
    datos_usuarios = pd.read_csv("Usuarios.csv")
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password_local = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Passwords"][1]

    if username not in datos_usuarios["Usuarios"].values or password_inp != password_local:
        tk.messagebox.showinfo(title = "Error", message = "Usuario o contraseña incorrecta")
    
    else:
        init_game()

