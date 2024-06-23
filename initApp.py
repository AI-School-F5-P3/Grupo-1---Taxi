import pandas as pd
import hashlib
import traceback
import datetime

path = "Usuarios.csv"

# Función para registrar acciones y errores
def registrar_accion(mensaje):
    with open("registro.txt", "a") as archivo:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"{timestamp} - {mensaje}\n")

def cargar_datos():
    try:
        # Intentar leer el archivo CSV
        datos_usuarios = pd.read_csv(path)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo
        print(f"El archivo {path} no se encontró. Creando una nueva base de datos.")
        datos_usuarios = pd.DataFrame(columns=['Usuarios', 'Passwords', 'Pregunta Secreta', 'Respuesta Secreta'])
        datos_usuarios.to_csv(path, index=False)
    except Exception as e:
        print(f"Ha ocurrido un error inesperado al cargar los datos: {e}")
        datos_usuarios = pd.DataFrame(columns=['Usuarios', 'Passwords', 'Pregunta Secreta', 'Respuesta Secreta'])
    return datos_usuarios

def registrar_usuario(datos_usuarios):
    try:
        print("Iniciando el registro de usuario")
        user = input("Escriba un nombre de usuario: ").strip().lower()
        while user in datos_usuarios["Usuarios"].str.lower().values:
            print("Ese nombre de usuario ya está seleccionado.")
            user = input("Escriba un nombre de usuario diferente: ").strip().lower()
        password = input("Escribe una contraseña segura: ").strip()
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        secret_q = input("Escriba una pregunta que solo usted conozca la respuesta: ").strip().lower()
        secret_a = hashlib.sha256(input("Escriba la respuesta a su pregunta secreta: ").strip().lower().encode('utf-8')).hexdigest()
        nuevo_usuario = pd.DataFrame({'Usuarios': [user], 'Passwords': [password_hash], 'Pregunta Secreta': [secret_q], 'Respuesta Secreta': [secret_a]})
        datos_usuarios = pd.concat([datos_usuarios, nuevo_usuario], ignore_index=True)
        datos_usuarios.to_csv(path, index=False)
        print("Usuario registrado correctamente.")
        registrar_accion(f"Nuevo usuario registrado: {user}")
    except Exception as e:
        print(f"Ha ocurrido un error al registrar usuario: {e}")
        registrar_accion(f"Error al registrar usuario: {e}")
        
def validar_contrasena(datos_usuarios, usuario): 
    password_inp = input("Escriba su contraseña: ").strip()
    # Control para que no introduzcan una contraseña vacía
    while not password_inp:
        print("La contraseña no puede estar vacía.")
        password_inp = input("Escriba su contraseña: ").strip()
    password_inp_hash = hashlib.sha256(password_inp.encode('utf-8')).hexdigest()
    intentos = 0
    password_local = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Passwords"].values[0]

    while password_inp_hash != password_local and intentos < 6:
        print("Contraseña incorrecta")
        registrar_accion(f"Contraseña incorrecta para usuario: {usuario}")
        password_inp = input("Escriba su contraseña: ").strip()
        while not password_inp:
            print("La contraseña no puede estar vacía.")
            password_inp = input("Escriba su contraseña: ").strip()
        password_inp_hash = hashlib.sha256(password_inp.encode('utf-8')).hexdigest()
        intentos += 1

    if password_inp_hash == password_local:
        print("Bienvenido")
        registrar_accion(f"Usuario autenticado correctamente: {usuario}")
        # Taximetro()
    else:
        print("Demasiados intentos fallidos, reinicie el programa")
            
def cambiar_contrasena(datos_usuarios, usuario):             
    secret_q = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Pregunta Secreta"].values[0]
    secret_answ = hashlib.sha256(input(secret_q).encode('utf-8')).hexdigest()
    true_answ = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Respuesta Secreta"].values[0]
    intentos = 0

    while secret_answ != true_answ and intentos < 3:
        print("Respuesta incorrecta")
        registrar_accion(f"Respuesta secreta incorrecta para usuario: {usuario}")
        secret_answ = hashlib.sha256(input(secret_q).encode('utf-8')).hexdigest()
        intentos += 1

    if secret_answ == true_answ:
        new_pass = input("Introduce tu nueva contraseña: ")
        while not new_pass:
            print("La contraseña no puede estar vacía.")
            new_pass = input("Introduce tu nueva contraseña: ").strip()
        current_pass_hash = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Passwords"].values[0]
        new_pass_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
        while new_pass_hash == current_pass_hash:
            print("La nueva contraseña no puede ser igual a la actual.")
            new_pass = input("Introduce tu nueva contraseña diferente a la actual: ").strip()
            while not new_pass:
                print("La contraseña no puede estar vacía.")
                new_pass = input("Introduce tu nueva contraseña: ").strip()
            new_pass_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()        
        datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Passwords"] = new_pass_hash
        datos_usuarios.to_csv(path, index=False)
        print("Contraseña Cambiada")
        registrar_accion(f"Contraseña cambiada para usuario: {usuario}")
    else:
        print("Demasiados intentos fallidos, reinicie el programa")
        registrar_accion(f"Demasiados intentos fallidos para cambiar contraseña de usuario: {usuario}")

def LogIn(cambio=False):
    datos_usuarios = cargar_datos()
    try:
        usuario = input("Escriba su nombre de usuario: ").lower()

        if cambio:
            if usuario not in datos_usuarios["Usuarios"].str.lower().values:
                print("Este usuario no existe")
                registrar_usuario(datos_usuarios)
                registrar_accion(f"Intento de (()(cambio de contraseña para usuario no existente: {usuario}")
            else:
                cambiar_contrasena(datos_usuarios, usuario)
        else:
            if usuario not in datos_usuarios["Usuarios"].str.lower().values:
                print("Usuario no registrado.")
                registrar_usuario(datos_usuarios)
            else:
                validar_contrasena(datos_usuarios, usuario)
    except Exception as e:
        registrar_accion(f"Error: {e}")
        registrar_accion(traceback.format_exc())
        print("Ha ocurrido un error. Por favor, revise el registro.")

def Iniciar():
    #LogIn(False)
    LogIn(True)
    
Iniciar()
#Iniciar(True)
