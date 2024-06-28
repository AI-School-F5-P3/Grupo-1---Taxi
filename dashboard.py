import dash
from dash import dcc, html
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import random

# Generar datos aleatorios
dia = random.choices(range(1, 32), k=10000)
mes = random.choices(range(1, 13), k=10000)
segundos = random.choices(range(300, 21600), k=10000)
precio = random.choices(range(5, 300), k=10000)
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

df = pd.DataFrame({'Dia': dia, 'Mes': mes, 'Segundos': segundos, 'Precio': precio, 'Horario': horario})

# Filtrar datos para junio
df_junio = df.loc[df["Mes"] == 6]

# Cálculos previos
num_carreras_dia = df_junio.loc[df_junio['Dia'] == 26].shape[0]
num_carreras_mes = df_junio.shape[0]
dinero_total_dia = df_junio.loc[df_junio['Dia'] == 26, 'Precio'].sum()
dinero_total_mes = df_junio['Precio'].sum()
dinero_medio_dia = df_junio.loc[df_junio['Dia'] == 26, 'Precio'].mean()
dinero_medio_mes = round(df_junio['Precio'].mean(), 2)

# Configurar estilo de seaborn
sns.set_palette("pastel")

# Crear gráficos utilizando Seaborn y Matplotlib
plt.figure(figsize=(17, 10))

# Gráfico de línea: Precio medio por mes
plt.subplot(3, 2, 1)
sns.lineplot(data=df, x='Mes', y='Precio', errorbar=None, color = '#541388')
plt.title('Precio Medio por Mes')

# Histograma total de carreras por mes
plt.subplot(3, 2, 2)
sns.countplot(data=df, x='Mes', color = '#541388')
plt.title('Histograma de Carreras por Mes')
plt.ylabel('Recuento carreras')

# Gráfico de línea: Media de precio por día en Junio
plt.subplot(3, 2, 3)
sns.lineplot(data=df_junio, x='Dia', y='Precio', errorbar=None, color = '#541388')
plt.title('Media de Precio por Día en Junio')

# Histograma número de carreras por día en Junio
plt.subplot(3, 2, 4)
sns.countplot(data=df_junio, x='Dia', color = '#541388')
plt.title('Histograma de Carreras por Día en Junio')
plt.ylabel('Recuento carreras')

# Ajustar diseño y guardar figura en un archivo
plt.tight_layout()
plt.savefig('plot.png')  # Guardar el gráfico como imagen PNG

# Convertir imagen a base64 para mostrar en Dash
plt.close()
image_filename = 'plot.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

# Crear aplicación Dash
app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Dashboard:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.server = self.app.server
# Definir el layout de la aplicación con el fondo gris oscuro
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
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image))
                ], className='six columns'),
            ], className='row'),
        ])

    def init_server(self):
        self.app.run_server(debug=False)
