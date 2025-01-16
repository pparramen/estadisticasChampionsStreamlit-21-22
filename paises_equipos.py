import geopandas as gpd
from matplotlib import colors
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import geopandas as gpd
from matplotlib.cm import ScalarMappable
import pandas as pd
import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def app():
    #Leemos los csv
    goals = pd.read_csv("baseDatos/goals.csv")
    goalkeeping =  pd.read_csv("baseDatos/goalkeeping.csv")
    clubs = pd.read_csv("baseDatos/clubs.csv")
    st.title('La Champions League en mapas')

    # Mostramos una vista previa de los datos
    st.subheader("Vista previa de los datos iniciales")
    st.write("Datos de la tabla Goals:")
    st.dataframe(goals.head())
    st.write("Datos de la tabla Goalkeeping:")
    st.dataframe(goalkeeping.head())
    st.write("También tenemos una tabla para asociar los clubes a sus respectivos países.")

    #Agrupamos por club
    goals_grouped = goals.groupby('club', as_index=False)['goals'].sum()
    goalkeeping_grouped = goalkeeping.groupby('club', as_index=False)['conceded'].sum()

    #Juntamos con pais
    goals_goalkeeping_grouped = pd.merge(goals_grouped, goalkeeping_grouped, on="club", how="inner")
    goals_goalkeeping_country_grouped = pd.merge(goals_goalkeeping_grouped, clubs, on = "club", how = "inner")

    # Crear un nuevo dataframe que contenga los equipos por cada país
    df_pais = goals_goalkeeping_country_grouped.groupby('country')['club'].unique().reset_index()
    df_pais['num_clubs'] = df_pais['club'].apply(len)
    df_pais['country'] = df_pais['country'].replace({'England': 'United Kingdom'})

    # Cargar el mapa de Europa
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    europe = world[world['continent'] == 'Europe']
    uk = world[world['name'] == 'United Kingdom']
    europe = pd.concat([europe, uk], ignore_index=True)
    europe = europe.merge(df_pais, left_on="name", right_on="country", how="left")

    st.title('La Champions League en mapas')
    st.divider()
    
    # Dibujar el mapa de Europa con el número de equipos por país
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(-30, 50)  # Límite de longitud para Europa
    ax.set_ylim(35, 72)   # Límite de latitud para Europa

    # Definir los valores discretos y los colores correspondientes
    discrete_values = sorted(df_pais["num_clubs"].unique())  # Obtener los valores únicos de 'num_clubs'
    colors_list = ["#64c5e8", "#acd4e3", "#ffd9d9", "#fc6156", "#800b03"]  # Colores personalizados
    cmap = ListedColormap(colors_list[:len(discrete_values)])  # Crear un colormap con los colores necesarios
    norm = BoundaryNorm(discrete_values + [max(discrete_values) + 1], cmap.N)  # Normalizar los valores discretos

    # Graficar el mapa con colores discretos y la leyenda
    europe.plot(
        column="num_clubs",
        cmap=cmap,
        linewidth=0.8,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        legend_kwds={
            'label': "Número de equipos en Champions por país",
            'orientation': "vertical",
            'shrink': 0.6,  # Ajustar tamaño de la barra
            'ticks': discrete_values  # Ajustar ticks para los valores discretos
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
    st.image(buffer, caption="Mapa de Europa con Número de Equipos en Champions", use_container_width=True)
     
    st.divider()
    st.markdown(
    "<h3 style='text-align: center;'>Espectadores por país</h3>",
    unsafe_allow_html=True
    )
    st.image("baseDatos/EspectadoresFutbol.webp", use_container_width= 40)
    st.divider()
    opcion_sel = st.selectbox("Selecciona una estadística", ["Diferencia de goles", "Goles a favor"])
    # Calcular diferencia de goles
    goals_goalkeeping_country_grouped['goal_difference'] = goals_goalkeeping_country_grouped['goals'] - goals_goalkeeping_country_grouped['conceded']
    # Gráfico de diferencia de goles
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(-30, 50)  # Límite de longitud para Europa
    ax.set_ylim(35, 72)   # Límite de latitud para Europa
    df_pais['diferencia_goles'] = goals_goalkeeping_country_grouped.groupby('country')['goal_difference'].mean().values
    df_pais['goles_a_favor'] = goals_goalkeeping_country_grouped.groupby('country')['goals'].mean().values
    df_pais['goles_en_contra'] = goals_goalkeeping_country_grouped.groupby('country')['conceded'].mean().values
    if opcion_sel == "Diferencia de goles":
        columna = "diferencia_goles"
        label = "Diferencia de goles"
    elif opcion_sel == "Goles a favor":
        columna = "goles_a_favor"
        label = "Goles a favor"
    # Mapa de europa con la diferencia de goles
    europe = europe.merge(df_pais, left_on="name", right_on="country", how="left")
    europe.plot(
        column=columna,
        cmap='coolwarm',
        linewidth=0.8,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        legend_kwds={
            'label': label,
            'orientation': "horizontal",
            'shrink': 0.6,
        }
    )
    if opcion_sel == "Diferencia de goles":
        ax.set_title("Diferencia de goles por país", fontsize=16)
    else:
        ax.set_title("Goles a favor por país", fontsize=16)
    ax.axis("off")
    
    # Guardar el gráfico en un buffer temporal
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    # Mostrar el mapa en Streamlit
    st.image(buffer, use_container_width=True)
    st.caption("¿Dónde está Sturridge?")
    # Botón para volver al home
    if st.button("Volver a la Página Principal"):
        st.session_state.page = "home"  

