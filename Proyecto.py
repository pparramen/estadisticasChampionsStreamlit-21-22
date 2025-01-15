import geopandas as gpd
from matplotlib import colors
import geopandas as gpd
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import pandas as pd
import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

#Leemos los csv
goals = pd.read_csv("baseDatos/goals.csv")
goalkeeping =  pd.read_csv("baseDatos/goalkeeping.csv")
clubs = pd.read_csv("baseDatos/clubs.csv")

#Agrupamos por club
goals_grouped = goals.groupby('club', as_index=False)['goals'].sum()
goalkeeping_grouped = goalkeeping.groupby('club', as_index=False)['conceded'].sum()

#Juntamos con pais
goals_goalkeeping_grouped = pd.merge(goals_grouped, goalkeeping_grouped, on="club", how="inner")
goals_goalkeeping_country_grouped = pd.merge(goals_goalkeeping_grouped, clubs, on = "club", how = "inner")

# Crear un nuevo dataframe que contenga los equipos por cada país
df_pais = goals_goalkeeping_country_grouped.groupby('country')['club'].unique().reset_index()
df_pais['num_clubs'] = df_pais['club'].apply(len)

# Cargar el mapa de Europa
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
europe = world[world['continent'] == 'Europe']
europe = europe.merge(df_pais, left_on="name", right_on="country", how="left")

st.title('Análisis de equipos por país en la Champions League')

# Dibujar el mapa de Europa con el número de equipos por país
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-30, 40)  # Límite de longitud para Europa
ax.set_ylim(35, 72)   # Límite de latitud para Europa
norm = colors.Normalize(vmin=df_pais["num_clubs"].min(), vmax=df_pais["num_clubs"].max()) # Normalizar los valores de 'num_clubs' para la leyenda
cmap = plt.cm.coolwarm # Elegir un mapa de colores
# Graficar el mapa con la leyenda personalizada
europe.plot(
    column="num_clubs",
    cmap=cmap,
    linewidth=0.8,
    ax=ax,
    edgecolor="0.8",
    legend=True,
    legend_kwds={
        'label': "Número de equipos en Champions por país",
        'orientation': "horizontal",
        'shrink': 0.6  # Ajustar tamaño de la barra
    }
)

ax.set_title("Equipos en Champions por país", fontsize=16)
ax.axis("off")

# Guardar el gráfico en un buffer temporal
from io import BytesIO
buffer = BytesIO()
plt.savefig(buffer, format="png", bbox_inches="tight")
buffer.seek(0)

# Mostrar el mapa en Streamlit
st.image(buffer, caption="Mapa de Europa con Número de Equipos en Champions", use_column_width=True)

st.subheader("Gráfica de Diferencia de Goles por Club")

pais_seleccionado = st.selectbox("Selecciona un país", goals_goalkeeping_country_grouped["country"].unique())

# Calcular diferencia de goles
goals_goalkeeping_country_grouped['goal_difference'] = goals_goalkeeping_country_grouped['goals'] - goals_goalkeeping_country_grouped['conceded']
# Gráfico de diferencia de goles
fig, ax = plt.subplots(figsize=(10, 6))
df_sorted = goals_goalkeeping_country_grouped.sort_values(by='goal_difference', ascending=False)
# Filtrar los datos por el país seleccionado
bars = sns.barplot(x = 'club', y = 'goal_difference', data = df_filtrado, dodge = False)
ax.axhline(0, color='black', linewidth=0.8)

ax.set_xlabel("Club")
ax.set_ylabel("Diferencia de Goles")
ax.set_title("Diferencia de Goles por Club")
ax.set_xticklabels(df_filtrado['club'], rotation=90)

st.pyplot(fig)

