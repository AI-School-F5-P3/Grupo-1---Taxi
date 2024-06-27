### Como arrancar el programa
Descargar el archivo '.zip' pulsando en "CODE" y seleccionando la opción. Extraer el contenido de las carpetas y mantener la misma estructura. La aplicación se inicia ejecutando en VSCode el script 'inicio_app.py'.

IMPORTANTE. Comprobar que la carpeta de trabajo es aquella en la que están todos los archivos del '.zip'. Puede abrirse desde vcode de forma manual, abriendo cartpeta donde estan los archivo .zip o mediante código usando los metodos:

- os.getcwd() -> para obtener la dirección completa del directorio de trabajo
- os.chdir('directorio deseado') -> para cambiar el directorio de trabajo

Para poder ejecutar el código se necesita instalar las bibliotecas:
- tkinter
- pygame
- pygame_gui

El codigo incluye un archivo txt que puede ejecutarse con pip para instalar todos los paquetes necesarios en una sola linea: 'pip install -r "ruta/del/arhcivo/requirements.txt"
Si se utiliza Anaconda o Miniconda para python puede instalarse pip en el entorno virtual y despues ejecutar el código previo. No obstante conda no recomienda este método, revisar documentación que se ajuste a cada caso de uso.

Ejecutar el script 'GUI Entrada.py' para comenzar a utilizar la aplicación y seguir los pasos necesarios. Registrarse si es la primera vez y seleccionar tipo de conductor y empresa de pertenencia.

Cuando el inicio de sesión es correcto y no presenta errores se podrán definir los descuentos que se quieran aplicar en el caso de licencias 'VTC' y seleccionar el turno de trabajo en el caso de Taxistas. La tarifa extra solo se aplica durante el horario nocturno.

En el caso de empresas se puede modificar la tarifa base utilizando el menu de inicio de sesión para empresas con:
- Usuario: jefe
- Contraseña: 1234
Esto cambiará las tarifas para los conductores VTC de la empresa Uber.
Se pueden incluir otros casos de uso modificando el archivo 'Empresa.csv'.
