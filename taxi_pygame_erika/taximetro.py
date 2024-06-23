import pygame
import time
import csv
import os

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colores
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Cargar y redimensionar imágenes
road_image = pygame.image.load('taxi_pygame_erika/images/road.png')  # Ruta de tu imagen de carretera
road_image = pygame.transform.scale(road_image, (screen_width, screen_height))

car_image = pygame.image.load('taxi_pygame_erika/images/taxi.png')  # Ruta de tu imagen de taxi
car_width = 60
car_height = 100
car_image = pygame.transform.scale(car_image, (car_width, car_height))

# Posición inicial del coche
car_x = (screen_width - car_width) // 2
car_y = screen_height - car_height - 10

# Variables de tiempo y cobro
start_time = None
pause_start_time = None
total_time = 0
total_pause_time = 0
moving = False
paused = False

# Distancia
distance_per_step = 0.01  # Cada paso representa 0.01 km
total_distance = 0
initial_distance = 0

# Posiciones para el desplazamiento de la carretera
road_y1 = 0
road_y2 = -screen_height

# Datos del viaje
events = []
driver_name = "John Doe"
passenger_name = "Jane Doe"
license_plate = "ABC123"
passenger_count = 1

# Leer el último ID usado desde un archivo
def get_last_trip_id():
    if os.path.exists('last_trip_id.txt'):
        with open('last_trip_id.txt', 'r') as file:
            return int(file.read().strip())
    return 0

# Guardar el último ID usado en un archivo
def save_last_trip_id(trip_id):
    with open('last_trip_id.txt', 'w') as file:
        file.write(str(trip_id))

# Obtener el siguiente ID de viaje
last_trip_id = get_last_trip_id()
trip_id = last_trip_id + 1

# Función para mostrar texto en la pantalla
def display_text(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Función para calcular el costo del viaje
def calculate_fare(total_time, total_pause_time):
    total_time_minutes = total_time / 60
    total_pause_minutes = total_pause_time / 60
    moving_time = total_time_minutes - total_pause_minutes
    fare = 1 + (moving_time * 3)
    return fare

# Bucle principal del juego
running = True
clock = pygame.time.Clock()  # Objeto para controlar la velocidad de fotogramas
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controles del coche
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Iniciar movimiento
                if not moving:
                    moving = True
                    paused = False
                    start_time = time.time()
                    initial_distance = total_distance  # Distancia inicial al arrancar
                    events.append({
                        'event': 'start',
                        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
                    })
                else:
                    paused = not paused
                    if paused:
                        pause_start_time = time.time()
                        events.append({
                            'event': 'pause',
                            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pause_start_time))
                        })
                    else:
                        pause_end_time = time.time()
                        total_pause_time += pause_end_time - pause_start_time
                        events.append({
                            'event': 'resume',
                            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pause_end_time))
                        })
            elif event.key == pygame.K_f:  # Finalizar carrera
                moving = False
                end_time = time.time()
                total_time = end_time - start_time - total_pause_time
                final_distance = total_distance  # Distancia final al terminar
                fare = calculate_fare(total_time, total_pause_time)
                events.append({
                    'event': 'end',
                    'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)),
                    'total_time': total_time,
                    'total_pause_time': total_pause_time,
                    'fare': fare,
                    'initial_distance': initial_distance,
                    'final_distance': final_distance,
                    'total_distance': final_distance - initial_distance
                })
                print(f"Fare: {fare} Euros")
                running = False

    # Actualizar posición del coche y la carretera
    if moving and not paused:
        car_y -= 5  # Ajusta la velocidad del coche aquí
        total_distance += distance_per_step  # Incrementar distancia
        road_y1 += 5
        road_y2 += 5

        # Reiniciar la posición de la carretera para crear un bucle
        if road_y1 >= screen_height:
            road_y1 = -screen_height
        if road_y2 >= screen_height:
            road_y2 = -screen_height

    # Asegurarse de que el coche no desaparezca de la pantalla
    if car_y < 0:
        car_y = screen_height - car_height - 10

    # Dibujar la carretera y el coche
    screen.blit(road_image, (0, road_y1))
    screen.blit(road_image, (0, road_y2))
    screen.blit(car_image, (car_x, car_y))

    # Mostrar texto en pantalla
    display_text(f"Total Time: {total_time / 60:.2f} mins", 30, blue, 10, 10)
    display_text(f"Total Pause Time: {total_pause_time / 60:.2f} mins", 30, blue, 10, 40)
    display_text(f"Driver: {driver_name}", 30, blue, 10, 70)
    display_text(f"Passenger: {passenger_name}", 30, blue, 10, 100)
    display_text(f"License Plate: {license_plate}", 30, blue, 10, 130)
    display_text(f"Passenger Count: {passenger_count}", 30, blue, 10, 160)
    display_text(f"Distance: {total_distance:.2f} km", 30, blue, 10, 190)
    display_text(f"Press 'F' to finish the trip", 30, red, 10, 220)

    # Actualizar la pantalla
    pygame.display.flip()

    # Calcular tiempos y costos
    if moving:
        if paused:
            pause_duration = time.time() - pause_start_time
            display_text(f"Paused: {int(pause_duration)} s", 30, red, 10, 250)
        else:
            total_time = time.time() - start_time - total_pause_time

    # Limitar la velocidad de fotogramas
    clock.tick(60)

# Guardar datos de eventos al salir en un archivo CSV
with open('events.csv', 'a', newline='') as csvfile:  # Cambiado a 'a' para append
    fieldnames = ['trip_id', 'driver_name', 'passenger_name', 'license_plate', 'passenger_count', 'event', 'time', 'total_time', 'total_pause_time', 'fare', 'initial_distance', 'final_distance', 'total_distance']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if os.path.getsize('events.csv') == 0:  # Escribir el encabezado solo si el archivo está vacío
        writer.writeheader()

    for event in events:
        event_data = {
            'trip_id': trip_id,
            'driver_name': driver_name,
            'passenger_name': passenger_name,
            'license_plate': license_plate,
            'passenger_count': passenger_count,
            'event': event['event'],
            'time': event['time'],
            'total_time': event.get('total_time', ''),
            'total_pause_time': event.get('total_pause_time', ''),
            'fare': event.get('fare', ''),
            'initial_distance': event.get('initial_distance', ''),
            'final_distance': event.get('final_distance', ''),
            'total_distance': event.get('total_distance', '')
        }
        writer.writerow(event_data)

# Guardar el último ID usado
save_last_trip_id(trip_id)

# Salir de Pygame
pygame.quit()
