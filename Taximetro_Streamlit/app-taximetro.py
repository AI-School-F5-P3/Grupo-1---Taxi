import streamlit as st
import time

class Taximetro:
    def __init__(self):
        self.carrera_iniciada = False
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.tarifa_parado = 0.02  # Tarifa en céntimos por segundo cuando el taxi está parado
        self.tarifa_movimiento = 0.05  # Tarifa en céntimos por segundo cuando el taxi está en movimiento 
        self.total_cobrado = 0.0

    def iniciar_carrera(self):
        if not self.carrera_iniciada:
            self.carrera_iniciada = True
            self.tiempo_inicio = time.time()
            st.write("La carrera ha comenzado.")

    def terminar_carrera(self):
        if self.carrera_iniciada:
            self.carrera_iniciada = False
            self.tiempo_fin = time.time()
            tiempo_total = self.tiempo_fin - self.tiempo_inicio
            self.total_cobrado += tiempo_total * (self.tarifa_parado if tiempo_total < 1 else self.tarifa_movimiento)
            st.write(f"La carrera ha terminado. Total cobrado: {self.total_cobrado:.2f} Euros.")
        else:
            st.write("La carrera no ha comenzado.")

    def agregar_tiempo_movimiento(self, segundos):
        if self.carrera_iniciada:
            self.total_cobrado += segundos * self.tarifa_movimiento
            st.write(f"Se ha agregado tiempo de movimiento: {segundos} segundos.")
        else:
            st.write("La carrera no ha comenzado.")

    def agregar_tiempo_parado(self, segundos):
        if self.carrera_iniciada:
            self.total_cobrado += segundos * self.tarifa_parado
            st.write(f"Se ha agregado tiempo de parada: {segundos} segundos.")
        else:
            st.write("La carrera no ha comenzado.")

# Función principal de la aplicación
def main():
    st.title("Simulador de Taxímetro")

    # Crear instancia de Taximetro
    taximetro = Taximetro()

    if 'taximetro' not in st.session_state:
        st.session_state.taximetro = Taximetro()
        st.session_state.tiempo_inicio = None
        st.session_state.carrera_iniciada = False

    # Iniciar carrera
    if st.button("Iniciar Carrera") and not st.session_state.carrera_iniciada:
        st.session_state.taximetro.iniciar_carrera()
        st.session_state.tiempo_inicio = time.time()
        st.session_state.carrera_iniciada = True

    # Agregar tiempo de movimiento
    tiempo_movimiento = st.number_input("Agregar tiempo de movimiento (segundos)", min_value=0, step=1)
    if st.button("Agregar Tiempo de Movimiento"):
        st.session_state.taximetro.agregar_tiempo_movimiento(tiempo_movimiento)

    # Agregar tiempo parado
    tiempo_parado = st.number_input("Agregar tiempo de parada (segundos)", min_value=0, step=1)
    if st.button("Agregar Tiempo de Parada"):
        st.session_state.taximetro.agregar_tiempo_parado(tiempo_parado)

    # Terminar carrera
    if st.button("Terminar Carrera") and st.session_state.carrera_iniciada:
        st.session_state.taximetro.terminar_carrera()
        st.session_state.carrera_iniciada = False

    # Mostrar total cobrado
    st.write(f"Total cobrado: {st.session_state.taximetro.total_cobrado:.2f} Euros")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
