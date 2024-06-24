import pygame
from sys import exit
import pygame_gui
import time
from datetime import datetime
import pandas as pd

class Game:
    def __init__(self, user):
        self.FPS = 60
        self.S_Width = 1600
        self.S_Height = 900
        pygame.init()
        self.screen = pygame.display.set_mode((self.S_Width, self.S_Height))
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((self.S_Width, self.S_Height))
        self.user = user
        
        self.gameStateManager = gameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.intro = Intro(self.screen, self.gameStateManager)
        self.taximetro = Taximetro(self.screen, self.gameStateManager, self.user)
        self.pantalla_fin = pantalla_fin(self.screen, self.gameStateManager, self.user)
        self.quit = Quit(self.screen, self.gameStateManager)

        self.states = {'start': self.start, 
                       'taximetro': self.taximetro,
                       'intro': self.intro,
                       'pantalla_fin': self.pantalla_fin,
                       'quit': self.quit}
        
        self.gameStateManager.set_states(self.states)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit.handle_quit()

                # Manejar eventos específicos del estado actual
                self.states[self.gameStateManager.get_state()].handle_events(event)
            
            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(self.FPS)
        
class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.gameStateManager.set_state('level')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            a, b = pygame.mouse.get_pos()
            if self.quit_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('quit')
            elif self.login_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('intro')

    def run(self):
        # Variables generales
        a, b = pygame.mouse.get_pos()
        login_screen = pygame.image.load('Graficos/base_2.jpeg')
        font = pygame.font.SysFont('Lucida Console', 70)
        color_font = (200, 245, 10, 1)
        color_rect_hover = (91, 23, 202, 0.8)
        color_rect_base = (65, 0, 168, 0.9)
        # Botón Start
        self.login_button_rect = pygame.Rect(500, 400, 650, 80)
        login_text = font.render('Empezar carrera', True, color_font)
        # Botón Quit
        self.quit_button_rect = pygame.Rect(730, 650, 180, 80)
        quit_text = font.render('Quit', True, color_font)
        self.display.blit(login_screen, (0, 0))
        if self.quit_button_rect.collidepoint((a, b)):
            pygame.draw.rect(self.display, color_rect_hover, self.quit_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, self.quit_button_rect)

        if self.login_button_rect.collidepoint((a, b)):
            pygame.draw.rect(self.display, color_rect_hover, self.login_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, self.login_button_rect)   

        self.display.blit(login_text, (self.login_button_rect.x + 5, self.login_button_rect.y + 5))
        self.display.blit(quit_text, (self.quit_button_rect.x + 5, self.quit_button_rect.y + 5))

class Intro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.gameStateManager.set_state('taximetro')
                # Pasar el estado actual a Taximetro para iniciar el tiempo
                self.gameStateManager.get_states()['taximetro'].start_time = time.time()

    def run(self):
        fondo = pygame.image.load('Graficos/base_2.jpeg')
        self.display.blit(fondo, (0, 0))
        texto = pygame.image.load('Graficos/Intro_text (Mediana).png')
        self.display.blit(texto, (100, 100))

class Taximetro:
    def __init__(self, display, gameStateManager, user):
        self.user = user
        self.display = display
        self.gameStateManager = gameStateManager
        self.car = pygame.image.load('Graficos/car1.png')
        self.car_position = 20
        self.car_mov = False
        self.font = pygame.font.SysFont('Lucida Console', 30)
        self.start_time = None  # Inicializamos start_time como None
        self.score = 0
        self.datos_usuarios = pd.read_csv("Usuarios.csv")
        self.update_tarifas()

    def update_tarifas(self):
        user_info = self.datos_usuarios[self.datos_usuarios["Usuarios"] == self.user].iloc[0]
        licencia = user_info["Licencia"]

        if licencia == 'Taxista':
            turno = user_info["Turno"]
            if turno == 'Nocturno':
                self.porc = user_info["Tarifa extra"]
                self.tarifa_mov = 0.05+(0.05*(int(self.porc)/100))
                self.tarifa_par = 0.02+(0.02*(int(self.porc)/100))
            else:
                self.tarifa_mov = 0.05
                self.tarifa_par = 0.02
        else:
            disc_mov = user_info["Descuento Movimiento"]
            disc_stp = user_info["Descuento Parado"]

            self.tarifa_mov = 0.05-(0.05*(int(disc_mov)/100))
            self.tarifa_par = 0.02-(0.02*(int(disc_stp)/100))


    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.car_mov = not self.car_mov
            elif event.key == pygame.K_p:
                self.gameStateManager.set_state('start')
            elif event.key == pygame.K_RETURN:
                self.gameStateManager.set_state('pantalla_fin')

    def run(self):
        first_screen = pygame.image.load('Graficos/base_2.jpeg')
        self.display.blit(first_screen, (0, 0))
        color_font = (200, 245, 10, 1)

        if self.start_time is not None:  # Aseguramos que start_time tenga un valor antes de usarlo
            if self.car_mov:
                self.car_position += 5  # Ajusta la velocidad del coche según sea necesario
                if self.car_position > 1600:  # 1600 es el ancho de la pantalla
                    self.car_position = -self.car.get_width()  # Aparecer en el otro lado
                self.score += self.tarifa_mov / 60  # Incrementar la puntuación por segundo en movimiento
            else:
                self.score += self.tarifa_par / 60  # Incrementar la puntuación por segundo en parado

            self.display.blit(self.car, (self.car_position, 700))

            # Calcular el tiempo transcurrido en minutos y segundos
            elapsed_time_s = time.time() - self.start_time
            elapsed_minutes = int(elapsed_time_s // 60)
            elapsed_seconds = int(elapsed_time_s % 60)
            clock_text = self.font.render(f'Tiempo: {elapsed_minutes:02}:{elapsed_seconds:02}', True, (color_font))
            self.display.blit(clock_text, (50, 50))

            # Mostrar la puntuación
            score_text = self.font.render(f'Precio: {round(self.score, 2)} €', True, (color_font))
            self.display.blit(score_text, (50, 100))

    def reset(self):
        self.start_time = time.time()
        self.score = 0
        self.car_position = 20
        self.car_mov = False

    def get_score(self):
        return self.score
    
    def get_total_time(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

class gameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        self.states = None  # Inicializamos states como None

    def set_states(self, states):
        self.states = states  # Método para establecer los estados

    def get_states(self):
        return self.states  # Método para obtener los estados

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

class pantalla_fin:
    def __init__(self, display, gameStateManager, user):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.SysFont('Lucida Console', 70)
        self.color_font = (200, 245, 10, 1)
        self.color_background = (65, 0, 168, 0.9)
        self.final_price = 0
        self.total_time = 0
        self.user = user
        self.csv_updated = False  # Flag para controlar la escritura en el CSV
        self.time_stopped = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            a, b = pygame.mouse.get_pos()
            if self.quit_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('quit')
            elif self.login_button_rect.collidepoint((a, b)):
                self.gameStateManager.get_states()['taximetro'].reset()
                self.gameStateManager.set_state('intro')
                self.reset()

    def precio_final(self):
        a, b = pygame.mouse.get_pos()
        login_screen = pygame.image.load('Graficos/base_2.jpeg')
        font = pygame.font.SysFont('Lucida Console', 70)
        color_font = (200, 245, 10, 1)
        color_rect_hover = (91, 23, 202, 0.8)
        color_rect_base = (65, 0, 168, 0.9)
        # Botón Start
        self.login_button_rect = pygame.Rect(500, 400, 650, 80)
        login_text = font.render('Empezar otra carrera', True, color_font)
        # Botón Quit
        self.quit_button_rect = pygame.Rect(730, 650, 180, 80)
        quit_text = font.render('Quit', True, color_font)
        self.display.blit(login_screen, (0, 0))
        if self.quit_button_rect.collidepoint((a, b)):
            pygame.draw.rect(self.display, color_rect_hover, self.quit_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, self.quit_button_rect)

        if self.login_button_rect.collidepoint((a, b)):
            pygame.draw.rect(self.display, color_rect_hover, self.login_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, self.login_button_rect)   

        self.display.blit(login_text, (self.login_button_rect.x + 5, self.login_button_rect.y + 5))
        self.display.blit(quit_text, (self.quit_button_rect.x + 5, self.quit_button_rect.y + 5))
        price_text = self.font.render(f'Precio final: {round(self.final_price, 2)}€', True, self.color_font)
        minutos = int(self.total_time // 60)
        segundos = int(self.total_time % 60)
        time_text = self.font.render(f'Tiempo total de carrera: {minutos}m:{segundos}s', True, self.color_font)
        price_text_rect = price_text.get_rect(center = (800, 250))
        time_text_rect = time_text.get_rect(center = (800, 350))
        self.display.blit(price_text, price_text_rect)
        self.display.blit(time_text, time_text_rect)

    def run(self):
        if not self.time_stopped:  # Solo para cuando no está detenido aún
            self.final_price = self.gameStateManager.get_states()['taximetro'].get_score()
            self.total_time = self.gameStateManager.get_states()['taximetro'].get_total_time()
            self.time_stopped = True  # Detiene el tiempo al establecerlo la primera vez

        self.precio_final()
        self.today = datetime.now()
        self.d1 = self.today.strftime("%d/%m/%Y %H:%M:%S")

        if not self.csv_updated:  # Solo actualiza el CSV si no ha sido actualizado aún
            datos_usuarios = pd.read_csv('Carreras.csv')
            df = pd.DataFrame({'Usuario': [self.user], 'Fecha': [self.d1], 'Tiempo_Minutos': [int(self.total_time // 60)], 'Tiempo_Segundos': [int(self.total_time % 60)], 'Precio': [round(self.final_price, 2)]})
            datos_usuarios = pd.concat([datos_usuarios, df], ignore_index = True)
            datos_usuarios.to_csv('Carreras.csv', index = False)
            self.csv_updated = True  # Marca el CSV como actualizado
        
    def reset(self):
        self.final_price = 0
        self.total_time = 0
        self.time_stopped = False
        self.csv_updated = False

class Quit:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def handle_quit(self):
        self.gameStateManager.set_state('quit')

    def run(self):
        pygame.quit()
        exit()

def init_game(user):
    game = Game(user)
    game.run()