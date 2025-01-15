import streamlit as st

# Inicializar el estado de la página
if "page" not in st.session_state:
    st.session_state.page = "home"

# Función para cambiar de página
def change_page(page_name):
    st.session_state.page = page_name

# Página principal
if st.session_state.page == "home":
    st.title("Página Principal de estadísticas de la Champions League 2021-2022")
    st.image("baseDatos/equiposChampions.webp", use_container_width= 50)
    st.write("Selecciona una opción para navegar a diferentes páginas:")

    # Botones de navegación
    if st.button("Efectividad Defensiva de los Clubes en la Champions League"):
        change_page("RobosTarjeta")
    elif st.button("Ir a Página 2"):
        change_page("pagina2")
    elif st.button("Juego limpio en los Clubes de la Champions League"):
        change_page("Tarjetas_Jugadores")

# Navegar a RobosTarjeta.py
elif st.session_state.page == "RobosTarjeta":
    from RobosTarjeta import app
    app()

# Navegar a pagina2.py
elif st.session_state.page == "pagina2":
    from pagina2 import app
    app()

# Navegar a pagina3.py
elif st.session_state.page == "Tarjetas_Jugadores":
    from Tarjetas_Jugadores import app
    app()
