import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("¿Cómo es la efectividad defensiva de los clubes en la Champions League?")

# Cargar datasets específicos
df_defending = pd.read_csv("baseDatos/defending.csv")  
df_disciplinary = pd.read_csv("baseDatos/disciplinary.csv")  

# Mostramos una vista previa de los datos
st.subheader("Vista previa de los datos iniciales")
st.write("Datos de la tabla Defending:")
st.dataframe(df_defending.head())
st.write("Datos de la tabla Disciplinary:")
st.dataframe(df_disciplinary.head())

# Creamos una tabla combinando los datos que utilizaremos en nuestra gráfica
merged_data = pd.merge(
    df_defending[["player_name", "club","balls_recoverd", "tackles"]],  # Subconjunto relevante del primer DataFrame
    df_disciplinary[["player_name","club", "fouls_committed", "minutes_played"]],      # Subconjunto relevante del segundo DataFrame
    on=["player_name", "club"]  # La columna común es "club"
)


# Agrupar por club y calcular las sumas totales
club_data = merged_data.groupby("club").sum().reset_index()
st.subheader("Tabla de clubes según los balones recuperados respecto a las faltas cometidas")
#Mostramos la tabla conjunta organizada por clubes
st.dataframe(club_data.drop(columns=["player_name"]))

# Creamos el primer gráfico
st.subheader("Comparación de Faltas Cometidas por Balones Recuperados por club")
fig, ax = plt.subplots(figsize=(20, 12))

# Dibujar las barras
ax.bar(club_data["club"], club_data["balls_recoverd"], label="Balones recuperados", color="blue", alpha=0.7)
ax.bar(club_data["club"], club_data["fouls_committed"], label="Faltas cometidas", color="red", alpha=0.7)

# Calcular y agregar los porcentajes sobre las barras
for i, club in enumerate(club_data["club"]):
    balls_recovered = club_data["balls_recoverd"][i]
    fouls = club_data["fouls_committed"][i]
    
    # Calcular el porcentaje de Faltas Cometidas por Balones Recuperados
    percentage = (fouls / balls_recovered * 100) if balls_recovered > 0 else 0
    
    
    y_text = max(balls_recovered, fouls) + 1  # Colocar el texto ligeramente por encima de la barra más alta
    
   # Agregar el texto del porcentaje
    ax.text(
        i, 
        y_text, 
        f"{percentage:.1f}%",  
        fontsize=13,  
        fontweight="bold", 
        ha="center"  
    )


# Etiquetas y formato
ax.set_xlabel("Club", fontsize=30)
ax.set_ylabel("Cantidad", fontsize=30)
ax.legend(fontsize=20)
ax.tick_params(axis="x", rotation=90, labelsize=20)  
ax.tick_params(axis="y", labelsize=20)

# Mostrar el gráfico
st.pyplot(fig)


# Creamos el segundo gráfico
st.subheader("Faltas Cometidas por Entradas realizadas por club")
fig1, ax1 = plt.subplots(figsize=(50, 50))  # Tamaño ajustado para mayor claridad


bar_width = 0.6 
clubs = club_data["club"]
y_positions = [i * 3 for i in range(len(clubs))]  # Posiciones de las barras

# Dibujar las barras horizontales
ax1.barh(
    [y - bar_width / 2 for y in y_positions], 
    club_data["tackles"], 
    color="deepskyblue", 
    label="Entradas realizadas" if "Entradas realizadas" not in ax1.get_legend_handles_labels()[1] else "", 
    height=bar_width
)
ax1.barh(
    [y + bar_width / 2 for y in y_positions], 
    club_data["fouls_committed"], 
    color="crimson", 
    label="Faltas cometidas" if "Faltas cometidas" not in ax1.get_legend_handles_labels()[1] else "", 
    height=bar_width
)

# Agregar porcentajes sobre las barras
for i, club in enumerate(clubs):
    tackles = club_data["tackles"][i]
    fouls = club_data["fouls_committed"][i]
    
    # Calcular porcentaje de Faltas Cometidas por Entradas realizadas
    percentage = (fouls / tackles * 100) if tackles > 0 else 0
    
    
    y_text = y_positions[i]
    x_text = max(tackles, fouls) + 5 
    
   
    ax1.text(
        x_text, 
        y_text, 
        f"{percentage:.1f}%",  
        fontsize=30,  
        fontweight="bold",  
        ha="center",  
        va="center"   
    )

# Etiquetas y formato
ax1.set_yticks(y_positions)
ax1.set_yticklabels(clubs, fontsize=30) 
ax1.set_xlabel("Cantidad", fontsize=40)  
ax1.set_ylabel("Club", fontsize=40)     
ax1.legend(fontsize=30)                  
ax1.tick_params(axis="x", labelsize=30) 
ax1.tick_params(axis="y", labelsize=30)  
ax1.invert_yaxis()  


plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.1)

st.pyplot(fig1)



#############################################FILTROS POR CLUBES################################################

st.subheader("Tabla de jugadores según los balones recuperados respecto a las faltas cometidas")
st.dataframe(merged_data)

# Filtro por clubes para ver a sus jugadores
st.subheader("Filtrar efectividad defensiva individual por club")
equipos = merged_data["club"].unique()
equipo_seleccionado = st.selectbox("Selecciona un club", equipos)
# Filtrar los datos por el equipo seleccionado
datos_filtrados = merged_data[merged_data["club"] == equipo_seleccionado]

#Creamos la tercera gráfica
st.subheader(f"Comparación de balones recuperados vs  faltas cometidas vs entradas realizadas  - {equipo_seleccionado}")
fig, ax = plt.subplots(figsize=(20, 12))
datos_filtrados.set_index("player_name")[["balls_recoverd", "fouls_committed", "tackles"]].plot(kind="bar", ax=ax, width=0.8, legend=True)
ax.set_xlabel("Jugador", fontsize=30)
ax.set_ylabel("Cantidad", fontsize=30)
ax.tick_params(axis="x", rotation=90, labelsize=20)  
ax.tick_params(axis="y", labelsize=20)
ax.legend(["Balones recuperados", "Faltas cometidas", "Entradas realizadas"], fontsize=20)
st.pyplot(fig)



# Filtrar los 5 jugadores con mejores estadísticas (por balones recuperados)
top_5 = datos_filtrados.nlargest(5, "balls_recoverd")  # Ordenar por "balls_recoverd" y tomar los 5 primeros

# Gráfico de burbujas
st.subheader(f"Comparación individual de Entradas realizadas y Faltas cometidas en relación a los Balones recuperados - {equipo_seleccionado}")
fig, ax = plt.subplots(figsize=(20, 12))
bubble_size = top_5["balls_recoverd"] * 50  # Escalar el tamaño de la burbuja
ax.scatter(
    top_5["tackles"], 
    top_5["fouls_committed"], 
    s=bubble_size,  
    alpha=0.7, 
    color="blue"
)

# Etiquetas para los jugadores
for i, row in top_5.iterrows():
    ax.text(row["tackles"], row["fouls_committed"] + 1, row["player_name"], fontsize=20, fontweight="bold", ha="center", va="top")


ax.set_xlabel("Entradas realizadas", fontsize=30)
ax.set_ylabel("Faltas cometidas", fontsize=30)
ax.tick_params(axis="x", labelsize=20)  
ax.tick_params(axis="y", labelsize=20)

# Mostrar el gráfico
st.pyplot(fig)


