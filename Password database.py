import pandas as pd
import numpy as np

lista_usuarios = {'Usuarios': , 'Passwords': }
datos_usuarios = pd.DataFrame.from_dict(lista_usuarios)

def LogIn():
    usuario = input("Escriba su nombre de usuario: ")
    if usuario not in users.values():
        print("Usuario no registrado.")
        user = input("Escriba un nombre de usuario")
        while user in user.value():
            user = input("Ese nombre de usuario ya está seleccionado. Escriba un nombre de usuario.")
        password = input("Escribe una contraseña segura")
        password_hash = hashlib.sha256(password.encode('utf-8'))
        df = pd.DataFrame({'Usuarios': user, 'Passwords': password_hash})
        datos_usuarios.append(df2)
    else:
        password_inp = input("Escriba su contraseña: ")
        password_inp_hash = hashlib.sha256(password_inp.encode('utf-8'))
        if datos_usuarios.loc[datos_usuarios["Usuarios"] == usuario, 'Passwords'].iloc[0] != password_inp_hash:
            print("Contraseña incorrecta")
        else
            print("Bienvenido")
            #taximetro()


