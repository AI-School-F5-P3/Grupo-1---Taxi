import logging # Biblioteca para generar los logs

def creador_logs():
    ''' 
    Se crea una función que va a iniciar el proceso de logear los sucesos.
    getLogger es una función de la biblioteca logging, a la que le asignamos __name__ que asigna a la variable el nombre del modulo a emplear
    basicConfig permite configurar los logs que se van a producir
    Por último devemos devolver el logger que hemos creado
    '''
    logger = logging.getLogger(__name__) 
    logging.basicConfig(filename = 'archivo_logs.log', #nombre del archivo
                        level = logging.INFO,  #nivel mínimo para el que va a generarse logs (mirar tabla https://docs.python.org/3/library/logging.html#levels)
                        format='%(asctime)s - %(levelname)s - %(message)s', #formato de presentación del log, asctime será la hora, levelname el nombre del nivel del mensaje y message el mensaje que nosotros asignemos
                        datefmt='%d/%m/%Y %I:%M:%S: %p') #formato de fecha, puesto para día, mes, año, hora, minuto, segundo y AM o PM.
    return logger


def taximetro():
    logger = creador_logs() #llamamos a la función previa
    ''' 
    El código a continuación es meramente una prueba para ver como funcinaría el logger
    Los diferentes niveles se establecen con un .level(.info/.error) que saldrán en el archivo del log
    '''
    logger.info("Inicio del log")
    movimiento = 0.05
    parado = 0.02
    try: # Para guardar los errores utilizar un try/except
        movimiento/0
        logger.info("Funcionando")
        logger.info("Final")
    except ZeroDivisionError:
        logger.error("Se ha producido un error")

taximetro()