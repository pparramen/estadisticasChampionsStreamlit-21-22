import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def app():
    st.title("Análisis de Tarjetas Amarillas y Rojas por Jugador")

    data = pd.read_csv("baseDatos/disciplinary.csv")

    # Mostrar una vista previa de los datos
    st.write("### Datos cargados:")
    st.dataframe(data[['player_name', 'club', 'position', 'yellow', 'red']])

    # Seleccionar el tipo de tarjeta
    card_type = st.selectbox("Selecciona el tipo de tarjeta:", options=["Amarilla", "Roja"])

    # Seleccionar la posición
    positions = data['position'].unique()
    selected_position = st.multiselect("Filtrar por posición:", options=positions, default=positions)

    # Filtrar los datos por la posición seleccionada
    filtered_data = data[data['position'].isin(selected_position)]

    # Verificar si hay datos después del filtrado
    if filtered_data.empty:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        # Calcular tarjetas por equipo
        summary = filtered_data.groupby('club')[['yellow', 'red']].sum().reset_index()

        # Crear gráficos basados en la selección de tarjeta y posición
        if card_type == "Amarilla":
            st.write("### Gráfico de tarjetas amarillas por equipo y posición:")
            plt.figure(figsize=(15, 8))  # Ajustar el tamaño del gráfico
            plt.bar(summary['club'], summary['yellow'], color='darkorange')  # Gráfico de barras
            plt.xticks(rotation=90)  # Rotar etiquetas del eje X
            plt.title(f"Tarjetas Amarillas por Club (Filtrado por Posición: {', '.join(selected_position)})", fontsize=16)
            plt.xlabel("Club", fontsize=14)  # Etiqueta eje X
            plt.ylabel("Número de Tarjetas Amarillas", fontsize=14)  # Etiqueta eje Y

            # Asegurarse de que solo se muestren números enteros en el eje Y
            y_max = int(summary['yellow'].max()) + 1
            plt.yticks(np.arange(0, y_max, step=1))

            # Mostrar gráfico en Streamlit
            st.pyplot(plt)

        elif card_type == "Roja":
            st.write("### Gráfico de tarjetas rojas por equipo y posición:")
            plt.figure(figsize=(15, 8))  # Ajustar el tamaño del gráfico
            plt.bar(summary['club'], summary['red'], color='red')  # Gráfico de barras
            plt.xticks(rotation=90)  # Rotar etiquetas del eje X
            plt.title(f"Tarjetas Rojas por Club (Filtrado por Posición: {', '.join(selected_position)})", fontsize=16)
            plt.xlabel("Club", fontsize=14)  # Etiqueta eje X
            plt.ylabel("Número de Tarjetas Rojas", fontsize=14)  # Etiqueta eje Y

            # Asegurarse de que solo se muestren números enteros en el eje Y
            y_max = int(summary['red'].max()) + 1
            plt.yticks(np.arange(0, y_max, step=1))

            # Mostrar gráfico en Streamlit
            st.pyplot(plt)

    # Botón para volver al home
    if st.button("Volver a la Página Principal"):
        st.session_state.page = "home"


    # En la Poweshell:
    # cd "C:\Users\Usuario\OneDrive\Escritorio\MASTER_LOYOLA_INDUSTRIAL_IA\year_1\1 Cuatri\Visualización, Procesamiento y Almacenamiento de Datos"
    # streamlit run Tarjetas_Juan.py