import logging
import os

def setup_logger():
    cwd = os.getcwd()
    base_folder = os.path.basename(cwd)
    if base_folder != 'Grupo-1---Taxi-main':
        os.chdir('Grupo-1---Taxi-main')
    logger = logging.getLogger('taxi_app_logger')
    logger.setLevel(logging.DEBUG)
   
    # Crear un manejador de archivo
    fh = logging.FileHandler('taxi_app.log')
    fh.setLevel(logging.DEBUG)

    # Crear un manejador de archivo con encoding UTF-8
    fh = logging.FileHandler('taxi_app.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Crear un manejador de consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Definir el formato del log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Agregar los manejadores al logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Configurar el logger
logger = setup_logger()
