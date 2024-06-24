import tkinter as tk
from tkinter import messagebox
from Check_passwords import LogIn, Register, Pregunta, Respuesta, Descuentos, Descuentos_taxi
from IU_Class import init_game


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inicio de Sesión")
        self.root.geometry('800x600')
        self.root.configure(bg='#541388')
        
        self.style_button = {'font': ('Lucida Console', 16), 'bg': '#C8F50A', 'fg': '#541388', 'padx': 20, 'pady': 10, 'bd': 0}
        
        self.p_inicio()

        self.root.mainloop()

    def p_inicio(self):

        self.clear_screen()

        self.inicio = tk.Button(self.root, text="Iniciar Sesión", command=self.login_screen, **self.style_button)
        self.inicio.pack(pady=75)
        
        self.reg = tk.Button(self.root, text="Registrarse", command=self.reg_screen, **self.style_button)
        self.reg.pack(pady=75)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()
        
        self.label = tk.Label(self.root, text="Inicie Sesión", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label.pack(pady=20)
        
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
        
        self.button = tk.Button(self.root, text="Iniciar Sesión", command=self.check_password, **self.style_button)
        self.button.pack(pady=20)
        
        self.button_forgot = tk.Button(self.root, text="Olvidé mi contraseña", command=self.res_pswd, **self.style_button)
        self.button_forgot.pack(pady=10)

        self.button_back = tk.Button(self.root, text="Atrás", command=self.p_inicio, **self.style_button)
        self.button_back.pack(pady=10)
    
    def reg_screen(self):
        self.clear_screen()
        
        self.label = tk.Label(self.root, text='Registro', font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label.pack(pady=20)
        
        self.label_user = tk.Label(self.root, text="Usuario:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_user.pack(pady = 5)
        self.user = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user.pack(pady=10)
        
        self.label_password = tk.Label(self.root, text="Contraseña", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_password.pack(pady = 5)
        self.password = tk.Entry(self.root, font=('Lucida Console', 16), show='*')
        self.password.pack(pady=10)
        
        self.label_quest = tk.Label(self.root, text="Defina una pregunta secreta para cambiar la contraseña en caso de olvido", font=('Lucida Console', 12), bg='#541388', fg='white')
        self.label_quest.pack(pady = 5)
        self.quest = tk.Entry(self.root, font=('Lucida Console', 16))
        self.quest.pack(pady=10)
        
        self.label_answ = tk.Label(self.root, text="Defina una respuesta para su pregunta secreta", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_answ.pack(pady = 5)
        self.answ = tk.Entry(self.root, font=('Lucida Console', 16))
        self.answ.pack(pady=10)

        self.label_dropdown = tk.Label(self.root, text="Seleccione tipo de conductor:", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_dropdown.pack(pady=5)

        # Lista vacía para el menú desplegable
        options = ["Taxista", "VTC"]
        self.selected_option = tk.StringVar()
        self.selected_option.set("")

        self.dropdown = tk.OptionMenu(self.root, self.selected_option, *options)
        self.dropdown.config(font=('Lucida Console', 16), bg='#C8F50A', fg='#4100A8', width=20)
        self.dropdown.pack(pady=5)
        
        button_frame = tk.Frame(self.root, bg='#791E94')
    
        self.button_register = tk.Button(button_frame, text="Registro", command=self.register, **self.style_button)
        self.button_register.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.button_back = tk.Button(button_frame, text="Incio de Sesion", command=self.login_screen, **self.style_button)
        self.button_back.pack(side=tk.LEFT, padx=10, pady=10)

        button_frame.pack(pady=20)
    
    def res_pswd(self):
        self.clear_screen()
        
        self.label = tk.Label(self.root, text="Reiniciar contraseña", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label.pack(pady=20)

        self.label_user = tk.Label(self.root, text="Nombre de usuario", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label_user.pack(pady = 5)
        self.user = tk.Entry(self.root, font=('Lucida Console', 16))
        self.user.pack(pady=10)
        
        self.quest = tk.Button(self.root, text="Ver pregunta secreta", command=self.get_quest, **self.style_button)
        self.quest.pack(pady=10)
        
        self.label2 = tk.Label(self.root, text="Escriba su respuesta secreta", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label2.pack(pady=10)
        
        self.answer = tk.Entry(self.root, font=('Lucida Console', 16))
        self.answer.pack(pady=10)
        
        self.label3 = tk.Label(self.root, text="Nueva contraseña", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label3.pack(pady=10)
        
        self.new_pswd = tk.Entry(self.root, font=('Lucida Console', 16), show='*')
        self.new_pswd.pack(pady=10)
        
        self.submit = tk.Button(self.root, text="Enviar", command=self.change_pswd, **self.style_button)
        self.submit.pack(pady=20)
        
        self.back = tk.Button(self.root, text="Atrás", command=self.login_screen, **self.style_button)
        self.back.pack(pady=10)

    def check_password(self):
        log = LogIn(self.user.get().lower(), self.password.get())
        user = self.user.get()
        if log == False:
            messagebox.showinfo(title = "Error", message = "Nombre de usuario o contraseña equivocados")
        else:
            if log == 'VTC':
                self.discount_screen(user)
            elif log == 'Taxista':
                self.turno_screen(user)

    def register(self):
        if Register(self.user.get().lower(), self.password.get(), self.quest.get(), self.answ.get().lower(), self.selected_option.get()) == True:
            self.login_screen()

    def get_quest(self):
        Pregunta(self.user.get().lower())
    
    def change_pswd(self):
        Respuesta(self.user.get().lower(), self.answer.get().lower(), self.new_pswd.get())

    def turno_screen(self, user):
        self.clear_screen()
        self.user = user

        self.label = tk.Label(self.root, text="Tarifas", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label.pack(pady=20)
        
        self.label1 = tk.Label(self.root, text="Turno", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label1.pack(pady=10)

        options = ["Diurno", "Nocturno"]
        self.turno = tk.StringVar()
        self.turno.set("")

        self.dropdown = tk.OptionMenu(self.root, self.turno, *options)
        self.dropdown.config(font=('Lucida Console', 16), bg='#C8F50A', fg='#4100A8', width=20)
        self.dropdown.pack(pady=5)
        
        
        self.label2 = tk.Label(self.root, text="Porcentaje de aumento de tarifa (solo para noche)", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label2.pack(pady=10)
        
        self.tarifa_extra = tk.Entry(self.root, font=('Lucida Console', 16))
        self.tarifa_extra.pack(pady=10)
        
        self.submit = tk.Button(self.root, text="Guardar", command=lambda: self.save_discounts_t(self.user), **self.style_button)
        self.submit.pack(pady=20)

    def discount_screen(self, user):
        self.clear_screen()
        self.user = user

        self.label = tk.Label(self.root, text="Descuentos", font=('Lucida Console', 20), bg='#541388', fg='white')
        self.label.pack(pady=20)
        
        self.label1 = tk.Label(self.root, text="Porcentaje de descuento parado", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label1.pack(pady=10)
        
        self.discount_stopped = tk.Entry(self.root, font=('Lucida Console', 16))
        self.discount_stopped.pack(pady=10)
        
        self.label2 = tk.Label(self.root, text="Porcentaje de descuento movimiento", font=('Lucida Console', 16), bg='#541388', fg='white')
        self.label2.pack(pady=10)
        
        self.discount_moving = tk.Entry(self.root, font=('Lucida Console', 16))
        self.discount_moving.pack(pady=10)
        
        self.submit = tk.Button(self.root, text="Guardar", command=lambda: self.save_discounts(self.user), **self.style_button)
        self.submit.pack(pady=20)
    
    def save_discounts(self, user):
        self.user = user.lower()
        stopped_discount = self.discount_stopped.get()
        moving_discount = self.discount_moving.get()

        stopped_discount = stopped_discount if stopped_discount else 0
        moving_discount = moving_discount if moving_discount else 0

        Descuentos(self.user.lower(), stopped_discount, moving_discount)
        messagebox.showinfo(title = "Exito", message = "Descuentos aplicados")
        init_game(self.user)
        # Aquí puedes agregar la lógica para manejar los valores de descuento ingresados
    
    def save_discounts_t(self, user):
        self.user = user.lower()
        turno = self.turno.get()
        tarifa_extra = self.tarifa_extra.get()

        tarifa_extra = tarifa_extra if tarifa_extra else '0'

        Descuentos_taxi(self.user.lower(), turno, tarifa_extra)
        messagebox.showinfo(title = "Exito", message = "Descuentos aplicados")
        init_game(self.user)


GUI()