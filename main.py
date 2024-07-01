import tkinter as tk
from tkinter import messagebox
from funciones_aux import login, registro, pregunta, respuesta, descuentos, descuentos_taxi, login_empresa, tarifa
from car import init_game
from logger_config import logger
from dashboard import Dashboard

class GUI:
    '''
    Clase que inicia la interfaz gráfica, en el constructor __init__ se va a especificar aquellas variables que vamos a querer que sean estables cuando se ejecuten los diferentes métodos de la clase.
    '''
    def __init__(self):
        self.root = tk.Tk() # Inicia la pantalla de tkinter
        self.root.title("Taxea") # Fija el nombre que aparece en la ventana 
        self.root.geometry('800x600') # Fija el tamaño por defecto de la pantalla al abrir la aplicación. En píxeles.
        self.morado = '#541388'
        self.verde = '#C8F50A'
        self.root.configure(bg=self.morado) # Establece el color del fondo para toda la ejecución de tkinter (hexadecimal, es morado)
        self.title_font = ('Lucida Console', 20)
        self.label_font = ('Lucida Console', 16)
        self.empresa = None # Se fija la variable de empresa que la vamos a necesitar en metodos posteriores

        self.style_button = {'font': ('Lucida Console', 16), 'bg': '#C8F50A', 'fg': '#541388', 'padx': 20, 'pady': 10, 'bd': 0}
        # Se define el estilo que van a tener todos los botones que van a utilizarse en la interfaz gráfica.

        self.p_inicio() # Se ejecuta la pantalla de inicio con un metodo definido más adelante.

        logger.info('Aplicación iniciada') # Mensaje que queremos que capture el logger al iniciar

        self.root.mainloop() # mainloop define el bucle de funcionamiento de la interfaz, para que no se cierre la aplicación
    
    def clear_screen(self): # Funcion para eliminar los widgets
        for widget in self.root.winfo_children():
            widget.destroy()

    def p_inicio(self): # Pantalla de inicio
        '''
        La pantalla de inicio, y en general el resto de métodos de pantalla van a tener una estructura general similar.
        En primer lugar la función clear_screen elimina de la pantalla todos los widgets que se hayan generado previamente, de esta forma podemos simular la sensación de que la interfaz tiene varias pantallas sobre las que vamos cambiando. 
        A nivel de funcionamiento lo que estamos haciendo es eliminar todos los widgets previos y generar los nuevos que queremos para la siguiente pantalla.

        Los widgets disponibles, entre otros son:
        -tk.Button = Boton interactuable, incluye como texto la cadena en (text), el comando que debe ejecutar (command) y el estilo de los botones (los asteriscos indican que se definió en __init__)
        -tk.Frame = Marco, se utiliza para colocar imagenes en la pantalla, se especifica tamaño y color de fondo (bg)
        -tk.PhotoImage = Se incluye el archivo fotográfico que queremos incluir
        -tk.Label = Sirve para incluir objetos (texto como titulos, o por ejemplo la fotografia creado en photoimage) con el color de fondo que queramo (bg), color de letra que queramos (fg) y la posibilidad de cambiar fuente del texto y tamaño (font).
        -tk.Entry = Genera una pequeña entrada de texto, de una linea de altura, en la que el usuario puede incluir la respuesta que se requiera, y que puede extraerse posteriormente.
        -tk.messagebox.showinfo = Muestra un mensaje externo que aparece como un pop-up en la aplicación.
        Para colocar todos estos widgets se utiliza pack, que coloca el widget a continuación del previo, utiliza padx y pady como argumentos para colocar distanca en el eje "x" y en el eje "y".
        '''

        self.clear_screen()

        # Boton para pasar a la pantalla de inicio de sesion usuaria
        self.inicio = tk.Button(self.root, text="Inicio Sesión Conductor", command=self.login_screen, **self.style_button)
        self.inicio.pack(pady=30)

        # Boton para pasar a la pantalla de inicio de sesion de empresa
        self.inicio_empresa = tk.Button(self.root, text="Inicio Sesión Empresa", command=self.login_empresa_screen, **self.style_button)
        self.inicio_empresa.pack(pady=30)

        # Boton para registar usuarios
        self.reg = tk.Button(self.root, text="Registrarse", command=self.reg_screen, **self.style_button)
        self.reg.pack(pady=30)

        # Boton para mostrar la ayuda
        self.ayuda = tk.Button(self.root, text="Ayuda", command=self.pantalla_ayuda, **self.style_button)
        self.ayuda.pack(pady=30)

        # Boton para generar el logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()


    def login_screen(self): # Pantalla de inicio de sesion de usuarios
        self.clear_screen()
        
        # Titulo que indica que la pantalla es de inicio de sesión
        self.label_inicio = tk.Label(self.root, text="Inicie Sesión", font=self.title_font, bg=self.morado, fg='white')
        self.label_inicio.pack(pady=20)
        
        # Titulo que indica que la siguiente entrada de texto es para el nombre de Usuario
        self.label_user = tk.Label(self.root, text="Usuario:", font=self.label_font, bg=self.morado, fg='white')
        self.label_user.pack(pady=5)
        # Entrada de usuario para el nombre de Usuario
        self.user = tk.Entry(self.root, font=self.label_font)
        self.user.pack(pady=5)
        
        # Título que indica que la siguiente entrada texto es para la contraseña
        self.label_password = tk.Label(self.root, text="Contraseña:", font=self.label_font, bg=self.morado, fg='white')
        self.label_password.pack(pady=5)
        # Entrada de usuario para la contraseña
        self.password = tk.Entry(self.root, font=self.label_font, show='*') #show = * permite que la contraseña sea secreta, sustituyendo las letras por asteriscos
        self.password.pack(pady=5)
        
         # Boton de inicio de sesión, lleva al método check_password
        self.button_login = tk.Button(self.root, text="Iniciar Sesión", command=self.check_password, **self.style_button)
        self.button_login.pack(pady=10)
        
        # Boton de recuperar contraseña, lleva al método res_pswd
        self.button_forgot = tk.Button(self.root, text="Olvidé mi contraseña", command=self.res_pswd, **self.style_button)
        self.button_forgot.pack(pady=10)

        # Boton de atrás para volver a la pantalla de inicio
        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

        #Logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()

    def check_password(self):
        '''
        Este método llama a una función auxiliar login, explicada en el script de funciones_aux. Esta función devolverá, si todo ha ido bien, si la licencia del usuario es VTC o Taxista, en cuyo caso llevará a la pantalla correspondiente para definir los datos que faltan antes de lanzar el programa, se pasa como argumento el nombre del usuario. Si hay algún problema (contraseña o usuario equivocado, usuario inexistente, etc.) la función devuelve un False, de tal forma que en este punto se mostrara un error al usuario en forma de pop-up indicando que ha cometido algún error al escribir su usuario o contraseña.
        El nombre de usuario y la contrseña se extraen de la pantalla previa a esta (login_screen) con el método .get.
        '''
        tarifa = login(self.user.get(), self.password.get())
        user = self.user.get()
        if not tarifa:
            messagebox.showinfo(title = "Error", message = "Nombre de usuario o contraseña equivocados")
            logger.error(f'¡Intento fallido: Nombre de usuario o contraseña incorrecto!') # Control de log
        else:
            if tarifa == 'VTC':
                self.discount_screen(user)
            elif tarifa == 'Taxista':
                self.turno_screen(user)

        logger.info('!Verificación de acceso al sistema exitosa!') # Control de Log

    def discount_screen(self, user): # Pantalla para aplicar descuentos en conductores de VTC
        self.clear_screen()
        self.user = user
        # Titulo de la pantalla
        self.label_disc = tk.Label(self.root, text="Descuentos", font=self.title_font, bg=self.morado, fg='white')
        self.label_disc.pack(pady=20)
        
        # Titulo que indica que la siguiente entrada de texto es para fijar el porcentaje de descuento en parado
        self.label_prcnt_stp = tk.Label(self.root, text="Porcentaje de descuento parado", font=self.label_font, bg=self.morado, fg='white')
        self.label_prcnt_stp.pack(pady=10)
        
        # Entrada de texto para porcentaje de descuento en parado
        self.discount_stopped = tk.Entry(self.root, font=self.label_font)
        self.discount_stopped.pack(pady=10)
        
        # Titulo que indica que la siguiente entrada de texto es para fijar el porcentaje de descuento en movimiento
        self.label_prcnt_mov = tk.Label(self.root, text="Porcentaje de descuento movimiento", font=self.label_font, bg=self.morado, fg='white')
        self.label_prcnt_mov.pack(pady=10)

        # Entrada de texto para porcentaje de descuento en movimiento
        self.discount_moving = tk.Entry(self.root, font=self.label_font)
        self.discount_moving.pack(pady=10)
        
        # Boton para guardar cambios, incluye como command una función lambda para poder pasar en el método save_discounts el usuario como argumento.
        self.submit = tk.Button(self.root, text="Guardar", command=lambda: self.save_discounts(self.user), **self.style_button)
        self.submit.pack(pady=20)

        # Logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()
    
        logger.info('Pantalla de Descuento') # Control de Log
    
    def save_discounts(self, user):  #Método para guardar los descuentos para VTC
        self.user = user.lower()
        stopped_discount = self.discount_stopped.get()
        moving_discount = self.discount_moving.get()

        # Si los valores de los descuentos no son válidos o están vacios, se fijan en 0
        stopped_discount = stopped_discount if stopped_discount else 0 
        moving_discount = moving_discount if moving_discount else 0

        '''
        Este método llama a una función auxiliar descuentos, explicada en el script de funciones_aux. Si recupera el valor True porque se han podido aplicar los descuentos se muestra un mensaje de éxito en pop-up y se inicia la aplicación en pygame.
        '''
        if descuentos(self.user, stopped_discount, moving_discount):
            messagebox.showinfo(title = "Exito", message = "Descuentos aplicados")
            logger.info('Pantalla de Descuentos aplicados') # Control de Log
            init_game(self.user)

    def turno_screen(self, user): # Pantalla para definir turno y valor extra de la tarifa nocturna para taxistas
        self.clear_screen()
        self.user = user
        
        # Titulo de la pantalla
        self.label_tarifa = tk.Label(self.root, text="Tarifas", font=self.title_font, bg=self.morado, fg='white')
        self.label_tarifa.pack(pady=20)
        
        # Titulo que indica que el siguiente menu de opciones es para definir el turno
        self.label_turno = tk.Label(self.root, text="Turno", font=self.label_font, bg=self.morado, fg='white')
        self.label_turno.pack(pady=10)

        # Lista de turnos para el menu
        turnos_opt = ["Diurno", "Nocturno"]
        self.turno = tk.StringVar()
        self.turno.set("")

        # Menu droprdown de turnos
        self.dropdown_turno = tk.OptionMenu(self.root, self.turno, *turnos_opt)
        self.dropdown_turno.config(font=self.label_font, bg=self.verde, fg='#4100A8', width=20)
        self.dropdown_turno.pack(pady=5)
        
        # Titulo que indica que la siguiente entrada de texto es para definir el porcentaje de aumento de tarifa (para turno nocturno)
        self.label_prcnt = tk.Label(self.root, text="Porcentaje de aumento de tarifa (solo para noche)", font=self.label_font, bg=self.morado, fg='white')
        self.label_prcnt.pack(pady=10)
        
        # Entrada de texto para tarifa
        self.tarifa_extra = tk.Entry(self.root, font=self.label_font)
        self.tarifa_extra.pack(pady=10)
        
        # Boton para guardar cambios, como command toma una función lambda  que permite ejecutar el método save_discounts_t con el argumento de usuario
        self.submit = tk.Button(self.root, text="Guardar", command=lambda: self.save_discounts_t(self.user), **self.style_button)
        self.submit.pack(pady=20)

        # Logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()

        logger.info('Pantalla de turno') # Control de Log
    
    def save_discounts_t(self, user): # Método para guardar la tarifa para taxistas
        self.user = user.lower()
        turno = self.turno.get()
        tarifa_extra = self.tarifa_extra.get()

        # Si el valor de la tarifa no son válidos o están vacios, se fijan en 0
        tarifa_extra = tarifa_extra if tarifa_extra else 0

        if descuentos_taxi(self.user, turno, tarifa_extra):
            '''
            Este método llama a una función auxiliar descuentos_taxi, explicada en el script de funciones_aux. Si recupera el valor True porque se han podido aplicar los descuentos se muestra un mensaje de éxito en pop-up y se inicia la aplicación en pygame.
            '''
            messagebox.showinfo(title = "Exito", message = "Descuentos aplicados")
            logger.info('Descuentos aplicados con exito') # Control de Log
            init_game(self.user)

    def res_pswd(self): # Pantalla para reiniciar la contraseña en clase de olvido
        self.clear_screen()
        
        self.label_reset = tk.Label(self.root, text="Reiniciar contraseña", font=self.title_font, bg=self.morado, fg='white')
        self.label_reset.pack(pady=20)

        # Titulo que indica que la siguiente entrada de texto es para el nombre de usuario
        self.label_user = tk.Label(self.root, text="Nombre de usuario", font=self.label_font, bg=self.morado, fg='white')
        self.label_user.pack(pady = 5)

        # Entrada de texto para el Usuario
        self.user = tk.Entry(self.root, font=self.label_font)
        self.user.pack(pady=10)

        # Botón para mostrar la pregunta secreta, será buscada con el método get_quest, spoiler, la muestra en un pop-up.
        self.quest_get = tk.Button(self.root, text="Ver pregunta secreta", command=self.get_quest, **self.style_button)
        self.quest_get.pack(pady=10)
        
        # Titulo que indica que la siguiente entrada de texto es para la respuesta secreta
        self.label_answ = tk.Label(self.root, text="Escriba su respuesta secreta", font=self.label_font, bg=self.morado, fg='white')
        self.label_answ.pack(pady=10)
        
        # Entrada de texto para la respuesta secreta
        self.user_answer = tk.Entry(self.root, font=self.label_font)
        self.user_answer.pack(pady=10)
        
        # Titulo que indica que la siguiente entrada de texto es para la nueva contraseña
        self.label_new_pswd = tk.Label(self.root, text="Nueva contraseña", font=self.label_font, bg=self.morado, fg='white')
        self.label_new_pswd.pack(pady=10)
        
        # Entrada de texto para la nueva contraseña
        self.new_pswd = tk.Entry(self.root, font=self.label_font, show='*')
        self.new_pswd.pack(pady=10)
        
        # Boton para confirmar los datos introducidos y cambiar la contraseña
        self.submit_button = tk.Button(self.root, text="Enviar", command=self.change_pswd, **self.style_button)
        self.submit_button.pack(pady=20)
        
        # Boton para volver a la pantalla de inicio de sesión
        self.button_back = tk.Button(self.root, text="Atrás", command=self.login_screen, **self.style_button)
        self.button_back.pack(pady=10)

        logger.info('Pantalla de inicio de sesión mostrada') # Control de Log

    def get_quest(self):
        '''
        Este método llama a una función auxiliar pregunta, explicada en el script de funciones_aux. Únicamente devuelve la cadena almacenada de la pregunta secreta y la muestra al usuario mediante un pop-up.
        '''
        pregunta(self.user.get())

    def change_pswd(self):
        '''
        Este método llama a una función auxiliar respuesta, explicada en el script de funciones_aux. Si se ha introducido la respuesta secreta de forma correcta permite cambiar la contrasela.
        '''
        respuesta(self.user.get(), self.user_answer.get(), self.new_pswd.get())

    def login_empresa_screen(self): # Pantalla de Login para representante de Empresa. La estructura es similar a login_screen
        self.clear_screen()

        # Titulo de inicio de sesion
        self.label_inicio = tk.Label(self.root, text="Inicie Sesión", font=self.title_font, bg=self.morado, fg='white')
        self.label_inicio.pack(pady=20)
        
        # Titulo que indica que la siguiente entrada de texto es para el nombre de Usuario
        self.label_user = tk.Label(self.root, text="Usuario:", font=self.label_font, bg=self.morado, fg='white')
        self.label_user.pack(pady=5)
        # Entrada de Usuario
        self.user = tk.Entry(self.root, font=self.label_font)
        self.user.pack(pady=5)
        
        # Titulo que indica que la siguiente entrada de texto es para la contraseña
        self.label_password = tk.Label(self.root, text="Contraseña:", font=self.label_font, bg=self.morado, fg='white')
        self.label_password.pack(pady=5)
        # Entrada de contraseña
        self.password = tk.Entry(self.root, font=self.label_font, show='*')
        self.password.pack(pady=5)
        
        # Boton que lleva al método check_password_empresa
        self.button_login = tk.Button(self.root, text="Iniciar Sesión", command=self.check_password_empresa, **self.style_button)
        self.button_login.pack(pady=10)
        
        # Boton que llevaría a la pantalla de cambio de contraseña, pero que en este caso muestra un error de que el cambio de contraseña lo gestiona IT.
        self.button_forgot = tk.Button(self.root, text="Olvidé mi contraseña", command= lambda: tk.messagebox.showinfo(title="Error", message="Debe ponerse en contacto con su responsable de IT."), **self.style_button)
        self.button_forgot.pack(pady=10)

        # Boton para volver a la pantalla de inicio
        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

        #Logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()

    def check_password_empresa(self):
        '''
        Este método llama a una función auxiliar login_empresa, explicada en el script de funciones_aux. Esta función devolverá, si todo ha ido bien, el nombre de la empresa a la que pertenece el representante, llevando al usuario a la pantalla de empresa, donde podrá decidir cambiar la tarifa para los conductores de su empresa, o ver el dashboard con información relevante para su empresa. Si hay algún problema (contraseña o usuario equivocado, usuario inexistente, etc.) la función devuelve un False, de tal forma que en este punto se mostrara un error al usuario en forma de pop-up indicando que ha cometido algún error al escribir su usuario o contraseña.
        El nombre de usuario y la contrseña se extraen de la pantalla previa a esta (login_empresa_screen) con el método .get.
        '''
        empresa = login_empresa(self.user.get(), self.password.get())
        if not empresa:
            messagebox.showinfo(title = "Error", message = "Nombre de usuario o contraseña equivocados")
            logger.error(f'¡Intento fallido: Nombre de usuario o contraseña incorrecto!') # Control de log
        else:
            self.empresa = empresa
            self.pantalla_empresa()
            logger.info('!Verificación de acceso al sistema exitosa!')
    
    def pantalla_empresa(self): # Pantalla de opciones una vez se ha iniciado sesión como representante de empresa
        self.clear_screen()

        # Boton para acceder a la pantalla de cambio de tarifas
        self.tarifa = tk.Button(self.root, text="Cambiar tarifa", command=self.pantalla_tarifa, **self.style_button)
        self.tarifa.pack(pady=20)

        # Boton para acceder al dashboard
        self.dash = tk.Button(self.root, text="Acceder al dashboard", command=self.dashboard, **self.style_button)
        self.dash.pack(pady=20)
        logger.info('Pantalla de Empresa')

        # Boton de atrás
        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

        # Logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()

    def pantalla_tarifa(self): # Pantalla para cambiar tarifas de una empresa
        self.clear_screen()

        # Titulo que indica que la siguiente entrada de texto es para la tarifa en movimiento
        self.tarifa_mov = tk.Label(self.root, text="Cambio tarifa movimiento (p.ej. 0.06€/s)", font=self.label_font, bg=self.morado, fg='white')
        self.tarifa_mov.pack(pady= 20)

        # Entrada de texto para la tarifa en movimiento
        self.tarifa_mov_change = tk.Entry(self.root, font=self.label_font)
        self.tarifa_mov_change.pack(pady = 10)

        # Titulo que indica que la siguiente entrada de texto es para la tarifa en parado
        self.tarifa_stop = tk.Label(self.root, text="Cambio tarifa parado (p.ej. 0.03€/s)", font=self.label_font, bg=self.morado, fg='white')
        self.tarifa_stop.pack(pady= 20)

        # Entrada de texto para la tarifa en parado
        self.tarifa_stop_change = tk.Entry(self.root, font=self.label_font)
        self.tarifa_stop_change.pack(pady = 10)

        # Boton para confirmar cambios, llama a la función set_tarifas
        self.submit_button = tk.Button(self.root, text="Enviar", command=self.set_tarifas, **self.style_button)
        self.submit_button.pack(pady=20)
        logger.info('Pantalla de cambio de tarifas mostrada')

        # Boton para volver a la pantalla de empresa
        self.button_back = tk.Button(self.root, text="Atrás", command=self.pantalla_empresa, **self.style_button)
        self.button_back.pack(pady=10)

        # Logo
        self.marco = tk.Frame(self.root, width=150, height=150, bg = self.morado)
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = self.morado)
        self.label.pack()

    def set_tarifas(self): # Método para definir las tarifas de empresa
        tarifa_stopped = self.tarifa_stop_change.get()
        tarifa_mov = self.tarifa_mov_change.get()
        
        # Si no se recupera un valor con .get, se establece en sus valores estándar 0.05 y 0.02. Si hay un valor, se establece ese valor.
        tarifa_stopped = tarifa_stopped if tarifa_stopped else 0.02 
        tarifa_mov = tarifa_mov if tarifa_mov else 0.05
        logger.info(f'Tarifa en parado fijada en {tarifa_stopped}')
        logger.info(f'Tarifa en movimiento fijada en {tarifa_mov}')

        '''
        Este método llama a una función auxiliar tarifa, explicada en el script de funciones_aux. Si recupera el valor True porque se han podido aplicar las tarifas se muestra un mensaje de éxito en pop-up y se vuelve a la pantalla de inicio.
        '''
        if tarifa(self.empresa, tarifa_mov, tarifa_stopped):
            messagebox.showinfo(title = "Exito", message = "Tarifas aplicadas")
            logger.info('Pantalla de tarifas aplicados') # Control de Log
            self.p_inicio()

    def dashboard(self): # Metodo intermedio para instanciar la clase importada Dashboard del script 'dashboard.py' e iniciar el servidor que mostrará el dashboard.
        dashboard = Dashboard()
        dashboard.init_server()

    def reg_screen(self): # Pantalla de registro de usuario
        self.clear_screen()
        
        # Titulo de la pantalla de Registro
        self.label_reg = tk.Label(self.root, text='Registro', font=self.title_font, bg=self.morado, fg='white')
        self.label_reg.pack(pady=10)
        
        # Titulo que indica que la siguiente entrada de texto es para el nombre de Usuario
        self.label_user = tk.Label(self.root, text="Usuario:", font=self.label_font, bg=self.morado, fg='white')
        self.label_user.pack(pady = 5)
        # Entrada de Usuario
        self.user = tk.Entry(self.root, font=self.label_font)
        self.user.pack(pady=5)

        # Titulo que indica que la siguiente entrada de texto es para la contraseña
        self.label_password = tk.Label(self.root, text="Contraseña", font=self.label_font, bg=self.morado, fg='white')
        self.label_password.pack(pady = 5)
        #Entrada de contraseña
        self.password = tk.Entry(self.root, font=self.label_font, show='*')
        self.password.pack(pady=5)
        
        # Titulo que indica que la siguiente entrada de texto es para la pregunta secreta
        self.label_quest = tk.Label(self.root, text="Defina una pregunta secreta para cambiar la contraseña en caso de olvido", font=('Lucida Console', 12), bg=self.morado, fg='white')
        self.label_quest.pack(pady = 5)
        # Entrada para la pregunta secreta
        self.quest = tk.Entry(self.root, font=self.label_font)
        self.quest.pack(pady=5)
        
        # Titulo que indica que la siguiente entrada de texto es para la respuesta secreta
        self.label_answ = tk.Label(self.root, text="Defina una respuesta para su pregunta secreta", font=self.label_font, bg=self.morado, fg='white')
        self.label_answ.pack(pady = 5)
        # Entrada para la respuesta secreta
        self.answ = tk.Entry(self.root, font=self.label_font)
        self.answ.pack(pady=5)
        
        # Titulo que indica que el siguiente menu desplegable es para seleccionar el tipo de conductor
        self.label_drop_conductor = tk.Label(self.root, text="Seleccione tipo de conductor:", font=self.label_font, bg=self.morado, fg='white')
        self.label_drop_conductor.pack(pady=5)

        # Lista para el menú desplegable de licencias
        conductores = ["Taxista", "VTC"]
        self.selected_conductor = tk.StringVar()
        self.selected_conductor.set("")

        # Menu desplegable para tipo de licencia
        self.dropdown_cond = tk.OptionMenu(self.root, self.selected_conductor, *conductores) # El segundo argumento define donde se almacena la elección y el tercero la lista de opciones.
        self.dropdown_cond.config(font=self.label_font, bg=self.verde, fg='#4100A8', width=20)
        self.dropdown_cond.pack(pady=5)
        
        # Titulo que indica que el siguiente menu desplegable es para seleccionar la empresa
        self.label_dropdown_emp = tk.Label(self.root, text="Seleccione empresa:", font=self.label_font, bg=self.morado, fg='white')
        self.label_dropdown_emp.pack(pady=5)

        #Lista para el menu desplegable de empresas
        empresas = ["Uber", "Cabify", "Bolt", "Confederacion Taxi"]

        self.empresa_sel = tk.StringVar()
        self.empresa_sel.set("")

        #Menu desplehable para empresa
        self.dropdown_emp = tk.OptionMenu(self.root, self.empresa_sel, *empresas)
        self.dropdown_emp.config(font=self.label_font, bg=self.verde, fg='#4100A8', width=20)
        self.dropdown_emp.pack(pady=5)

        # Logo
        button_frame = tk.Frame(self.root, bg='#791E94')
    
        self.button_register = tk.Button(button_frame, text="Registro", command=self.register, **self.style_button)
        self.button_register.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.button_back = tk.Button(button_frame, text="Incio de Sesion", command=self.login_screen, **self.style_button)
        self.button_back.pack(side=tk.LEFT, padx=10, pady=10)

        button_frame.pack(pady=20)

        logger.info('Pantalla de Registro de Usuarios') # Control de Log

    def register(self):
        '''
        Este método llama a una función auxiliar registro, explicada en el script de funciones_aux. Esta función devolverá, si todo ha ido bien un valor True, en cuyo caso permite al usuario ir a la pantalla de login de usuarios para poder emepzar a usar la aplicación.
        Las variables se extraen de la pantalla previa (reg_screen) con el método .get.
        '''
        if registro(self.user.get(), self.password.get(), self.quest.get(), self.answ.get(), self.selected_conductor.get(), self.empresa_sel.get()) == True:
            self.login_screen()

    def pantalla_ayuda(self): # Pantala de ayuda
        self.clear_screen()

        texto = """
### Como arrancar el programa
Descargar el archivo '.zip' pulsando en "CODE" y seleccionando la opción. Extraer el contenido de las carpetas y mantener la misma estructura. La aplicación se inicia ejecutando el script 'main.py', desde VSCode o desde la terminal.

IMPORTANTE. Comprobar que la carpeta de trabajo es aquella en la que están todos los archivos del '.zip'. Puede abrirse desde vcode de forma manual, aunque está contemplado que el script la establezca correctamente de forma automática.

Antes de ejecutar el código se necesita instalar las bibliotecas:
- tkinter
- pygame
- pygame_gui
- dash
- matplotlib
- seaborn

El codigo incluye un archivo txt que puede ejecutarse con pip para instalar todos los paquetes necesarios en una sola linea, abrir la carpeta de trabajo en la terminal y escribir 'pip install -r "ruta/del/arhcivo/requirements.txt"
Si se utiliza Anaconda o Miniconda para python puede instalarse pip en el entorno virtual y despues ejecutar el código previo. No obstante conda no recomienda este método, revisar documentación que se ajuste a cada caso de uso.

Ejecutar el script 'main.py' para comenzar a utilizar la aplicación y seguir los pasos necesarios. Registrarse si es la primera vez y seleccionar tipo de conductor y empresa de pertenencia.

Cuando el inicio de sesión es correcto y no presenta errores se podrán definir los descuentos que se quieran aplicar en el caso de licencias 'VTC' y seleccionar el turno de trabajo en el caso de Taxistas. La tarifa extra solo se aplica durante el horario nocturno.

En el caso de empresas se puede modificar la tarifa base utilizando el menu de inicio de sesión para empresas con:
- Usuario: jefe
- Contraseña: 1234
Esto cambiará las tarifas para los conductores VTC de la empresa Uber.
Se pueden incluir otros casos de uso modificando el archivo 'Empresa.csv', pero la contraseña debe incluirse en un formato sha-256.
"""
        texto_widget = tk.Text(self.root, wrap=tk.WORD, bg="#541388", fg="#C8F50A", font=("Lucida Console", 16)) # wrap para que cierre linea con palabras completas
        texto_widget.pack(padx=20, pady=40)

        # Insertar el texto
        texto_widget.insert(tk.END, texto)

        # Deshabilitar la edición del texto
        texto_widget.configure(state='disabled')

        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

# Inicio del script
if __name__ == "__main__":
    GUI()
