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
    En segundo lugar, para asegurar que el formato siempre es igual, se convierte el nombre de usuario a minúsuclas, y se codifica la contraseña se ecnripta usando el algoritmo sha-256.
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
    '''
    Función para iniciar sesión en la interfaz gráfica de tkinter.
    En primer lugar se intenta capturar el error de que la base de datos no pueda accederse, generalmente se debe a que esté abierta a la vez que se intenta editar. O que no haya un archivo porque no se ha registrado ninguna empresa en este momento.
    En segundo lugar, para asegurar que el formato siempre es igual, se convierte el nombre de usuario a minúsuclas, y se codifica la contraseña se ecnripta usando el algoritmo sha-256.
    En tercer lugar se intenta catpurar el error de que la base de que el usuario no se encuentre en la base de datos. Para ello se especifican dos errores:
        - ValueError. El valor introducido es inocrrecto.
        - IndexError: No se encuentra en el índice el usuario por lo que genera un error de índice (pandas no puede encontrar la instancia en la base).
    A continuación, una vez se solventan los errores, se comprueba si hay errores en el nombre de usuario o en la contraseña, en cuyo caso el inicio de sesión falla.
    Si todo ha salido bien, el inicio de sesión ha sido exitoso y se extrae la empresa correspondiente para ese usuario para su uso en la función principal.
    Todos los pasos se registran en el archivo de log.
    '''
    username = username.lower()
    try:
        datos_empresa = pd.read_csv(Empresa_DB)
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
    '''
    Función para registrar un conductor en la base de datos.
    En primer lugar se intenta capturar el error de que la base de datos no pueda accederse, generalmente se debe a que esté abierta a la vez que se intenta editar.
    En segundo lugar, para asegurar que el formato siempre es igual, se convierte el nombre de usuario, respuesta secreta y nombre de empresa a minúsuclas.
    En trecer lugar se incluyen una serie de controles para garantizar que se han rellenado todos los espacios en el registro de usuario y no se han dejado datos vacíos o con valores no válido (p.ej. la contraseña tiene que tener mínimo 4 caracteres).
    Una vez se han llevado a cabo estos controles, si se han resuelto satisfactoriamentes, se encripta la contraseña del usuario utilizando el algoritmo sha-256 y se genera una base de datos temporal con pandas incluyendo todos los datos del usuario. Despúes se concatena a la base de datos de usuarios y se guarda el archivo .csv con el mismo nombre, de esta forma actualizamos con cada registro la base de datos.
    '''
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
    '''
    Función para recuperar la pregunta secreta del usuario. 
    En primer lugar se convierte el nombre de usuario a mínusculas, formato en el que están los usuarios en la base de datos.
    Se capturan errores de no haber introducido un nombre de usuario o de que el usuario no exista en nuestra base de datos. 
    Si todo está en orden se muestra la pregunta secreta al usuario utilizando un pop-up definido en messagebox.showinfo de la biblioteca tkinter.
    '''
    username = username.lower()

    datos_usuarios = pd.read_csv(User_DB)

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
    '''
    Función que comprueba que el usuario haya introducido la respuesta secreta correcta. Se capturan los errores de no poder acceder a la base de datos (probablemente porque en ese momento esté abierta).
    Se convierten el usuario y la respuesta a mínusculas, formato en el que se encuentran en la base de datos y se comprueba que los formularios no estén vacíos.
    Si no hay errores, se comprueba que el usuario exista y que la respuesta introducida corresponde a aquella que se incluye en la base de datos para dicho usuario.
    Si se cumplen ambas condiciones se acepta la contraseña nueva que el usuario haya indicado (siempre que cumpla tener más de 4 caracteres), se encripta con sha-256 y se actualiza en la base de datos.
    Si ha habido errores al introducir la respuesta secreta, se avisa al usuario mediante un pop-up.
    '''
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
    '''
    Función que aplica, para el usuario con licencia VTC logeado, los descuentos que haya indicado en la pantalla de descuentos. Estos se guardan en formato int(entero) para poder trabajar con ellos correctamente en pygame. Se capturan además los errores de que no se tenga permiso de acceso a la base de datos o de que no se haya incluido un número entero. Podría trabajarse con numeros decimales, pero consideramos que es poco probable que alguien quiera hacer un descuento porcentual con decimales.
    '''
    datos_usuarios = pd.read_csv(User_DB) 
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
    '''
    Función que aplica, para el usuario con licencia de taxi logeado, la tarifa que haya señalado en la pantalla de tarifa. Este se guarda en formato int(entero) para poder trabajar correctamente en pygame. Se capturan además los errores de que no se tenga permiso de acceso a la base de datos o de que no se haya incluido un número entero. Podría trabajarse con numeros decimales, pero consideramos que es poco probable que alguien quiera hacer un descuento porcentual con decimales.
    '''
    datos_usuarios = pd.read_csv(User_DB) 
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
    '''
    Función que aplica las tarifas que haya indicado el representante de la empresa para todos los usuarios de dicha empresa. 
    Se comprueba que el valor sea númerico intentando convertirlo a entero (los inputs son siempre strings) en un try except. Si no se puede se devuelve el mensaje en pop-up de que tiene que introducirse un valor numérico.
    Se incluye además un breve condicional para que, si se incluye una tarifa con valor negativo se convierta al valor mínimo posible, un céntimo por segundo (0.01)
    Por último se captura el error de que no se tengan permisos de acceso a la base de datos.
    '''
    try:
        int(tarifa_mov)
        int(tarifa_stp)
    except ValueError:
        logger.error('No se ha introducido un número como valor')
        messagebox.showinfo(title="Error", message="Ha de introducirse un número")
        return False

    tarifa_mov = tarifa_mov if tarifa_mov >= 0.01 else 0.01
    tarifa_stp = tarifa_stp if tarifa_stp >= 0.01 else 0.01

    datos_usuarios = pd.read_csv(User_DB)
    try:
        datos_usuarios.loc[datos_usuarios["Empresa"] == empresa, "Tarifa Mov"] = float(tarifa_mov)
        datos_usuarios.loc[datos_usuarios["Empresa"] == empresa, "Tarifa Stop"] = float(tarifa_stp)
        datos_usuarios.to_csv(User_DB, index = False)
        return True
    except PermissionError:
        logger.error('No se tienen permisos para acceder a la base de datos.')
        messagebox.showinfo(title="Error", message="No se tienen permisos para acceder a la base de datos.")
        return False


