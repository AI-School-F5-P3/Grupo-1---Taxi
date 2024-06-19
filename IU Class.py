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

        self.states = {'start': self.start, 'level': self.level}

        def Run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                self.states[(self.gameStateManager.get_state())].run()

                pygame.display.update()
                self.clock.tick(FPS)
        

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        def Run(self):
            self.display.fill('blue')
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.gameStateManager.set_state('start')

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        def Run(self):
            self.display.fill('red')
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.gameStateManager.set_state('level')

class gameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    
    def set_state(self):
        self.currentState = state
        

if __name__ == __main__:
    game = Game()
    game.run()