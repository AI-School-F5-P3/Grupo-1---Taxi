import pygame
from sys import exit
import pygame_gui
import time
from datetime import datetime
import pandas as pd
import numpy as np
from logger_config import logger

class Game:
    '''
    Se define la clase game, en el constructor __init__ se van a incluir las variables con las que vamos a trabajar a lo largo de la ejecución en los diferentes métodos.
    Se especifican los fps en 60 para que el movimiento del coche sea fluido cuando se ejecute.
    El tamaño de la pantalla se establece en 1600 de ancho y 900 de alto, que debería permitir adapatarse bien a la mayoría de pantallas de ordenador actuales.
    pygame.init() inicia la ejecución del módulo de pygame, y se genera la pantalla de la aplicación (pygame.display.set_mode) con las especificaciones previas.
    Se añade además una caption (display.set_caption) para que la ventana de la aplicación presente el nombre de nuestra aplicación 'taxea' y como icono nuestro logo (display.set_icon).
    Se guarda en una variable el reloj de pygame y en otra el gestor de eventos de pygame para la pantalla.
    Se guardan además el nombre de usuario que ha iniciado sesión y se genera una variable vacía empresa que luego usaremos.
    Especificaremos además los diferentes estados del juego con una función definida más adelante en el código llamada gameStateManager, que nos permitira ejecutar diferentes métodos de la clase game, correspondientes a las diferentes pantallas de juego.
    Start indica la pantalla de inicio
    Intro indica la pantalla de introducción al funcionamiento del juego
    Taximetro indica la pantalla del propio taximetro, donde mostraremos el movimiento del coche, los precios y gestionaremos los estados de movimiento y parada.
    Quit será el metodo que gestione el cierre de la aplicación para que se haga correctamente y sin errores.
    '''
    def __init__(self, user):
        self.FPS = 60
        self.S_Width = 1600
        self.S_Height = 900
        pygame.init()
        self.screen = pygame.display.set_mode((self.S_Width, self.S_Height))
        pygame.display.set_caption("Taxea")
        self.icon = pygame.image.load('Graficos/logo_cuadrado.png').convert_alpha()
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((self.S_Width, self.S_Height))
        self.user = user
        self.empresa = None

        logger.info(f'Juego iniciado para usuario: {user}') # Control de log
        
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
        '''
        El método run será el método de ejecución para todas las clases, en este caso es además el que controla el bucle principal de juego, de tal forma que el juego correrá (while True es siempre) hasta que llegue a un evento de cierre, en nuestro caso el estado Quit. 
        Dentro de este bucle hemos inlcuido un gestor de eventos, que es un método se incluye en todas las clases de la aplicación, el cual define y gestiona los eventos de juego como pulsar botones, hacer click del ratón etc. Necesarios para poder modificar los estados de juego y asegurar su correcto funcionamiento.
        Por último, el bucle incluye un display.update() que actualiza la pantalla con cada ejecución, con clock tick y fps definimos que serán 60 actualizaciones por segundo, para hacer una ejecución fluida visualmente.
        '''
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
    ''' 
    La clase Start recibe la información de la pantalla, que será siempre la que hemos definido en la clase game y el gameStateManager, que permite definir el estado en el que se encuentra la aplicación.
    '''
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def handle_events(self, event):
        ''' 
        Los eventos que debe capturar esta clase se refieren a los botones de 'empezar carrera' y 'quit' que se definirán en el método run. En este caso la función busca que se pulse un botón del raton, y que cuando se pulsa si su posición (obtenida con mouse.get_pos, donde a y b son eje x y eje y) esta dentro del rectangulo que define alguno de los dos botones, el estado del gameStateManager cambie del actual 'Start' al que corresponde 'Intro' o 'Quit'.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            a, b = pygame.mouse.get_pos()
            if self.quit_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('quit')
                logger.info('El taxista/vtc ha finalizado el viaje')
            elif self.login_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('intro')
                logger.info('El taxista/vtc ha empezado el viaje')

    def run(self):
        '''
        El método de ejecución genera todos los elementos de la pantalla de inicio.
        Image.load se utiliza para cargar las imágenes que queremos introducir en pantalla
        Con font.SysFont definimos la fuente del sistema (están instaladas por defecto en nuestro sistema operativo) y el tamaño que queremos usar.
        Se definen unas variables que guardarán los colores que vamos a utilzar en el método. En este caso tenemos que definirlo por el método RGBA.
        Después se definen los botones, que no serán otra cosa que unos rectangulos en los que debemos especificar su posición de inicio (x e y) y su tamaño (ancho y alto)
        Se define también el texto que queremos que se situe dentro de estos rectángulos para generar la sensación de un botón interactuable.
        Display.blit permite posicionar en pantalla cada uno de los elementos que estamos generando, es importante seguir un orden correcto ya que cada llamada a esta función coloca la imagen encima de lo que había antes.
        Para dar aún mas sensación de interactuabilidad y generar una mejor experiencia de usuario, especificamos un condicional para que, si la posición del raton (a y b) entran en la posición en la que se encuentra cada rectángulo se modifique el color a un gradiente más suave, de esta forma generamos la ilusión de poder clickarlo.
        Por último se coloca el texto dentro del rectángulo usando display.blit, para que se sitúe correctamente, como argumento de posición le pasamos la posición del rectangulo en ambos ejes + 5 pixeles, para que así hay algo de margen con el límite del rectángulo.
        '''
        # Variables generales
        a, b = pygame.mouse.get_pos()
        login_screen = pygame.image.load('Graficos/start_p.jpeg')
        logo = pygame.image.load('Graficos/logo_big.png')
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
        self.display.blit(logo, (700, 100))

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
        '''
        En este caso los eventos que queremos capturar es que se si se pulsa el botón (KEYDOWN) del teclado correspondiente a enter/return (K_RETURN) se cambia el estado de la aplicación a taximetro y empieza a contarse el tiempo de ejecución del taximetro.
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.gameStateManager.set_state('taximetro')
                self.gameStateManager.get_states()['taximetro'].start_time = time.time()
                logger.info('Pasa el estado actual a Taximetro para iniciar el tiempo')

    def run(self):
        fondo = pygame.image.load('Graficos/tuto.jpeg')
        self.display.blit(fondo, (0, 0))
        texto = pygame.image.load('Graficos/Texto intro.png')
        self.display.blit(texto, (175, 100))

class Taximetro:
    '''
    Taximetro es la clase que va a gestionar la mayor parte de nuestro programa. Incluye el movimiento del coche, el cálculo de tiempo y dinero y la creación y actualización de una base de datos que incluya las carreras que se vayan generando.
    Además de las variables que conocemos de las otras clases se incluyen clases importantes como:
    La imagen del coche que vamos a utilizar, cargada con image.load
    La posición en la pantalla en la que se situa el coche inicialmente
    Un flag que indica que el movimiento del coche al empezar es False (empiza parado)
    Definición de la fuente a utilizar.
    Una llamada al tiempo de inicio, se incluye para que se pueda modificar como hemos visto en la clase anterior.
    Se almacena el csv con los usuarios
    Y se llama a una función que actualiza las tarifas si se han modificado en el csv de usuarios.
    '''
    def __init__(self, display, gameStateManager, user):
        self.user = user
        self.display = display
        self.gameStateManager = gameStateManager
        self.car = pygame.image.load('Graficos/car.png')
        self.car_position = 20
        self.car_mov = False
        self.font = pygame.font.SysFont('Lucida Console', 30)
        self.start_time = None  # Inicializamos start_time como None
        self.score = 0
        self.datos_usuarios = pd.read_csv("Usuarios.csv")
        self.update_tarifas()

    def update_tarifas(self):
        '''
        Esta función se encarga de comprobar el precio de la tarifa que el usuario tiene asociado y la licencia de este.
        Si la tarifa no se encuentra en la base de datos (porque todavía no se haya añadido ninguna por ejemplo) se asigna a los valores por defecto de 0.05 y 0.02
        Si la licencia es de taxista, en el caso de que esté en turno nocturno, se añadirá a la tarifa base el valor de la tarifa base multiplicada por el valor del descuento y divido por 100. 
        Para la licencia de vtc se hace el mismo proceso pero en este caso se resta el valor del cálculo dado que se trata de un descuento y no de una tarifa extra por nocturnidad.
        '''
        user_info = self.datos_usuarios[self.datos_usuarios["Usuarios"] == self.user].iloc[0]
        licencia = user_info["Licencia"]
        tarifa_b_mov = 0.05 if np.isnan(user_info['Tarifa Mov']) else user_info['Tarifa Mov']
        tarifa_b_stop = 0.02 if np.isnan(user_info['Tarifa Stop']) else user_info['Tarifa Stop']
        logger.info(f'Actualización de tarifas para usuario: {self.user}')

        if licencia == 'Taxista':
            turno = user_info["Turno"]
            if turno == 'Nocturno':
                self.porc = user_info["Tarifa extra"]
                self.tarifa_mov = float(tarifa_b_mov)+(float(tarifa_b_mov)*(float(self.porc)/100))
                self.tarifa_par = float(tarifa_b_stop)+(float(tarifa_b_stop)*(float(self.porc)/100))
            else:
                self.tarifa_mov = tarifa_b_mov
                self.tarifa_par = tarifa_b_stop
        else:
            disc_mov = user_info["Descuento Movimiento"]
            disc_stp = user_info["Descuento Parado"]
            self.tarifa_mov = tarifa_b_mov-(tarifa_b_mov*(float(disc_mov)/100))
            self.tarifa_par = tarifa_b_stop-(tarifa_b_stop*(float(disc_stp)/100))

    def create_csv_if_not_exists(self, filename):
        '''
        Esta función creará el csv de las carreras, con las variables que hayamos definido previamente, en el caso de que no encuentre un archivo que abrir.
        '''
        try:
            pd.read_csv(filename)  # Intentar cargar el archivo
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Usuario', 'Fecha', 'Tiempo_Minutos', 'Tiempo_Segundos', 'Precio'])
            df.to_csv(filename, index=False)
            logger.info(f'Archivo CSV "{filename}" creado en tiempo de ejecución')


    def handle_events(self, event):
        '''
        En este caso los eventos que nos interesa capturar son, que se pulse en el teclado la tecla espacio (K_SPACE) la cual hará lo contrario del flag self.car, de tal forma que si es False (que lo será al inicio de la aplicación) pasa a ser True, y viceversa. De esta forma podemos alternar entre parado y movimiento con una sola tecla. El otro evento que nos interesa es que se pulse en el teclado la tecla enter/return (K_RETURN) que cambiará el estado de la aplicación a la pantalla de fin que nos mostrará las estadísticas de la carrera-
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.car_mov = not self.car_mov
                logger.info(f'Estado de movimiento del coche cambiado a: {self.car_mov}')
            elif event.key == pygame.K_RETURN:
                self.gameStateManager.set_state('pantalla_fin')
                logger.info('Cambio de estado a pantalla_fin')

    def run(self):
        '''
        El método run lleva a cabo todo el desarrollo de esta clase. En primer lugar genera un csv si no existe con la función vista previamente.
        Posteriormente genera la pantalla base y, una vez nos aseguramos de que el valor de tiempo se ha guardado correctamente, especificamos el movimiento del coche.
        Si la flag car_move es True, el coche se moverá 5 píxeles en la pantalla 60 veces por segundo (como vimos al especificar en clock que corre a 60 fps).
        Si el coche supera el ancho total de la pantalla, en nestro caso 1600, volverá al inicio de la pantalla (valor x 0) dando la sensación de que da la vuelta a la pantalla.
        Por cada segundo queremos que se aumente la tarifa con los valores que hemos especificado previamente. Dado que la aplicación actualiza su estado 60 veces por segundo, debemos dividir el valor de la tarifa por 60, para que se aumente correctamente cada segundo.
        Despúes se calcula el tiempo que ha transcurrido la aplicación, restando el tiempo actual al tiempo que se guardó al iniciar la aplicación.
        Esta resta da un valor int, por lo que para poder adaptarlo a minutos y segundos se utiliza la división entera (//) para los minutos y el resto (%) para los segundos.
        A continuación se especifica el formato de texto que queremos tener para visualizar el tiempo y el dinero.
        Finalmente se posiciona en la pantalla donde queremos que se muestre el tiempo trascurrido, el precio, y las tarifas.
        '''
        self.create_csv_if_not_exists('Carreras.csv')

        run_screen = pygame.image.load('Graficos/base_2.jpeg')
        self.display.blit(run_screen, (0, 0))
        color_font = (200, 245, 10, 1)

        if self.start_time is not None:  # Aseguramos que start_time tenga un valor antes de usarlo
            if self.car_mov:
                self.car_position += 5  # Ajusta la velocidad del coche según sea necesario
                if self.car_position > 1600:  # 1600 es el ancho de la pantalla
                    self.car_position = -self.car.get_width()  # Aparecer en el otro lado
                self.score += self.tarifa_mov / 60  # Incrementar el precio por segundo en movimiento
            else:
                self.score += self.tarifa_par / 60  # Incrementar el precio por segundo en parado

            self.display.blit(self.car, (self.car_position, 600))

            # Calcular el tiempo transcurrido en minutos y segundos
            elapsed_time_s = time.time() - self.start_time
            elapsed_minutes = int(elapsed_time_s // 60)
            elapsed_seconds = int(elapsed_time_s % 60)
            clock_text = self.font.render(f'Tiempo: {elapsed_minutes:02}:{elapsed_seconds:02}', True, (color_font))
            self.display.blit(clock_text, (50, 50))

            # Mostrar la puntuación
            score_text = self.font.render(f'Precio: {round(self.score, 2)} €', True, (color_font))
            self.display.blit(score_text, (50, 100))

            tarifa_mov_text = self.font.render(f'Tarifa en movimiento: {round(self.tarifa_mov, 2)}', True, (color_font))
            self.display.blit(tarifa_mov_text, (50, 150))
            tarifa_stp_text = self.font.render(f'Tarifa en parado: {round(self.tarifa_par, 2)}', True, (color_font))
            self.display.blit(tarifa_stp_text, (50, 200))

    def reset(self):
        '''
        La función reset nos servirá para volver a poner los valores que usamos para calcular precio, tiempo, posición y movimiento del coche a sus valores por defecto, para que si se lanza una nueva carrera se vuelva a empezar todo desde 0.
        '''
        self.start_time = time.time()
        self.score = 0
        self.car_position = 20
        self.car_mov = False
        logger.info('Valores de Taximetro reseteados')

    def get_score(self):
        #Función para extraer el precio final de la carrera
        return self.score
    
    def get_total_time(self):
        # Función para extraer la duración total de la carrera
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

class gameStateManager:
    '''
    La clase gameStateManager es la que nos permite cambiar de estados en la aplicación, y de esta forma llamar a las diferentes clases que hemos ido definiendo, de esta forma simulamos el ir pasando de pantallas como en una aplicación cualquiera.
    '''
    def __init__(self, currentState):
        self.currentState = currentState
        self.states = None  # Inicializamos states como None

    def set_states(self, states):
        self.states = states  # Método para establecer los estados

    def get_states(self):
        return self.states  # Método para obtener los estados

    def get_state(self):
        return self.currentState # Método para obtener el estado actual

    def set_state(self, state):
        logger.info(f'Cambio de estado de {self.currentState} a {state}')
        self.currentState = state # Metodo para definir un estado

class pantalla_fin:
    '''
    La clase de pantalla fin es la que nos dará las estadísticas finales de la carrera que se acabe de completar. Las variables de __init__ en su mayoría ya son conocidas.
    Final_price y total_time se fijan a 0 para poder modificarlas fuera de esta clase accediendo a su atributo.
    csv_update empieza en False para poder modificar el csv de carrera una sola vez, como veremos a continuación.
    time_stopped nos sirve para resetear los valores de tiempo al inicar una nueva carrera
    '''

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
        '''
        En este caso nos interesa gestionar los eventos de pulsar un botón del ratón cuando su posición se encuentra dentro de la posición del rectángulo que define empezar una nueva carrera o salir de la aplicación.
        Si se selecciona el boton de nueva carrera se resetean los valores de taximetro (precio, tiempo, etc.) y se cambia el estado a la pantalla de introducción.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            a, b = pygame.mouse.get_pos()
            if self.quit_button_rect.collidepoint((a, b)):
                self.gameStateManager.set_state('quit')
                logger.info('Fin del juego seleccionado')
            elif self.newrun_button_rect.collidepoint((a, b)):
                self.gameStateManager.get_states()['taximetro'].reset()
                self.gameStateManager.set_state('intro')
                self.reset() # Reset de los valores en la pantalla de fin
                logger.info('Reinicio del juego seleccionado')

    def precio_final(self):
        '''
        En este caso se definen los botones de quit y nueva carrera de la misma forma que vimos en la pantalla de inicio.
        Además se incluye una salida de texto para mostrar los valores de precio total y de tiempo total de la carrera.
        El formato de todas estos cálculos y definiciones es el mismo que los que hemos visto previamente por lo que no se volverán a comentar.
        '''
        a, b = pygame.mouse.get_pos()
        login_screen = pygame.image.load('Graficos/fin.jpeg')
        font = pygame.font.SysFont('Lucida Console', 70)
        color_font = (200, 245, 10, 1)
        color_rect_hover = (91, 23, 202, 0.8)
        color_rect_base = (65, 0, 168, 0.9)
        # Botón Start
        self.newrun_button_rect = pygame.Rect(400, 400, 850, 80)
        login_text = font.render('Empezar otra carrera', True, color_font)
        # Botón Quit
        self.quit_button_rect = pygame.Rect(725, 650, 180, 80)
        quit_text = font.render('Quit', True, color_font)
        self.display.blit(login_screen, (0, 0))
        if self.quit_button_rect.collidepoint((a, b)):
            pygame.draw.rect(self.display, color_rect_hover, self.quit_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, self.quit_button_rect)

        if self.newrun_button_rect.collidepoint((a, b)):
            pygame.draw.rect(self.display, color_rect_hover, self.newrun_button_rect)
        else:
            pygame.draw.rect(self.display, color_rect_base, self.newrun_button_rect)   

        self.display.blit(login_text, (self.newrun_button_rect.x + 5, self.newrun_button_rect.y + 5))
        self.display.blit(quit_text, (self.quit_button_rect.x + 5, self.quit_button_rect.y + 5))
        price_text = self.font.render(f'Precio final: {round(self.final_price, 2)}€', True, self.color_font)
        minutos = int(self.total_time // 60)
        segundos = int(self.total_time % 60)
        time_text = self.font.render(f'Tiempo total de carrera: {minutos}m:{segundos}s', True, self.color_font)
        price_text_rect = price_text.get_rect(center=(800, 250))
        time_text_rect = time_text.get_rect(center=(800, 350))
        self.display.blit(price_text, price_text_rect)
        self.display.blit(time_text, time_text_rect)

    def run(self):
        ''' 
        La función de run tomará los valores de precio y tiempo total para poder mostrarlos en pantalla.
        Después registra el día actual con la hora a la que ha acabado la carrera y la guarda en el formato común en españa de día/mes/año hora:minuto:segundo.
        Por último se comprueba si el csv se ha actualizado, por defecto este flag se inicia en False. Se guardan todos los datos de la carrera y, para evitar que se sigan generando registros de la misma carrera se cambia el flag a True, de esta forma nos aseguramos que solo se ejecuta una vez en el bucle de juego (si no se nos generarían 60 nuevos registros cada segundo).
        '''
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
            datos_usuarios = pd.concat([datos_usuarios, df], ignore_index=True)
            datos_usuarios.to_csv('Carreras.csv', index=False)

            logger.info(f'Registro de carrera añadido para el usuario {self.user} con precio {self.final_price} y tiempo {self.total_time} segundos')
            self.csv_updated = True  # Marca el CSV como actualizado

    def reset(self):
        self.final_price = 0
        self.total_time = 0
        self.time_stopped = False
        self.csv_updated = False
        logger.info('Valores de pantalla_fin reseteados')

class Quit:
    '''
    Finalmente la clase quit gestiona el evento de salida del juego, de tal forma que no de errores. Para ello utilza la función quit de pygame y aparte la función exit de sys.
    '''
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def handle_events(self, event):
        # En esta clase solo manejamos el evento de pygame.QUIT
        if event.type == pygame.QUIT:
            self.gameStateManager.set_state('quit')
            logger.info('Evento de salida de pygame detectado')

    def handle_quit(self):
        self.gameStateManager.set_state('quit')
        logger.info('Juego terminado')

    def run(self):
        pygame.quit()
        exit()

def init_game(user):
    # Se define la función para empezar el juego, que se utiliza en el script main
    game = Game(user)
    game.run()
