import time

class Taxi:
    # __init__: Inicializa los atributos del taxi como el tiempo de inicio, 
    # tiempo acumulado parado, tiempo acumulado en movimiento y el estado actual.
    def __init__(self):
        self.tiempo_inicio = None
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_actual = 'parado'

    # Muestra un mensaje de bienvenida y los comandos disponibles
    def mostrar_bienvenida(self):
        print("¡Bienvenido al taxímetro digital!")
        print("Comandos disponibles:")
        print(" 1 - Inicia una nueva carrera.")
        print(" 2 - El taxi empieza a moverse.")
        print(" 3 - El taxi se detiene.")
        print(" 4 - Termina la carrera y muestra el costo total.")
        print(" 0 - Sale del programa.")

    # Inicializa una nueva carrera configurando el tiempo de inicio y reseteando 
    # los tiempos acumulados y el estado del taxi
    def iniciar_carrera(self):
        if self.estado_actual != 'parado':
            raise ValueError("No se puede iniciar una nueva carrera mientras otra está en curso.")
        
        print("\nCarrera iniciada. El taxi está parado.")
        self.tiempo_inicio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_actual = 'parado'

    # Cambia el estado del taxi entre "parado" y "movimiento", 
    # actualizando los tiempos acumulados según el estado previo
    def cambiar_estado(self, nuevo_estado):
        if self.estado_actual == nuevo_estado:
            raise ValueError(f"El taxi ya está en estado '{nuevo_estado}'.")
        
        tiempo_actual = time.time()
        if self.estado_actual == 'parado':
            self.tiempo_parado += tiempo_actual - self.tiempo_inicio
            print(f'Tiempo parado {self.tiempo_parado}')
        elif self.estado_actual == 'movimiento':
            self.tiempo_movimiento += tiempo_actual - self.tiempo_inicio
            print(f'Tiempo movimiento {self.tiempo_movimiento}')
        
        self.tiempo_inicio = tiempo_actual
        self.estado_actual = nuevo_estado
        print(f'Tiempo actual {tiempo_actual}')
        print(f"El taxi está ahora {nuevo_estado}.")

    # Finaliza la carrera, calcula el costo total y lo muestra al usuario. 
    # Luego, resetea los tiempos y el estado
    def finalizar_carrera(self):
        if self.tiempo_inicio is None:
            raise ValueError("No hay una carrera en curso para finalizar.")
        
        tiempo_actual = time.time()
        if self.estado_actual == 'parado':
            self.tiempo_parado += tiempo_actual - self.tiempo_inicio
        elif self.estado_actual == 'movimiento':
            self.tiempo_movimiento += tiempo_actual - self.tiempo_inicio

        costo_total = (self.tiempo_parado * 0.02) + (self.tiempo_movimiento * 0.05)
        print(f"\nCarrera finalizada. El costo total es: €{costo_total:.2f}\n")

        self.tiempo_inicio = None
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_actual = 'parado'

def main():
    # Crea una instancia de la clase Taxi
    taxi = Taxi()
    
    # Muestra el mensaje de bienvenida y los comandos disponibles
    taxi.mostrar_bienvenida()

    # Entra en un bucle para recibir y procesar los comandos del usuario,
    # manejando errores con bloques try-except:
    # Intenta convertir el comando ingresado a un entero.
    # Verifica que el comando esté en el rango válido (1-5)
    # Maneja los errores de valor y muestra un mensaje apropiado si el comando no es válido o si ocurre 
    # un error inesperado.

    while True:
        try:
            comando = int(input("Ingrese un comando (1-5): ").strip())
            if comando < 1 or comando > 5:
                raise ValueError("El comando debe estar entre 1 y 5.")

            if comando == 1:
                taxi.iniciar_carrera()
            elif comando == 2:
                taxi.cambiar_estado('movimiento')
            elif comando == 3:
                taxi.cambiar_estado('parado')
            elif comando == 4:
                taxi.finalizar_carrera()
            elif comando == 5:
                print("Saliendo del programa. ¡Gracias por usar el taxímetro digital!")
                break
        except ValueError as e:
            print(f"Error: {e}. Por favor, intente de nuevo.")
        except Exception as e:
            print(f"Error inesperado: {e}. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
