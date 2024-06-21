import pygame
from sys import exit

S_Width, S_Height = 800,400
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((S_Width, S_Height))
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = gameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen , self.gameStateManager)
        self.login = login(self.screen, self.gameStateManager)
        self.registro = registro(self.screen, self.gameStateManager)
        self.quit = quit(self.gameStateManager)

        self.states = {'start': self.start, 
                       'level': self.level, 
                       'login': self.login,
                       'registro': self.registro,
                       'quit': self.quit}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.states[(self.gameStateManager.get_state())].run()

            pygame.display.update()
            self.clock.tick(FPS)
        

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        #Variables generales
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        a,b = pygame.mouse.get_pos()
        login_screen = pygame.image.load('Graficos/start.jpg')
        font = pygame.font.SysFont('Lucida Console', 45)
        color_font = (200, 245, 10, 1)
        color_rect_hover = (91 ,23 ,202, 0.8)
        color_rect_base = (65, 0, 168, 0.9)
        #Boton Login
        login_button_rect = pygame.Rect(220, 50, 390, 55)
        login_text = font.render('Iniciar Sesion', True, color_font)
        #Boton Sign Up
        reg_button_rect = pygame.Rect(260, 150, 305, 55)
        reg_text = font.render('Registrarse', True, color_font)
        #Boton Quit
        quit_button_rect = pygame.Rect(360, 250, 120, 55)
        quit_text = font.render('Quit', True, color_font)
        self.display.blit(login_screen, (0,0))
        if quit_button_rect.x <= a <= quit_button_rect.x+120 and quit_button_rect.y <= b <= quit_button_rect.y+55:
            pygame.draw.rect(self.display, color_rect_hover, quit_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, quit_button_rect)

        if reg_button_rect.x <= a <= reg_button_rect.x+305 and reg_button_rect.y <= b <= reg_button_rect.y+55:
            pygame.draw.rect(self.display, color_rect_hover, reg_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, reg_button_rect)

        if login_button_rect.x <= a <= login_button_rect.x+390 and login_button_rect.y <= b <= login_button_rect.y+55:
            pygame.draw.rect(self.display, color_rect_hover, login_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, login_button_rect)   

        self.display.blit(login_text, (login_button_rect.x + 5, login_button_rect.y+5))
        self.display.blit(reg_text, (reg_button_rect.x + 5, reg_button_rect.y + 5))
        self.display.blit(quit_text, (quit_button_rect.x + 5, quit_button_rect.y + 5))
        
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('level')
        if mouse[0]:
            if quit_button_rect.collidepoint((a,b)):
                self.gameStateManager.set_state('quit')
            if login_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('login')
            if reg_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('registro')
        

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        first_screen = pygame.image.load('Graficos/start.jpg')
        self.display.blit(first_screen, (0,0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.gameStateManager.set_state('level')

class login:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        login = pygame.image.load('Graficos/login.jpg')
        self.display.blit(login, (0,0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.gameStateManager.set_state('start')

class registro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self):
        registro = pygame.image.load('Graficos/outrun2.jpg')
        self.display.blit(registro, (0,0))
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