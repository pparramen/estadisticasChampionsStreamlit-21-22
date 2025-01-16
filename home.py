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
    elif st.button("La Champions League por Países"):
        change_page("paises_equipos")
    elif st.button("Ir a Página 3"):
        change_page("pagina3")

# Navegar a RobosTarjeta.py
elif st.session_state.page == "RobosTarjeta":
    from RobosTarjeta import app
    app()

# Navegar a pagina2.py
elif st.session_state.page == "paises_equipos":
    from paises_equipos import app
    app()

# Navegar a pagina3.py
elif st.session_state.page == "pagina3":
    from pagina3 import app
    app()
