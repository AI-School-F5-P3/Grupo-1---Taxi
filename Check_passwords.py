import pandas as pd
import hashlib

#Cuando tengamos una base de datos como tal
#datos_usuarios = pd.read_csv("usuarios.csv")


def LogIn(username, password):    
    datos_usuarios = pd.read_csv("Usuarios.csv")
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password_local = datos_usuarios.query('Usuarios == @usuario')["Passwords"][1]

    if username not in datos_usuarios["Usuarios"].values or password_inp != password_local:
        messagebox.showinfo(title = "Error", message = "Usuario o contraseña incorrecta")
    
    else:
        game = Game()
        game.run()

