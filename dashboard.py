import dash # la librería dash permite crear aplicaciones web interactivas con Python.
from dash import dcc, html
import pandas as pd # Pandas es una librería de manipulación y análisis de datos.
import seaborn as sns # Seaborn es una librería de visualización de datos basada en Matplotlib.
import matplotlib.pyplot as plt # Matplotlib es una librería de visualización de datos en 2D.
import io # La librería io permite trabajar con archivos de entrada y salida.
import base64 # La librería base64 permite codificar y decodificar archivos en base64.
import random # La librería random permite generar números aleatorios.

# Generar datos aleatorios
'''
Se utiliza el método choices de la biblioteca random (incluida con python) para generar 10000 valores de diferentes categorias. Además se genera una variable de horario que se establece en función de la hora en la que se ha registrado la carrera.
Para días tecnicamente deberían generarse los valores de días en función del mes, ya que de esta forma todos los meses tienen 31 días, pero para una simulación nos puede valer.
Una vez se han generado los datos se incluyen en un dataframe de pandas con la misma estructura que el csv que tendríamos de carreras.
'''
dia = random.choices(range(1, 32), k=10000) # Se generan 10.000 números aleatorios entre 1 y 31. 
mes = random.choices(range(1, 13), k=10000)
segundos = random.choices(range(300, 21600), k=10000) # Entre 5 minutos y 6 horas.
precio = random.choices(range(5, 300), k=10000) # Entre 5 y 300 euros.
horas = random.choices(range(1, 23), k=10000)
horario = []
for item in horas:
    if 6 <= item <= 12:
        horario.append("Mañana")
    elif 12 < item <= 21:
        horario.append("Tarde")
    elif 21 < item <= 23:
        horario.append("Noche")
    elif 0 < item < 6:
        horario.append("Madrugada")

df = pd.DataFrame({'Dia': dia, 'Mes': mes, 'Segundos': segundos, 'Precio': precio, 'Horario': horario}) # Se crea un DataFrame con los datos generados.

# Filtrar datos para junio
df_junio = df.loc[df["Mes"] == 6]

# Cálculos previos
num_carreras_dia = df_junio.loc[df_junio['Dia'] == 26].shape[0] #shape 0 nos da el número de filas, siendo cada fila una carrera, nos da el total de carreras
num_carreras_mes = df_junio.shape[0] #shape 0 nos da el número de filas, siendo cada fila una carrera, nos da el total de carreras
dinero_total_dia = df_junio.loc[df_junio['Dia'] == 26, 'Precio'].sum() #sum nos da el sumatorio de todos los elementos de la columna Precio para el df filtrado por día
dinero_total_mes = df_junio['Precio'].sum() #sum nos da el sumatorio de todos los elementos de la columna Precio.
dinero_medio_dia = round(df_junio.loc[df_junio['Dia'] == 26, 'Precio'].mean(), 2) #mean nos da la media de la columna Precio para el df filtrado por día, en este caso redondeada a dos decimales, que es lo que tiene sentido para euros
dinero_medio_mes = round(df_junio['Precio'].mean(), 2) # mean nos da la media de Precio, en este caso redondeada a dos decimales, que es lo que tiene sentido para euros

# Configurar paleta de colores para los gráficos generados por seaborn
sns.set_palette("pastel")

# tamaño de los gráficos que se van a generar
plt.figure(figsize=(17, 10))

# Gráfico de línea: Precio medio por mes
plt.subplot(3, 2, 1) # Se crea un subplot (un gráfico dentro de otro gráfico) con 3 filas y 2 columnas. # subplot nos permite colocar los gráficos en posiciones concretas
sns.lineplot(data=df, x='Mes', y='Precio', errorbar=None, color = '#541388') # Crea el gráfico de línea.
plt.title('Precio Medio por Mes')

# Histograma total de carreras por mes
plt.subplot(3, 2, 2) # Se crea un subplot en la segunda posición.
sns.countplot(data=df, x='Mes', color = '#541388') # Crea el histograma.
plt.title('Histograma de Carreras por Mes')
plt.ylabel('Recuento carreras') # Añade etiqueta al eje Y.

# Gráfico de línea: Media de precio por día en Junio
plt.subplot(3, 2, 3) # Se crea un subplot en la tercera posición.
sns.lineplot(data=df_junio, x='Dia', y='Precio', errorbar=None, color = '#541388')
plt.title('Media de Precio por Día en Junio')

# Histograma número de carreras por día en Junio
plt.subplot(3, 2, 4)
sns.countplot(data=df_junio, x='Dia', color = '#541388')
plt.title('Histograma de Carreras por Día en Junio')
plt.ylabel('Recuento carreras')

# Histograma número de carreras por horario en Junio
plt.subplot(3, 2, 5)
sns.countplot(data = df_junio, x = 'Horario', color = '#541388')
plt.title('Histograma de Carreras según Horario en Junio')
plt.ylabel('Recuento carreras')

#Gráfico de barras: Media de precio según horario en Junio.
plt.subplot(3, 2, 6)
sns.barplot(data = df_junio, x = 'Horario', y = 'Precio', color = '#541388')
plt.title('Media de precio por Horario en Junio')
plt.ylabel('Media de Precio')
# Ajustar diseño y guardar figura en un archivo
plt.tight_layout()
plt.savefig('plot.png')  # Guarda el gráfico como imagen PNG

# Convertir imagen a base64 para mostrar en Dash
plt.close() # Cierra la figura para liberar memoria.
image_filename = 'plot.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii') # Conversor.

# Crear aplicación Dash
app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Estilos externos para la aplicación Dash.

class Dashboard:
    def __init__(self):
        self.app = dash.Dash(__name__) # Inicializar la aplicación Dash.
        self.server = self.app.server
# Definir el layout de la aplicación con los colores básicos de nuestra aplicación y con la fuente que hemos usado habitualmente.
        self.app.layout = html.Div(style={'backgroundColor': '#541388', 'color': '#C8F50A', 'font-family': 'Lucida Console'}, children=[
            html.H1('Dashboard de Análisis de Carreras', style={'textAlign': 'center'}),

            # Mostrar los cálculos como texto en 2 filas y 3 columnas
            html.Div([
                html.Div([
                    html.H3('Número de Carreras por Día'),
                    html.Div(f'{num_carreras_dia}')
                ], className='four columns'),

                html.Div([
                    html.H3('Número de Carreras por Mes'),
                    html.Div(f'{num_carreras_mes}')
                ], className='four columns'),

                html.Div([
                    html.H3('Dinero Total Recaudado en el Día'),
                    html.Div(f'${dinero_total_dia}')
                ], className='four columns'),
            ], className='row'),

            html.Div([
                html.Div([
                    html.H3('Dinero Total Recaudado en el Mes'),
                    html.Div(f'${dinero_total_mes}')
                ], className='four columns'),

                html.Div([
                    html.H3('Dinero Medio Recaudado en el Día'),
                    html.Div(f'${dinero_medio_dia:.2f}')
                ], className='four columns'),

                html.Div([
                    html.H3('Dinero Medio Recaudado en el Mes'),
                    html.Div(f'${dinero_medio_mes}')
                ], className='four columns'),
            ], className='row'),

            # Mostrar las imágenes en un layout de cuadrícula
            html.Div([
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image)) # Muestra la imagen del gráfico.
                ], className='six columns'),
            ], className='row'),
        ])

    def init_server(self):
        # Función que inicia el servidor en dash para poder visualizarlo. Para cerrarlo hay que pulsar ctrl+c en la terminal de ejecución de vscode.
        self.app.run_server(debug=False)
