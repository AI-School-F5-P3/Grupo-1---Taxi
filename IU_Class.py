import pygame
from sys import exit
import pygame_gui

class Game:
    def __init__(self):
        self.FPS = 60
        self.S_Width = 1600
        self.S_Height = 900
        pygame.init()
        self.screen = pygame.display.set_mode((self.S_Width, self.S_Height))
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((self.S_Width, self.S_Height))
        
        self.gameStateManager = gameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.intro = Intro(self.screen, self.gameStateManager)
        self.taximetro = Taximetro(self.screen, self.gameStateManager)
        self.quit = Quit(self.gameStateManager)

        self.states = {'start': self.start, 
                       'taximetro': self.taximetro,
                       'intro': self.intro,
                       'quit': self.quit}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
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

    def run(self):
        fondo = pygame.image.load('Graficos/base_2.jpeg')
        self.display.blit(fondo, (0, 0))
        texto = pygame.image.load('Graficos/Intro_text (Mediana).png')
        self.display.blit(texto, (100, 100))

class Taximetro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.car = pygame.image.load('Graficos/car1.png')
        self.car_position = 20
        self.car_mov = False
        self.font = pygame.font.SysFont('Lucida Console', 30)
        self.start_time = pygame.time.get_ticks()
        self.score = 0

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.car_mov = not self.car_mov
            elif event.key == pygame.K_p:
                self.gameStateManager.set_state('start')

    def run(self):
        first_screen = pygame.image.load('Graficos/base_2.jpeg')
        self.display.blit(first_screen, (0, 0))
        color_font = (200, 245, 10, 1)

        if self.car_mov:
            self.car_position += 2  # Ajusta la velocidad del coche según sea necesario
            if self.car_position > 1600:  # 1600 es el ancho de la pantalla
                self.car_position = -self.car.get_width()  # Aparecer en el otro lado

        self.display.blit(self.car, (self.car_position, 700))

        # Calcular el tiempo transcurrido
        elapsed_time_ms = pygame.time.get_ticks() - self.start_time
        elapsed_minutes = elapsed_time_ms // 60000
        elapsed_seconds = (elapsed_time_ms % 60000) // 1000
        clock_text = self.font.render(f'Tiempo transcurrido: {elapsed_minutes:02}:{elapsed_seconds:02}', True, (color_font))
        self.display.blit(clock_text, (50, 50))

        # Mostrar la puntuación
        score_text = self.font.render(f'Precio: {self.score}', True, (color_font))
        self.display.blit(score_text, (50, 100))

class gameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

class Quit:
    def __init__(self, gameStateManager):
        self.gameStateManager = gameStateManager
    def run(self):
        pygame.quit()
        exit()

game = Game()
game.run()

def init_game():
    game = Game()
    game.run()