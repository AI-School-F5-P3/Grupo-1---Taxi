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
        self.taximetro = Taximetro(self.screen , self.gameStateManager)
        self.quit = quit(self.gameStateManager)

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

            self.states[(self.gameStateManager.get_state())].run()

            pygame.display.update()
            self.clock.tick(self.FPS)
        

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        #Variables generales
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        a,b = pygame.mouse.get_pos()
        login_screen = pygame.image.load('Graficos/road_big.jpg')
        font = pygame.font.SysFont('Lucida Console', 70)
        color_font = (200, 245, 10, 1)
        color_rect_hover = (91 ,23 ,202, 0.8)
        color_rect_base = (65, 0, 168, 0.9)
        #Boton Start
        login_button_rect = pygame.Rect(450, 337.5, 650, 80)
        login_text = font.render('Empezar carrera', True, color_font)
        #Boton Quit
        quit_button_rect = pygame.Rect(650, 600, 180, 80)
        quit_text = font.render('Quit', True, color_font)
        self.display.blit(login_screen, (0,0))
        if quit_button_rect.x <= a <= quit_button_rect.x+120 and quit_button_rect.y <= b <= quit_button_rect.y+55:
            pygame.draw.rect(self.display, color_rect_hover, quit_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, quit_button_rect)

        if login_button_rect.x <= a <= login_button_rect.x+830 and login_button_rect.y <= b <= login_button_rect.y+123.75:
            pygame.draw.rect(self.display, color_rect_hover, login_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, login_button_rect)   

        self.display.blit(login_text, (login_button_rect.x + 5, login_button_rect.y+5))
        self.display.blit(quit_text, (quit_button_rect.x + 5, quit_button_rect.y + 5))
        
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('level')
        if mouse[0]:
            if quit_button_rect.collidepoint((a,b)):
                self.gameStateManager.set_state('quit')
            if login_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('intro')

class Intro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        fondo = pygame.image.load('Graficos/road_big.jpg')
        self.display.blit(fondo, (0,0))
        texto = pygame.image.load('Graficos/Intro_text (Mediana).png')
        self.display.blit(texto, (100, 100))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.gameStateManager.set_state('taximetro')

        
class Taximetro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        first_screen = pygame.image.load('Graficos/road_big.jpg')
        self.display.blit(first_screen, (0,0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.gameStateManager.set_state('start')

class gameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

class quit:
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
