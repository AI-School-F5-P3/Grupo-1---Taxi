import time
from logger import configurar_logger
import json
import os

def cargar_configuracion(archivo_config):
    directorio_actual = os.path.dirname(__file__)
    ruta_config = os.path.join(directorio_actual, archivo_config)
    with open(ruta_config, 'r') as f:
        return json.load(f)
    #with open(archivo_config, 'r') as f:
        #return json.load(f)

config = cargar_configuracion('config.json')

class Taxi:
    def __init__(self):
        self.logger = configurar_logger(self.__class__.__name__)
        self.tiempo_inicio = None
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_actual = 'parado'
        self.logger.info("Taxi inicializado.")

    def iniciar_carrera(self):
        if self.estado_actual != 'parado':
            self.logger.error("Intento de iniciar una nueva carrera mientras otra está en curso.")
            raise ValueError("No se puede iniciar una nueva carrera mientras otra está en curso.")
        self.tiempo_inicio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_actual = 'parado'
        self.logger.info("Carrera iniciada.")

    def cambiar_estado(self, nuevo_estado):
        if self.estado_actual == nuevo_estado:
            self.logger.error(f"Intento de cambiar al mismo estado '{nuevo_estado}'.")
            raise ValueError(f"El taxi ya está en estado '{nuevo_estado}'.")

        tiempo_actual = time.time()
        if self.estado_actual == 'parado':
            self.tiempo_parado += tiempo_actual - self.tiempo_inicio
        elif self.estado_actual == 'movimiento':
            self.tiempo_movimiento += tiempo_actual - self.tiempo_inicio

        self.tiempo_inicio = tiempo_actual
        self.estado_actual = nuevo_estado
        self.logger.info(f"Estado cambiado a '{nuevo_estado}'.")

    def finalizar_carrera(self):
        if self.tiempo_inicio is None:
            self.logger.error("Intento de finalizar una carrera que no ha comenzado.")
            raise ValueError("No hay una carrera en curso para finalizar.")

        tiempo_actual = time.time()
        if self.estado_actual == 'parado':
            self.tiempo_parado += tiempo_actual - self.tiempo_inicio
        elif self.estado_actual == 'movimiento':
            self.tiempo_movimiento += tiempo_actual - self.tiempo_inicio

        costo_total = (self.tiempo_parado * config["precio_parado"]) + (self.tiempo_movimiento * config["precio_movimiento"])
        self.__registrar_carrera(costo_total)
        self.__init__()  # Resetear el estado del taxi
        self.logger.info(f"Carrera finalizada. Costo total: €{costo_total:.2f}")
        return costo_total

    def __registrar_carrera(self, costo_total):
        with open('historial.txt', 'a') as f:
            f.write(f"Carrera finalizada - Costo total: €{costo_total:.2f}\n")
        self.logger.info("Carrera registrada en el historial.")
