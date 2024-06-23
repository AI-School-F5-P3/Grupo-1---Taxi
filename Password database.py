import pandas as pd
import hashlib

#Cuando tengamos una base de datos como tal
#datos_usuarios = pd.read_csv("usuarios.csv")


def LogIn(cambio = False):
    '''
    LogIn va a permitir un argumento 'cambio' que por defecto será falso, para poder cambiar la contraseña.
    La función en primer lugar va a pedir un nombre al usuario y comprobará mediante condicional if si existe ese nombre en nuestra base de datos.
    Si el usuario no existe, entendemos que es un usuario nuevo y le pedimos que nos de un nombre
    La función comprueba que el nombre no esté ya en uso, y mientras no se de un nombre nuevo seguira pidiendolo en bucle.
    Después se le pide una contraseña "segura", podríamos definir que significa que su contraseña sea segura e incluso solicitar una longitud concreta (o carácteres)
    Una vez tenemos la contraseña, esta se hashea utilizando sha-256 y se almacena de forma encriptada en nuestra base de datos, para aumentar la seguridad.
    Para permitir cambiar la contraseña, se introduce una pregunta y respuesta secreta definidas por el usuario, y que deberá responder correctamente en el caso de necesitar cambiarla. Se permiten 3 intentos para acertar la respuesta.
    Finalmente el usuario, su contraseña encriptada y la pregunta y respuesta secretas se añaden a la base de datos de usuarios.
    Si el usuario si existe, se le pedirá que introduzca su contraseña y está se buscara en la base de datos en su forma encriptada.
    Si hay coincidencias el programa de taximetro se inicia, si no, se le pide que repita la contraseña, hasta un máximo de 6 intentos.
    '''
    
    datos_usuarios = pd.read_csv("Usuarios.csv")
    if cambio:
        usuario = input("Escriba su nombre de usuario: ")
        if usuario not in datos_usuarios["Usuarios"].values:
            print("Este usuario no existe")
        else:
            secret_q = datos_usuarios.query('Usuarios == @usuario')["Pregunta Secreta"][1]
            secret_answ = hashlib.sha256(input(secret_q).encode('utf-8')).hexdigest()
            true_answ = datos_usuarios.query('Usuarios == @usuario')["Respuesta Secreta"][1]
            intentos = 0
            if secret_answ == true_answ:
                new_pass = input("Introduce tu nueva contraseña: ")
                new_pass_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
                datos_usuarios.query('Usuarios == @usuario')["Pregunta Secreta"][1]
                datos_usuarios.loc[datos_usuarios["Usuarios"] == usuario, "Passwords"] = new_pass_hash
                datos_usuarios.to_csv('Usuarios.csv', index = False)
                print("Contraseña Cambiada")
            else:
                while (secret_answ != true_answ):
                    if intentos == 4:
                        print("Demasiados intentos fallados, reinicie el programa")
                        break
                    else:
                        print("Respuesta incorrecta")
                        secret_answ = input(secret_q)
                        intentos += 1
                    
    else:
        usuario = input("Escriba su nombre de usuario: ")
        if usuario not in datos_usuarios["Usuarios"].values:
            print("Usuario no registrado.")
            user = input("Escriba un nombre de usuario")
            while user in datos_usuarios.Usuarios.isin([user]):
                user = input("Ese nombre de usuario ya está seleccionado. Escriba un nombre de usuario.")
            password = input("Escribe una contraseña segura")
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            secret_q = input("Escriba una pregunta que solo usted conozca la respuesta")
            secret_a = hashlib.sha256(input("Escriba la respuesta a su pregunta secreta").encode('utf-8')).hexdigest()
            df = pd.DataFrame({'Usuarios': [user], 'Passwords': [password_hash], 'Pregunta Secreta': secret_q, 'Respuesta Secreta': secret_a})
            datos_usuarios = pd.concat([datos_usuarios, df], ignore_index= True)
            datos_usuarios.to_csv('Usuarios.csv', index = False)
        else:
            password_inp = input("Escriba su contraseña: ")
            password_inp_hash = hashlib.sha256(password_inp.encode('utf-8')).hexdigest()
            intentos = 0
            password_local = datos_usuarios.query('Usuarios == @usuario')["Passwords"][1]
            while(password_inp_hash != password_local):
                if intentos == 6:
                    print("Demasiados intentos fallados, reinicie el programa")
                    break
                else:
                    print("Contraseña incorrecta")
                    password_inp = input("Escriba su contraseña: ")
                    password_inp_hash = hashlib.sha256(password_inp.encode('utf-8')).hexdigest()
                    intentos += 1
                
            else:
                print("Bienvenido")
                #taximetro()


def Iniciar(cambio = False):
    LogIn(cambio)

#Iniciar()

#Iniciar(True) Cambio de contraseña