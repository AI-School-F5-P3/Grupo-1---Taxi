import logging # la librería logging permite generar logs en un archivo externo y en la consola.
import os # la librería os permite interactuar con el sistema operativo, en este caso para cambiar de directorio.

def setup_logger():
    '''
    La función en primer lugar comprueba que estemos en la carpeta de trabajo correcta, en nuestro caso aquella en la que se encuentra la función main.py.
    Si no estamos en la carpeta adecuada se modifica automáticamente.
    Se inicializa el gestor de logs en la variable 'logger' utilizando la función getlogger de la biblioteca logging.
    Después se genera el 'gestor' para ir introduciendo los logs en un archivo externo, definido como 'taxi_app_logger.log' y que utilizará la codificación 'utf-8'
    Se especifica además el nivel (entendiendo nivel como la gravedad que presenta el mensaje) minimo que captura el logger. Con DEBUG capturamos todos los niveles más graves que DEBUG.
    Se añade también el 'gestor' para que los mensajes aparezcan además de en el archivo externo, en la consola a medida que se vaya ejecutando el programa.
    Posteriormente se especifica el formato en el que queremos que se generen los logs, en este caso 'asctime' define el formato de fecha (con fecha actual y hora, levelname define el nivel de gravedad del mensaje, y message muestra el mensaje que se ha especificado que se quiere loggear cuando se da la condición x.)
    Finalmente se añaden los gestores al 'logger' y el return devuelve el logger para utilizarlo en el cuerpo principal de la apliación.
    '''

    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith("funciones_aux.py")]: # usando un list comprehension para filtrar los archivos que terminan en funciones_aux.py
            os.chdir(dirpath)

    logger = logging.getLogger('taxi_app_logger') # Inicializar el gestor de logs.
    logger.setLevel(logging.DEBUG)
   
    # Crear un gestor de archivo 'fh' para guardar los logs en un archivo externo.
    fh = logging.FileHandler('taxi_app.log')
    fh.setLevel(logging.DEBUG) # Nivel de gravedad mínimo que captura el mensaje.
    # Se ha configurado el nivel de logging a DEBUG para capturar todos los niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    # Crear un gestor de archivo con encoding UTF-8
    fh = logging.FileHandler('taxi_app.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Crear un gestor de consola ('ch' console handler) para mostrar también los mensajes en la consola.
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Definir el formato del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # fecha actual y hora, nivel de gravedad del mensaje, mensaje que se quiere loggear.
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Agregar los gestores al logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger # Devolver el logger para utilizarlo en el cuerpo principal de la aplicación.

# Configurar el logger
logger = setup_logger()
