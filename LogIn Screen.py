import pygame
from sys import exit

pygame.init()

#Tamaño de pantalla del juego
screen = pygame.display.set_mode((800, 400))
#Texto que figura en la ventana ejecutada
pygame.display.set_caption('Taximetro Interactivo')

#Reloj interno, para configurar la tasa de refreso del juego (fps)
clock = pygame.time.Clock()

first_screen = pygame.image.load('Graficos/road 2.jpg')
#Boton de LogIn
#Fuente para el boton de LogIn
login_font = pygame.font.SysFont('Lucida Console', 45)
#Rectangulo para el boton, (posicion ancho, posicion alto, tamaño ancho, tamaño alto)
login_button_rect = pygame.Rect(585, 70, 170, 62)
#Superficie donde se coloca el boton
login_text = login_font.render('Log In', True, (128, 245, 10, 1))

#Boton de registo
reg_font = pygame.font.SysFont('Lucida Console', 45)
reg_but_rect = pygame.Rect(560, 170, 220, 62)
reg_text = reg_font.render('Registro', True, (128, 245, 10, 1))

#Boton de quit
quit_font = pygame.font.SysFont('Lucida Console', 45)
quit_but_rect = pygame.Rect(610, 270, 120, 62)
quit_text = quit_font.render('Quit', True, (128, 245, 10, 1))

#Bucle de ejecución del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if quit_but_rect.collidepoint(event.pos):
                pygame.quit()
                exit()
    
    a,b = pygame.mouse.get_pos()
    if login_button_rect.x <= a <= login_button_rect.x + 190 and login_button_rect.y <= b <= login_button_rect.y + 70:
        pygame.draw.rect(screen, (91 ,23 ,202, 0.8), login_button_rect) #sin hover
    else:
        pygame.draw.rect(screen, (65, 0, 168, 0.9), login_button_rect) #con hover

    if reg_but_rect.x <= a <= reg_but_rect.x + 210 and reg_but_rect.y <= b <= reg_but_rect.y + 70:
        pygame.draw.rect(screen, (91 ,23 ,202, 0.8), reg_but_rect)
    else:
        pygame.draw.rect(screen, (65, 0, 168, 0.9), reg_but_rect)

    if quit_but_rect.x <= a <= quit_but_rect.x + 210 and quit_but_rect.y <= b <= quit_but_rect.y + 70:
        pygame.draw.rect(screen, (91 ,23 ,202, 0.8), quit_but_rect)
    else:
        pygame.draw.rect(screen, (65, 0, 168, 0.9), quit_but_rect)

    screen.blit(first_screen, (0, 0))
    screen.blit(login_text, (login_button_rect.x + 5, login_button_rect.y+5))
    screen.blit(reg_text, (reg_but_rect.x + 5, reg_but_rect.y+5))
    screen.blit(quit_text, (quit_but_rect.x + 5, quit_but_rect.y+5))

    pygame.display.update()
    clock.tick(60)