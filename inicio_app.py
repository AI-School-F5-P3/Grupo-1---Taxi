import tkinter as tk
from tkinter import messagebox
from funciones_aux import LogIn, Register, Pregunta, Respuesta, Descuentos, Descuentos_taxi, LogIn_Empresa, Tarifa
from car import init_game
from logger_config import logger
from dashboard import Dashboard

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Taxea")
        self.root.geometry('800x600')
        self.root.configure(bg='#541388')

        self.empresa = None

        self.style_button = {'font': ('Lucida Console', 16), 'bg': '#C8F50A', 'fg': '#541388', 'padx': 20, 'pady': 10, 'bd': 0}

        self.p_inicio()

        logger.info('Aplicación iniciada') # Control de Log

        self.root.mainloop()

    def p_inicio(self):

        self.clear_screen()

        self.inicio = tk.Button(self.root, text="Inicio Sesión Conductor", command=self.login_screen, **self.style_button)
        self.inicio.pack(pady=30)

        self.inicio_empresa = tk.Button(self.root, text="Inicio Sesión Empresa", command=self.login_empresa_screen, **self.style_button)
        self.inicio_empresa.pack(pady=30)
        
        self.reg = tk.Button(self.root, text="Registrarse", command=self.reg_screen, **self.style_button)
        self.reg.pack(pady=30)

        self.reg = tk.Button(self.root, text="Ayuda", command=self.pantalla_ayuda, **self.style_button)
        self.reg.pack(pady=30)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()


    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()
        
        self.label_inicio = tk.Label(self.root, text="Inicie Sesión", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label_inicio.pack(pady=20)
        
         # Título y Entry para el usuario
        self.label_user = tk.Label(self.root, text="Usuario:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_user.pack(pady=5)
        self.user = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user.pack(pady=5)
        
        # Título y Entry para la contraseña
        self.label_password = tk.Label(self.root, text="Contraseña:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_password.pack(pady=5)
        self.password = tk.Entry(self.root, font=('Lucida Console', 16), show='*')
        self.password.pack(pady=5)
        
        self.button_login = tk.Button(self.root, text="Iniciar Sesión", command=self.check_password, **self.style_button)
        self.button_login.pack(pady=10)
        
        self.button_forgot = tk.Button(self.root, text="Olvidé mi contraseña", command=self.res_pswd, **self.style_button)
        self.button_forgot.pack(pady=10)

        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()
    
    def login_empresa_screen(self):
        self.clear_screen()
        self.label_inicio = tk.Label(self.root, text="Inicie Sesión", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label_inicio.pack(pady=20)
        

        self.label_user = tk.Label(self.root, text="Usuario:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_user.pack(pady=5)
        self.user = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user.pack(pady=5)
        
        self.label_password = tk.Label(self.root, text="Contraseña:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_password.pack(pady=5)
        self.password = tk.Entry(self.root, font=('Lucida Console', 16), show='*')
        self.password.pack(pady=5)
        
        self.button_login = tk.Button(self.root, text="Iniciar Sesión", command=self.check_password_empresa, **self.style_button)
        self.button_login.pack(pady=10)
        
        self.button_forgot = tk.Button(self.root, text="Olvidé mi contraseña", command= lambda: tk.messagebox.showinfo(title="Error", message="Debe ponerse en contacto con su responsable de IT."), **self.style_button)
        self.button_forgot.pack(pady=10)

        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()


    def reg_screen(self):
        self.clear_screen()
        
        self.label_reg = tk.Label(self.root, text='Registro', font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label_reg.pack(pady=10)
        
        self.label_user = tk.Label(self.root, text="Usuario:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_user.pack(pady = 5)
        self.user = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user.pack(pady=5)
        
        self.label_password = tk.Label(self.root, text="Contraseña", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_password.pack(pady = 5)
        self.password = tk.Entry(self.root, font=('Lucida Console', 16), show='*')
        self.password.pack(pady=5)
        
        self.label_quest = tk.Label(self.root, text="Defina una pregunta secreta para cambiar la contraseña en caso de olvido", font=('Lucida Console', 12), bg='#541388', fg='white')
        self.label_quest.pack(pady = 5)
        self.quest = tk.Entry(self.root, font=('Lucida Console', 16))
        self.quest.pack(pady=5)
        
        self.label_answ = tk.Label(self.root, text="Defina una respuesta para su pregunta secreta", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_answ.pack(pady = 5)
        self.answ = tk.Entry(self.root, font=('Lucida Console', 16))
        self.answ.pack(pady=5)

        self.label_drop_conductor = tk.Label(self.root, text="Seleccione tipo de conductor:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_drop_conductor.pack(pady=5)

        # Lista vacía para el menú desplegable
        conductores = ["Taxista", "VTC"]
        self.selected_conductor = tk.StringVar()
        self.selected_conductor.set("")

        self.dropdown_cond = tk.OptionMenu(self.root, self.selected_conductor, *conductores)
        self.dropdown_cond.config(font=('Lucida Console', 16), bg='#C8F50A', fg='#4100A8', width=20)
        self.dropdown_cond.pack(pady=5)
        

        # Lista vacía para el menú desplegable
        self.label_dropdown_emp = tk.Label(self.root, text="Seleccione empresa:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_dropdown_emp.pack(pady=5)

        empresas = ["Uber", "Cabify", "Bolt", "Confederacion Taxi"]

        self.empresa_sel = tk.StringVar()
        self.empresa_sel.set("")

        self.dropdown_emp = tk.OptionMenu(self.root, self.empresa_sel, *empresas)
        self.dropdown_emp.config(font=('Lucida Console', 16), bg='#C8F50A', fg='#4100A8', width=20)
        self.dropdown_emp.pack(pady=5)

        
        button_frame = tk.Frame(self.root, bg='#791E94')
    
        self.button_register = tk.Button(button_frame, text="Registro", command=self.register, **self.style_button)
        self.button_register.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.button_back = tk.Button(button_frame, text="Incio de Sesion", command=self.login_screen, **self.style_button)
        self.button_back.pack(side=tk.LEFT, padx=10, pady=10)

        button_frame.pack(pady=20)

        logger.info('Pantalla de Registro de Usuarios') # Control de Log

    def pantalla_ayuda(self):
        self.clear_screen()

        texto = """
Como arrancar el programa

Hay que bajarse del github todos los documentos que hay subidos y mantener la misma estructura que tienen.

Para poder ejecutar el código se necesita instalar las bibliotecas:

    -tkinter
    -pygame
    -pygame_gui

El codigo incluye un archivo txt que puede ejecutarse con pip para instalar todos los paquetes necesarios en una sola linea: 'pip install -r "ruta/del/arhcivo/requirements.txt" Si se utiliza Anaconda o Miniconda para python puede instalarse pip en el entorno virtual y despues ejecutar el código previo. No obstante conda no recomienda este método, revisar documentación que se ajuste a cada caso de uso.

Ejecutar el script 'GUI Entrada.py' para comenzar a utilizar la aplicación y seguir los pasos necesarios. Registrarse si es la primera vez y seleccionar tipo de conductor.

Despues cuando el inicio de sesión es correcto y no presenta errores se podrán definir los descuentos que se quieran aplicar en el caso de licencias 'VTC' y seleccionar el turno en el caso de Taxistas. La tarifa extra solo se aplica durante el horario nocturno pero de momento hay que escribirla hasta que se meta un valor de control ahí para que no salte error.
"""
        texto_widget = tk.Text(self.root, wrap=tk.WORD, bg="#541388", fg="#C8F50A", font=("Lucida Console", 16))
        texto_widget.pack(padx=20, pady=40)

        # Insertar el texto
        texto_widget.insert(tk.END, texto)

        # Deshabilitar la edición del texto (opcional)
        texto_widget.configure(state='disabled')

        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

    def pantalla_empresa(self):
        self.clear_screen()

        self.tarifa = tk.Button(self.root, text="Cambiar tarifa", command=self.pantalla_tarifa, **self.style_button)
        self.tarifa.pack(pady=20)

        self.dash = tk.Button(self.root, text="Acceder al dashboard", command=self.dashboard, **self.style_button)
        self.dash.pack(pady=20)
        logger.info('Pantalla de Empresa')

        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()


    def pantalla_tarifa(self):
        self.clear_screen()

        self.tarifa_mov = tk.Label(self.root, text="Cambio tarifa movimiento (p.ej. 0.06€/s)", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.tarifa_mov.pack(pady= 20)

        self.tarifa_mov_change = tk.Entry(self.root, font=('Lucida Console', 16))
        self.tarifa_mov_change.pack(pady = 10)

        self.tarifa_stop = tk.Label(self.root, text="Cambio tarifa parado (p.ej. 0.03€/s)", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.tarifa_stop.pack(pady= 20)

        self.tarifa_stop_change = tk.Entry(self.root, font=('Lucida Console', 16))
        self.tarifa_stop_change.pack(pady = 10)

        self.submit_button = tk.Button(self.root, text="Enviar", command=self.set_tarifas, **self.style_button)
        self.submit_button.pack(pady=20)
        logger.info('Pantalla de cambio de tarifas mostrada')

        self.button_back = tk.Button(self.root, text="Atrás", command=self.pantalla_empresa, **self.style_button)
        self.button_back.pack(pady=10)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()

    def dashboard(self):
        dashboard = Dashboard()
        dashboard.init_server()

    def res_pswd(self):
        self.clear_screen()
        
        self.label_reset = tk.Label(self.root, text="Reiniciar contraseña", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label_reset.pack(pady=20)

        self.label_user = tk.Label(self.root, text="Nombre de usuario", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_user.pack(pady = 5)
        self.user = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user.pack(pady=10)
        
        self.quest_get = tk.Button(self.root, text="Ver pregunta secreta", command=self.get_quest, **self.style_button)
        self.quest_get.pack(pady=10)
        
        self.label_answ = tk.Label(self.root, text="Escriba su respuesta secreta", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_answ.pack(pady=10)
        
        self.user_answer = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user_answer.pack(pady=10)
        
        self.label_new_pswd = tk.Label(self.root, text="Nueva contraseña", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_new_pswd.pack(pady=10)
        
        self.new_pswd = tk.Entry(self.root, font=('Lucida Console', 16), show='*')
        self.new_pswd.pack(pady=10)
        
        self.submit_button = tk.Button(self.root, text="Enviar", command=self.change_pswd, **self.style_button)
        self.submit_button.pack(pady=20)
        
        self.button_back = tk.Button(self.root, text="Atrás", command=self.login_screen, **self.style_button)
        self.button_back.pack(pady=10)

        logger.info('Pantalla de inicio de sesión mostrada') # Control de Log

    def check_password(self):
        tarifa = LogIn(self.user.get(), self.password.get())
        user = self.user.get()
        if tarifa == False:
            messagebox.showinfo(title = "Error", message = "Nombre de usuario o contraseña equivocados")
            logger.error(f'¡Intento fallido: Nombre de usuario o contraseña incorrecto!') # Control de log
        else:
            if tarifa == 'VTC':
                self.discount_screen(user)
            elif tarifa == 'Taxista':
                self.turno_screen(user)

        logger.info('!Verificación de acceso al sistema exitosa!') # Control de Log
    
    def check_password_empresa(self):
        empresa = LogIn_Empresa(self.user.get(), self.password.get())
        if not empresa:
            messagebox.showinfo(title = "Error", message = "Nombre de usuario o contraseña equivocados")
            logger.error(f'¡Intento fallido: Nombre de usuario o contraseña incorrecto!') # Control de log
        else:
            self.empresa = empresa
            self.pantalla_empresa()
            logger.info('!Verificación de acceso al sistema exitosa!')

    
    def register(self):
        if Register(self.user.get(), self.password.get(), self.quest.get(), self.answ.get(), self.selected_conductor.get(), self.empresa_sel.get()) == True:
            self.login_screen()

    def get_quest(self):
        Pregunta(self.user.get())
    
    def change_pswd(self):
        Respuesta(self.user.get(), self.user_answer.get(), self.new_pswd.get())

    def turno_screen(self, user):
        self.clear_screen()
        self.user = user

        self.label_tarifa = tk.Label(self.root, text="Tarifas", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label_tarifa.pack(pady=20)
        
        self.label_turno = tk.Label(self.root, text="Turno", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_turno.pack(pady=10)

        turnos_opt = ["Diurno", "Nocturno"]
        self.turno = tk.StringVar()
        self.turno.set("")

        self.dropdown_turno = tk.OptionMenu(self.root, self.turno, *turnos_opt)
        self.dropdown_turno.config(font=('Lucida Console', 16), bg='#C8F50A', fg='#4100A8', width=20)
        self.dropdown_turno.pack(pady=5)
        
        self.label_prcnt = tk.Label(self.root, text="Porcentaje de aumento de tarifa (solo para noche)", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_prcnt.pack(pady=10)
        
        self.tarifa_extra = tk.Entry(self.root, font=('Lucida Console', 16))
        self.tarifa_extra.pack(pady=10)
        
        self.submit = tk.Button(self.root, text="Guardar", command=lambda: self.save_discounts_t(self.user), **self.style_button)
        self.submit.pack(pady=20)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()

        logger.info('Pantalla de turno') # Control de Log

    def set_tarifas(self):
        tarifa_stopped = self.tarifa_mov_change.get()
        tarifa_mov = self.tarifa_stop_change.get()

        tarifa_stopped = tarifa_stopped if tarifa_stopped else 0.02
        tarifa_mov = tarifa_mov if tarifa_mov else 0.05
        logger.info(f'Tarifa en parado fijada en {tarifa_stopped}')
        logger.info(f'Tarifa en movimiento fijada en {tarifa_mov}')

        if Tarifa(self.empresa, tarifa_mov, tarifa_stopped):
            messagebox.showinfo(title = "Exito", message = "Tarifas aplicadas")
            logger.info('Pantalla de tarifas aplicados') # Control de Log
            self.p_inicio()



    def discount_screen(self, user):
        self.clear_screen()
        self.user = user

        self.label_disc = tk.Label(self.root, text="Descuentos", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label_disc.pack(pady=20)
        
        self.label_prcnt_stp = tk.Label(self.root, text="Porcentaje de descuento parado", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_prcnt_stp.pack(pady=10)
        
        self.discount_stopped = tk.Entry(self.root, font=('Lucida Console', 16))
        self.discount_stopped.pack(pady=10)
        
        self.label_prcnt_mov = tk.Label(self.root, text="Porcentaje de descuento movimiento", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_prcnt_mov.pack(pady=10)
        
        self.discount_moving = tk.Entry(self.root, font=('Lucida Console', 16))
        self.discount_moving.pack(pady=10)
        
        self.submit = tk.Button(self.root, text="Guardar", command=lambda: self.save_discounts(self.user), **self.style_button)
        self.submit.pack(pady=20)

        self.marco = tk.Frame(self.root, width=150, height=150, bg = '#541388')
        self.marco.pack()
        self.marco.place(anchor = 'center', relx = 0.5, rely = 0.85)

        self.logo = tk.PhotoImage(file = 'Graficos/logo_cuadrado.png')

        self.label= tk.Label(self.marco, image = self.logo, bg = '#541388')
        self.label.pack()
    
        logger.info('Pantalla de Descuento') # Control de Log

    def save_discounts(self, user):
        self.user = user.lower()
        stopped_discount = self.discount_stopped.get()
        moving_discount = self.discount_moving.get()

        stopped_discount = stopped_discount if stopped_discount else 0
        moving_discount = moving_discount if moving_discount else 0

        if Descuentos(self.user, stopped_discount, moving_discount):
            messagebox.showinfo(title = "Exito", message = "Descuentos aplicados")
            logger.info('Pantalla de Descuentos aplicados') # Control de Log
            init_game(self.user)
       
    
    def save_discounts_t(self, user):
        self.user = user.lower()
        turno = self.turno.get()
        tarifa_extra = self.tarifa_extra.get()

        tarifa_extra = tarifa_extra if tarifa_extra else 0

        if Descuentos_taxi(self.user, turno, tarifa_extra):
            messagebox.showinfo(title = "Exito", message = "Descuentos aplicados")
            logger.info('Descuentos aplicados con exito') # Control de Log
            init_game(self.user)


if __name__ == "__main__":
    GUI()