import pandas as pd
import hashlib
import traceback
import datetime

# Especifica la ruta del archivo CSV donde se almacenan los datos de los usuarios.
path = "Usuarios.csv"

def register_action(mensaje):
# Función para registrar acciones y errores.
# Registra mensajes de acciones y errores en un archivo de registro (registro.txt) con una marca de tiempo.
    with open("registro.txt", "a") as archivo:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"{timestamp} - {mensaje}\n")

def load_data():
# Función que intenta cargar los datos del archivo CSV especificado en path. 
# Si el archivo no existe, crea uno nuevo con las columnas Usuarios, Passwords, PreguntaSecreta y Respuesta Secreta.
    try:
        # Intentar leer el archivo CSV
        datos_usuarios = pd.read_csv(path)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo
        print(f"El archivo {path} no se encontró. Creando una nueva base de datos.")
        datos_usuarios = pd.DataFrame(columns=['Usuarios', 'Passwords', 'PreguntaSecreta', 'RespuestaSecreta', 'TipoConductor', 'TarifaParado', 'TarifaMovimiento'])
        datos_usuarios.to_csv(path, index=False)
    except Exception as e:
        print(f"Ha ocurrido un error inesperado al cargar los datos: {e}")
        datos_usuarios = pd.DataFrame(columns=['Usuarios', 'Passwords', 'PreguntaSecreta', 'RespuestaSecreta', 'TipoConductor', 'TarifaParado', 'TarifaMovimiento'])
    return datos_usuarios

def request_input(mensaje, validacion=None):
# Solicita una entrada del usuario y valida la entrada usando una función de validación opcional
    while True:
        entrada = input(mensaje).strip()
        if validacion and not validacion(entrada):
            print("La contreña ha de tener como mínimo 8 caracteres. Inténtalo de nuevo.")
        else:
            return entrada

def validate_password_format(contrasena):
# Valida que la contraseña tenga al menos 8 caracteres
    return len(contrasena) >= 8

def request_password(mensaje):
# Solicita una contraseña del usuario y valida que tenga al menos 8 caracteres
    return request_input(mensaje, validate_password_format)

def register_user(datos_usuarios):
    ''' 
    Esta función registra un nuevo usuario:
    1. Solicita un nombre de usuario y verifica que no esté en uso.
    2. Solicita una contraseña, pregunta secreta y respuesta secreta.
    3. Guarda los datos del nuevo usuario en el archivo CSV.
    '''
    try:
        print("Iniciando el registro de usuario")
        user = request_input("Escriba un nombre de usuario: ").lower()
        while user in datos_usuarios["Usuarios"].str.lower().values:
            print("Ese nombre de usuario ya está seleccionado.")
            user = request_input("Escriba un nombre de usuario diferente: ").lower()
        password = request_password("Escribe una contraseña segura (mínimo 8 caracteres alfanuméricos): ")
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        secret_q = request_input("Escriba una pregunta que solo usted conozca la respuesta: ").lower()
        secret_a = hashlib.sha256(request_input("Escriba la respuesta a su pregunta secreta: ").encode('utf-8')).hexdigest()
        #nuevo_usuario = pd.DataFrame({'Usuarios': [user], 'Passwords': [password_hash], 'PreguntaSecreta': [secret_q], 'RespuestaSecreta': [secret_a]})
        #datos_usuarios = pd.concat([datos_usuarios, nuevo_usuario], ignore_index=True)
        #datos_usuarios.to_csv(path, index=False)
        
        # Código añadido para que añada las columnas correspondientes al tipo de conductor, 
        # tarifa parado y tarifa en movimiento
        tipo_conductor = request_input("Escriba el tipo de conductor (VTC o Taxi): ").lower()
        tarifa_parado = 0.02  # Inicialización de la variable
        tarifa_movimiento = 0.05  # Inicialización de la variable
        
        if tipo_conductor == "vtc":
            descuento_p = float(request_input("Ingrese el descuento en tarifa parado (%): "))
            descuento_m = float(request_input("Ingrese el descuento en tarifa movimiento (%): "))
            tarifa_parado_calc = tarifa_parado * (1 - descuento_p / 100)
            tarifa_movimiento_calc = tarifa_movimiento * (1 - descuento_m / 100)
            print(f'tarifa parado VTC {tarifa_parado_calc}, tarifa movimiento {tarifa_movimiento_calc}' )
            #conductor_obj = VTC(descuento_p, descuento_m)
        elif tipo_conductor == "taxi":
            es_noche = request_input("¿Es horario nocturno? (s/n): ").lower()
            if es_noche == "s":
                prcnt_noche = float(request_input("Ingrese el porcentaje de incremento por nocturnidad (%): "))
                tarifa_parado_calc = tarifa_parado * (1 + prcnt_noche / 100)
                tarifa_movimiento_calc = tarifa_movimiento * (1 + prcnt_noche / 100)
            print(f'tarifa parado taxi {tarifa_parado_calc}, tarifa movimiento {tarifa_movimiento_calc}' )
            #conductor_obj = taxista(es_noche, prcnt_noche)
        else:
            print("Tipo de conductor no válido.")
            return

        tarifa_parado = round(tarifa_parado_calc, 2)
        tarifa_movimiento = round(tarifa_movimiento_calc, 2)
        print(f'tarifa parado ¿redondeado? {tarifa_parado}, tarifa movimiento {tarifa_movimiento}' )
        #tarifa_parado = conductor_obj.tarifa_parado
        #tarifa_movimiento = conductor_obj.tarifa_movimiento
        
        nuevo_usuario = pd.DataFrame({
            'Usuarios': [user],
            'Passwords': [password_hash],
            'PreguntaSecreta': [secret_q],
            'RespuestaSecreta': [secret_a],
            'TipoConductor': [tipo_conductor],
            'TarifaParado': [tarifa_parado],
            'TarifaMovimiento': [tarifa_movimiento]
        })
        
        # Asegurarse de que las columnas estén alineadas correctamente
        datos_usuarios = datos_usuarios.reindex(columns=nuevo_usuario.columns)
        
        datos_usuarios = pd.concat([datos_usuarios, nuevo_usuario], ignore_index=True)
        datos_usuarios.to_csv(path, index=False)
        print("Usuario registrado correctamente.")
        register_action(f"Nuevo usuario registrado: {user}")
    except Exception as e:
        print(f"Ha ocurrido un error al registrar usuario: {e}")
        register_action(f"Error al registrar usuario: {e}")

def validate_password(datos_usuarios, usuario): 
    ''' 
    Esta función valida que la contraseña introducida por el usuario es correcta.
    En caso que no se introduzca la contraseña correcta en los 6 intentos, se pide al usuario que reinicie el programa
    '''
    intentos = 0
    password_local = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Passwords"].values[0]
    while intentos < 6:
        password_inp = request_password("Escriba su contraseña: ")
        password_inp_hash = hashlib.sha256(password_inp.encode('utf-8')).hexdigest()
        if password_inp_hash == password_local:
            print("Bienvenido")
            print(datos_usuarios)
            register_action(f"Usuario autenticado correctamente: {usuario}")
            return
        else:
            print("Contraseña incorrecta")
            register_action(f"Contraseña incorrecta para usuario: {usuario}")
        intentos += 1
    print("Demasiados intentos fallidos, reinicie el programa")

def change_password(datos_usuarios, usuario): 
    '''
    Cambia la contraseña del usuario:
    Verifica la respuesta a la pregunta secreta (hasta 3 intentos).
    Solicita una nueva contraseña que debe ser diferente a la actual.
    '''            
    secret_q = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "PreguntaSecreta"].values[0]
    true_answ = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "RespuestaSecreta"].values[0]
    intentos = 0

    while intentos < 3:
        secret_answ = hashlib.sha256(request_input(secret_q).encode('utf-8')).hexdigest()
        if secret_answ == true_answ:
            current_pass_hash = datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Passwords"].values[0]
            new_pass = request_password("Introduce tu nueva contraseña (mínimo 8 caracteres alfanuméricos): ")
            new_pass_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
            while new_pass_hash == current_pass_hash:
                print("La nueva contraseña no puede ser igual a la actual.")
                new_pass = request_password("Introduce tu nueva contraseña diferente a la actual: ")
                new_pass_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
            datos_usuarios.loc[datos_usuarios["Usuarios"].str.lower() == usuario, "Passwords"] = new_pass_hash
            datos_usuarios.to_csv(path, index=False)
            print("Contraseña cambiada")
            register_action(f"Contraseña cambiada para usuario: {usuario}")
            return
        else:
            print("Respuesta incorrecta")
            register_action(f"Respuesta secreta incorrecta para usuario: {usuario}")
        intentos += 1
    print("Demasiados intentos fallidos, reinicie el programa")
    register_action(f"Demasiados intentos fallidos para cambiar contraseña de usuario: {usuario}")

def login_user(cambio=False):
    '''
    Gestiona el inicio de sesión o cambio de contraseña:
    Carga los datos de usuarios.
    Si cambio es True, cambia la contraseña; si no, valida la contraseña.
    '''
    datos_usuarios = load_data()
    try:
        usuario = request_input("Escriba su nombre de usuario: ").lower()
        if cambio:
            if usuario not in datos_usuarios["Usuarios"].str.lower().values:
                print("Este usuario no existe")
                register_user(datos_usuarios)
                register_action(f"Intento de cambio de contraseña para usuario no existente: {usuario}")
            else:
                change_password(datos_usuarios, usuario)
        else:
            if usuario not in datos_usuarios["Usuarios"].str.lower().values:
                print("Usuario no registrado.")
                register_user(datos_usuarios)
            else:
                validate_password(datos_usuarios, usuario)
    except Exception as e:
        register_action(f"Error: {e}")
        register_action(traceback.format_exc())
        print("Ha ocurrido un error. Por favor, revise el registro.")

def start():
    '''
    Llama a la función login_user con el parámetro cambio
    Si cambio=True para start el proceso de cambio de contraseña al ejecutar el programa.
    Si cambio=False se inicia el proceso para start sesion en la aplicación
    '''
    login_user(False)
    #login_user(True)

start()
