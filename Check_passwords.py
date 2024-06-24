import pandas as pd
import hashlib
import tkinter as tk
from IU_Class import init_game
from logger_config import logger # Control de log

#Cuando tengamos una base de datos como tal
#datos_usuarios = pd.read_csv("usuarios.csv")


def LogIn(username, password):    
    datos_usuarios = pd.read_csv("Usuarios.csv")
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try: # Control de log
        password_local = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Passwords"].item()
    except ValueError: # Control de log
        logger.error(f'Usuario {username} no encontrado en la base de datos') # Control de log
        return False

    if username not in datos_usuarios["Usuarios"].values or password_inp != password_local:
        logger.warning(f'Intento de inicio de sesión fallido para usuario: {username}') # Control de log
        return False
    else:
        logger.info(f'Inicio de sesión exitoso para usuario: {username}') # Control de log
        return datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Licencia"].item()


def Register(username, password, s_quest, s_answer, conductor):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    if datos_usuarios.Usuarios.isin([username]).any():
        tk.messagebox.showinfo(title = "Error", message = "Nombre de usuario en uso, por favor eliga otro")
        logger.error(f'El nombre de usuaro {username} esta en uso, por favor elija otro') # Control de log
    else:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        df = pd.DataFrame({'Usuarios' : [username], 'Passwords': [password_hash], 'Pregunta Secreta' : [s_quest], 'Respuesta Secreta': [s_answer], 'Licencia': [conductor]})
        datos_usuarios = pd.concat([datos_usuarios, df], ignore_index = True)
        datos_usuarios.to_csv('Usuarios.csv', index = False)
        tk.messagebox.showinfo(title = "Registro completado", message = "Registo completado")
        logger.info(f'Registro completado con exito') # Control de log
        return(True)
                        

def Pregunta(username):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    if not datos_usuarios.Usuarios.isin([username]).any():
        tk.messagebox.showinfo(title = "Error", message = "Usuario no encontrado")
        logger.error(f'Usuario {username} no encontrado en la base de datos') # Control de log
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
        logger.info(f'Contraseña cambiada con exito') # Control de log
    else:
        tk.messagebox.showinfo(title = "Error", message = "Respuesta Incorrecta")
        logger.error(f'Intento de recuperación de contraseña fallida: Respuesta Secreta Incorrecta') # Control de log
    
def Descuentos(username, stop_disc, mov_disc):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Descuento Parado"] = int(stop_disc)
    datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Descuento Movimiento"] = int(mov_disc)
    datos_usuarios.to_csv('Usuarios.csv', index = False)

def Descuentos_taxi(username, turno, tarifa):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Turno"] = turno
    datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Tarifa extra"] = int(tarifa)
    datos_usuarios.to_csv('Usuarios.csv', index = False)