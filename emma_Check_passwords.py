import pandas as pd
import hashlib
import tkinter as tk
from tkinter import messagebox
from logger_config import logger
import os

######################################################################################################
#                                                                                                    #
# IMPORTANTE:                                                                                        #
# Para probar el control del Login hay en el módulo "GUI Entrada.py" hay que cambiar a:                #   
# from emma_Check_password import LogIn, Register, Pregunta, Respuesta, Descuentos, Descuentos_taxi  #  
#                                                                                                    #
######################################################################################################

# Constantes
DB_FILE = "Usuarios.csv"

# Verificar si la base de datos existe, si no, crear una nueva
if not os.path.exists(DB_FILE):
    logger.warning("La base de datos no existe. Se creará una nueva.")
    df = pd.DataFrame(columns=["Usuarios", "Passwords", "Pregunta Secreta", "Respuesta Secreta", "Licencia", "Descuento Parado", "Descuento Movimiento", "Turno", "Tarifa extra", "Tarifa Mov", "Tarifa Stop", "Empresa"])
    df.to_csv(DB_FILE, index=False)

def LogIn(username, password):
    try:
        datos_usuarios = pd.read_csv(DB_FILE)
    except PermissionError:
        logger.warning('No se tienen permisos para acceder a la base de datos.')
        #messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False

    username = username.lower()
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        password_local = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Passwords"].item()
    except ValueError:
        logger.error(f'Usuario {username} no encontrado en la base de datos. ')
        return False

    if username not in datos_usuarios["Usuarios"].values or password_inp != password_local:
        logger.warning(f'Intento de inicio de sesión fallido para usuario: {username}')
        return False
    else:
        logger.info(f'Inicio de sesión exitoso para usuario: {username}')
        return datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Licencia"].item()

def LogIn_Empresa(username, password):
    try:
        datos_empresa = pd.read_csv("Empresa.csv")
    except PermissionError:
        logger.warning('No se tienen permisos para acceder a la base de datos.')
        #messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False

    username = username.lower()
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        password_local = datos_empresa.loc[datos_empresa["Usuarios"] == username]["Passwords"].item()
    except ValueError:
        logger.error(f'Usuario {username} no encontrado en la base de datos. ')
        return False
    if username not in datos_empresa["Usuarios"].values or password_inp != password_local:
        logger.warning(f'Intento de inicio de sesión fallido para usuario: {username}')
        return False
    else:
        empresa = datos_empresa.loc[datos_empresa["Usuarios"] == username]["Empresa"].item()
        logger.info(f'Inicio de sesión exitoso para usuario: {username}')
        return empresa


def Register(username, password, s_quest, s_answer, conductor, empresa):
    try:
        datos_usuarios = pd.read_csv(DB_FILE)
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        #messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False

    username = username.lower()
    s_answer = s_answer.lower()

    if datos_usuarios.Usuarios.isin([username]).any():
        messagebox.showinfo(title="Error", message="Nombre de usuario en uso, por favor eliga otro")
        logger.error(f'El nombre de usuario {username} está en uso, por favor elija otro')
    else:
        if not username:
            messagebox.showinfo(title="Error", message="Debe introducir un nombre de usuario.")
            logger.error('Nombre usuario vacio.')
            return False
        elif len(password) < 4:
            messagebox.showinfo(title="Error", message="Debe introducir una contraseña correcta de al menos 4 caracteres.")
            logger.error('Contraseña demasiado corta.')
            return False
        elif not s_quest:
            messagebox.showinfo(title="Error", message="La pregunta secreta es obligatoria.")
            logger.error('Pregunta secreta vacía.')
            return False
        elif not s_answer:
            messagebox.showinfo(title="Error", message="La respuesta secreta es obligatoria.")
            logger.error('Respuesta secreta vacía.')
            return False
        elif not conductor:
            messagebox.showinfo(title="Error", message="Seleccione tipo de conductor.")
            logger.error('No se ha seleccionado el tipo de conductor.')
            return False
        elif not empresa:
            messagebox.showinfo(title="Error", message="Seleccione empresa.")
            logger.error('No se ha seleccionado empresa.')
            return False

        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        df = pd.DataFrame({'Usuarios': [username], 'Passwords': [password_hash], 'Pregunta Secreta': [s_quest], 'Respuesta Secreta': [s_answer], 'Licencia': [conductor], 'Empresa': [empresa]})
        datos_usuarios = pd.concat([datos_usuarios, df], ignore_index=True)
        datos_usuarios.to_csv(DB_FILE, index=False)
        messagebox.showinfo(title="Registro completado", message="Registro completado con éxito")
        logger.info('Registro completado con éxito')
        return True


def Pregunta(username):
    username = username.lower()

    datos_usuarios = pd.read_csv("Usuarios.csv")
    if not username:
        messagebox.showinfo(title="Error", message="Debe introducir un nombre de usuario.")
        logger.error('Nombre de usuario vacío.')
        return False
    elif not datos_usuarios.Usuarios.isin([username]).any():
        messagebox.showinfo(title = "Error", message = "Usuario no encontrado")
        logger.error(f'Usuario {username} no encontrado en la base de datos') # Control de log
    else:
        pregunta_s = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Pregunta Secreta"].item()
        messagebox.showinfo(title = "Pregunta", message = pregunta_s)

def Respuesta(username, answer, new_pswd):
    try:
        datos_usuarios = pd.read_csv(DB_FILE)
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False

    username = username.lower()
    answer = answer.lower()

    if not username:
        messagebox.showinfo(title="Error", message="Debe introducir un nombre de usuario.")
        logger.error('Nombre de usuario vacío.')
        return False

    elif not answer:
        messagebox.showinfo(title="Error", message="Debe introducir su respuesta secreta.")
        logger.error('Respuesta secreta vacía.')
        return False
        
    try:
        local_answ = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Respuesta Secreta"].item()
    except ValueError:
        messagebox.showinfo(title="Error", message="Usuario no encontrado o respuesta incorrecta.")
        logger.error('Usuario no encontrado o respuesta incorrecta.')
        return False

    #local_answ = datos_usuarios.loc[datos_usuarios["Usuarios"] == username]["Respuesta Secreta"].item()
    if local_answ == answer:
        if len(new_pswd) < 4:
            messagebox.showinfo(title="Error", message="La contraseña debe tener al menos 4 caracteres.")
            logger.error('Contraseña demasiado corta.')
            return False

        new_pswd_hash = hashlib.sha256(new_pswd.encode('utf-8')).hexdigest()
        try:
            datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Passwords"] = new_pswd_hash
            datos_usuarios.to_csv(DB_FILE, index=False)
            messagebox.showinfo(title="Éxito", message="Contraseña cambiada")
            logger.info('Contraseña cambiada con éxito')
        except PermissionError:
            logger.error('No se tienen permisos para acceder a la base de datos.')
            messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
            return False

    else:
        messagebox.showinfo(title="Error", message="Respuesta Incorrecta")
        logger.error('Intento de recuperación de contraseña fallida: Respuesta Secreta Incorrecta')
        
def Descuentos(username, stop_disc, mov_disc): 
    datos_usuarios = pd.read_csv("Usuarios.csv") 
        
    try:
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Descuento Parado"] = int(stop_disc) 
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Descuento Movimiento"] = int(mov_disc)
        datos_usuarios.to_csv(DB_FILE, index = False)
        return True
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False
    except ValueError:
        logger.error('Valor introducido no válido.')
        messagebox.showinfo(title="Error", message="El valor tiene que ser un número entero (porcenataje del total).")
        return False


def Descuentos_taxi(username, turno, tarifa): 
    datos_usuarios = pd.read_csv("Usuarios.csv") 
    try:
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Turno"] = turno 
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Tarifa extra"] = int(tarifa) 
        datos_usuarios.to_csv(DB_FILE, index = False)
        return True
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False
    except ValueError:
        logger.error('Valor introducido no válido.')
        messagebox.showinfo(title="Error", message="El valor tiene que ser un número entero (porcenataje del total).")
        return False
    
def Tarifa(empresa, tarifa_mov, tarifa_stp):
    datos_usuarios = pd.read_csv("Usuarios.csv")
    try:
        datos_usuarios.loc[datos_usuarios["Empresa"] == empresa, "Tarifa Mov"] = float(tarifa_mov)
        datos_usuarios.loc[datos_usuarios["Empresa"] == empresa, "Tarifa Stop"] = float(tarifa_stp)
        datos_usuarios.to_csv(DB_FILE, index = False)
        return True
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False


