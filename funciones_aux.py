import pandas as pd
import hashlib
import tkinter as tk
from tkinter import messagebox
from logger_config import logger
import os

# Asignación de variables de bases de datos
User_DB = "Usuarios.csv"
Empresa_DB = "Empresa.csv"
logger.info("Se crean las variables de bases de datos correctamente")

# Se verifica con os.path si la base de datos existe, si no, crear una nueva con pandas
if not os.path.exists(User_DB):
    logger.warning("La base de datos no existe. Se creará una nueva.")
    df = pd.DataFrame(columns=["Usuarios", "Passwords", "Pregunta Secreta", "Respuesta Secreta", "Licencia", "Descuento Parado", "Descuento Movimiento", "Turno", "Tarifa extra", "Tarifa Mov", "Tarifa Stop", "Empresa"])
    df.to_csv(User_DB, index=False)

def LogIn(username, password):
    '''
    Función para iniciar sesión en la interfaz gráfica de tkinter.
    En primer lugar se intenta capturar el error de que la base de datos no pueda accederse, generalmente se debe a que esté abierta a la vez que se intenta editar.
    En segundo lugar, para asegurar que el formato siempre es igual, se convierte el nombre de usuario a minúsuclas, y se codifica la contraseña en .sha256.
    En tercer lugar se intenta catpurar el error de que la base de que el usuario no se encuentre en la base de datos. Para ello se especifican dos errores:
        - ValueError. El valor introducido es inocrrecto.
        - IndexError: No se encuentra en el índice el usuario por lo que genera un error de índice (pandas no puede encontrar la instancia en la base).
    A continuación, una vez se solventan los errores, se comprueba si hay errores en el nombre de usuario o en la contraseña, en cuyo caso el inicio de sesión falla.
    Si todo ha salido bien, el inicio de sesión ha sido exitoso y se extrae la licencia registrada para ese usuario para su uso en la función principal.
    Todos los pasos se registran en el archivo de log.
    '''
    try:
        datos_usuarios = pd.read_csv(User_DB)
    except PermissionError:
        logger.warning('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False

    username = username.lower()
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        user_info = datos_usuarios[datos_usuarios["Usuarios"] == username].iloc[0]
        password_local = user_info["Passwords"]
    except ValueError:
        logger.error(f'Usuario {username} no encontrado en la base de datos. ')
        return False
    except IndexError:
        logger.error(f'Usuario {username} no encontrado en la base de datos. ')
        return False

    if username not in datos_usuarios["Usuarios"].values or password_inp != password_local:
        logger.warning(f'Intento de inicio de sesión fallido para usuario: {username}')
        return False
    else:
        logger.info(f'Inicio de sesión exitoso para usuario: {username}')
        return user_info["Licencia"]

def LogIn_Empresa(username, password):
    username = username.lower()
    try:
        datos_empresa = pd.read_csv("Empresa.csv")
    except PermissionError:
        logger.warning('No se tienen permisos para acceder a la base de datos.')
        #messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False
    except FileNotFoundError:
        logger.error('No hay empresas registradas en este momento')
        return False

    username = username.lower()
    password_inp = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try: 
        empresa_info = datos_empresa[datos_empresa["Usuarios"] == username].iloc[0]
    except IndexError:
        logger.error(f'Usuario {username} no encontrado')
        return False

    try:
        password_local = empresa_info["Passwords"]
    except ValueError:
        logger.error(f'Usuario {username} no encontrado en la base de datos. ')
        return False
    if username not in datos_empresa["Usuarios"].values or password_inp != password_local:
        logger.warning(f'Intento de inicio de sesión fallido para usuario: {username}')
        return False
    else:
        empresa = empresa_info["Empresa"]
        logger.info(f'Inicio de sesión exitoso para usuario: {username}')
        return empresa


def Register(username, password, s_quest, s_answer, conductor, empresa):
    try:
        datos_usuarios = pd.read_csv(User_DB)
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        #messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False

    username = username.lower()
    s_answer = s_answer.lower()
    empresa = empresa.lower()

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
        datos_usuarios.to_csv(User_DB, index=False)
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
        usuarios_info = datos_usuarios[datos_usuarios["Usuarios"] == username].iloc[0]
        pregunta_s = usuarios_info["Pregunta Secreta"]
        messagebox.showinfo(title = "Pregunta", message = pregunta_s)

def Respuesta(username, answer, new_pswd):
    try:
        datos_usuarios = pd.read_csv(User_DB)
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
        usuarios_info = datos_usuarios[datos_usuarios["Usuarios"] == username].iloc[0]
        local_answ = usuarios_info["Respuesta Secreta"]
    except ValueError:
        messagebox.showinfo(title="Error", message="Usuario no encontrado o respuesta incorrecta.")
        logger.error('Usuario no encontrado o respuesta incorrecta.')
        return False
    except IndexError:
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
            datos_usuarios.to_csv(User_DB, index=False)
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
    username = username.lower()
        
    try:
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Descuento Parado"] = int(stop_disc) 
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Descuento Movimiento"] = int(mov_disc)
        datos_usuarios.to_csv(User_DB, index = False)
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
    username = username.lower()
    try:
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Turno"] = turno 
        datos_usuarios.loc[datos_usuarios["Usuarios"] == username, "Tarifa extra"] = int(tarifa) 
        datos_usuarios.to_csv(User_DB, index = False)
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
        datos_usuarios.to_csv(User_DB, index = False)
        return True
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False


