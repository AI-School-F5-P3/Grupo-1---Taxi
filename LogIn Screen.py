import pygame
from sys import exit

pygame.init()

#Tamaño de pantalla del juego
screen = pygame.display.set_mode((800, 400))
#Texto que figura en la ventana ejecutada
pygame.display.set_caption('Taximetro Interactiv')

#Reloj interno, para configurar la tasa de refreso del juego (fps)
clock = pygame.time.Clock()

first_screen = pygame.image.load('Graficos/road 2.jpg')
#Boton de LogIn
#Fuente para el boton de LogIn
login_font = pygame.font.SysFont('Lucida Console', 50)
#Rectangulo para el boton, (posicion ancho, posicion alto, tamaño ancho, tamaño alto)
login_button_rect = pygame.Rect(575, 100, 190, 70)
#Superficie donde se coloca el boton
login_text = login_font.render('Log In', True, 'red')

#Bucle de ejecución del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if login_button_rect.collidepoint(event.pos):
                pygame.quit()
                exit()
    a,b = pygame.mouse.get_pos()
    if login_button_rect.x <= a <= login_button_rect.x + 190 and login_button_rect.y <= b <= login_button_rect.y + 70:
        pygame.draw.rect(screen, (180,180,180), login_button_rect)
    else:
        pygame.draw.rect(screen, (110, 110, 110), login_button_rect)

    screen.blit(first_screen, (0, 0))
    screen.blit(login_text, (login_button_rect.x + 5, login_button_rect.y+5))

    pygame.display.update()
    clock.tick(60)