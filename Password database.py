import hashlib
import pandas as pd
import numpy as np

lista_usuarios = {'Usuarios': [], 'Passwords': []} #Diccionario vacío para ir rellenando con los usuarios y contraseñas que genere la función
datos_usuarios = pd.DataFrame.from_dict(lista_usuarios) #Se pasa del diccionario a una base de datos en pandas

def LogIn():
    '''
    La función en primer lugar va a pedir un nombre al usuario y comprobará mediante condicional if si existe ese nombre en nuestra base de datos.
    Si el usuario no existe, entendemos que es un usuario nuevo y le pedimos que nos de un nombre
    La función comprueba que el nombre no esté ya en uso, y mientras no se de un nombre nuevo seguira pidiendolo en bucle.
    Después se le pide una contraseña "segura", podríamos definir que significa que su contraseña sea segura e incluso solicitar una longitud concreta (o carácteres)
    Una vez tenemos la contraseña, esta se hashea utilizando sha-256 y se almacena de forma encriptada en nuestra base de datos, para aumentar la seguridad.
    Finalmente el usuario y su contraseña encriptada se añaden a la base de datos de usuarios.
    Si el usuario si existe, se le pedirá que introduzca su contraseña y está se buscara en la base de datos en su forma encriptada.
    Si hay coincidencias el programa de taximetro se inicia, si no, se le pide que repita.
    '''
    usuario = input("Escriba su nombre de usuario: ")
    if usuario not in datos_usuarios.Usuarios.isin(usuario):
        print("Usuario no registrado.")
        user = input("Escriba un nombre de usuario")
        while user in user.value():
            user = input("Ese nombre de usuario ya está seleccionado. Escriba un nombre de usuario.")
        password = input("Escribe una contraseña segura")
        password_hash = hashlib.sha256(password.encode('utf-8'))
        df = pd.DataFrame({'Usuarios': user, 'Passwords': password_hash})
        datos_usuarios.append(df)
    else:
        password_inp = input("Escriba su contraseña: ")
        password_inp_hash = hashlib.sha256(password_inp.encode('utf-8'))
        intentos = 0
        while(datos_usuarios.loc[datos_usuarios["Usuarios"] == usuario, 'Passwords'].iloc[0] != password_inp_hash):
            print("Contraseña incorrecta")
            password_inp = input("Escriba su contraseña: ")
            password_inp_hash = hashlib.sha256(password_inp.encode('utf-8'))
            intentos += 1
            if intentos == 6:
                break
        else:
            print("Bienvenido")
            #taximetro()


