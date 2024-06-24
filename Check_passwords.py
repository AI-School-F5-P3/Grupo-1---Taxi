import pandas as pd
import hashlib
import tkinter as tk
from IU_Class import init_game

#Cuando tengamos una base de datos como tal
#datos_usuarios = pd.read_csv("usuarios.csv")


def LogIn(username, password):    
    datos_usuarios = pd.read_csv("Usuarios.csv")
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password_local = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Passwords"].item()

    if username not in datos_usuarios["Usuarios"].values or password_inp != password_local:
        tk.messagebox.showinfo(title = "Error", message = "Usuario o contraseña incorrecta")
    
    else:
        init_game(username)

def Register(username, password, s_quest, s_answer):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    if datos_usuarios.Usuarios.isin([username]).any():
        tk.messagebox.showinfo(title = "Error", message = "Nombre de usuario en uso, por favor eliga otro")
    else:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        df = pd.DataFrame({'Usuarios' : [username], 'Passwords': [password_hash], 'Pregunta Secreta' : s_quest, 'Respuesta Secreta': s_answer})
        datos_usuarios = pd.concat([datos_usuarios, df], ignore_index = True)
        datos_usuarios.to_csv('Usuarios.csv', index = False)
        tk.messagebox.showinfo(title = "Registro completado", message = "Registo completado")
        return(True)
                        

def Pregunta(username):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    if not datos_usuarios.Usuarios.isin([username]).any():
        tk.messagebox.showinfo(title = "Error", message = "Usuario no encontrado")
    else:
        pregunta_s = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Pregunta Secreta"].item()
        tk.messagebox.showinfo(title = "Pregunta", message = pregunta_s)

def Respuesta(username, answer, new_pswd):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    local_answ = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Respuesta Secreta"].item()
    if local_answ == answer:
        new_pswd_hash = hashlib.sha256(new_pswd.encode('utf-8')).hexdigest()
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Passwords"] = new_pswd_hash
        datos_usuarios.to_csv('Usuarios.csv', index = False)
        tk.messagebox.showinfo(title = "Exito", message = "Contraseña cambiada")
    else:
        tk.messagebox.showinfo(title = "Error", message = "Respuesta Incorrecta")
    
