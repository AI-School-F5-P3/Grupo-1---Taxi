from taxi import Taxi

class TaximeterCLI:
    def __init__(self):
        self.taxi = Taxi()

    def mostrar_bienvenida(self):
        print("¡Bienvenido al taxímetro digital!")
        print("Comandos disponibles:")
        print(" 1 - Inicia una nueva carrera.")
        print(" 2 - El taxi empieza a moverse.")
        print(" 3 - El taxi se detiene.")
        print(" 4 - Termina la carrera y muestra el costo total.")
        print(" 5 - Sale del programa.")

    def ejecutar_comando(self, comando):
        try:
            if comando == 1:
                self.taxi.iniciar_carrera()
                print("Carrera iniciada. El taxi está parado.")
            elif comando == 2:
                self.taxi.cambiar_estado('movimiento')
                print("El taxi está ahora en movimiento.")
            elif comando == 3:
                self.taxi.cambiar_estado('parado')
                print("El taxi está ahora parado.")
            elif comando == 4:
                costo_total = self.taxi.finalizar_carrera()
                print(f"\nCarrera finalizada. El costo total es: €{costo_total:.2f}\n")
            elif comando == 5:
                print("Saliendo del programa. ¡Gracias por usar el taxímetro digital!")
                return False
            else:
                print("Comando no reconocido. Por favor, intente de nuevo.")
        except ValueError as e:
            print(f"Error: {e}. Por favor, intente de nuevo.")
        except Exception as e:
            print(f"Error inesperado: {e}. Por favor, intente de nuevo.")
        return True

def main():
    cli = TaximeterCLI()
    cli.mostrar_bienvenida()

    while True:
        try:
            comando = int(input("Ingrese un comando (1-5): ").strip())
            if comando < 1 or comando > 5:
                raise ValueError("El comando debe estar entre 1 y 5.")
            if not cli.ejecutar_comando(comando):
                break
        except ValueError as e:
            print(f"Error: {e}. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()