import pygame
from sys import exit

S_Width, S_Height = 800,400
FPS = 60

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((S_Width, S_Height))
        self.clock = pygame.time.Clock()
        
        def Run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                pygame.display.update()
                self.clock.tick(FPS)