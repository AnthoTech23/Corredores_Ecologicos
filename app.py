import streamlit as st

from Utils.estilos import cargar_estilos

from Paginas.inicio import mostrar_inicio
from Paginas.ambiental import mostrar_ambiental
from Paginas.machine_learning import mostrar_machine_learning
from Paginas.temporal import mostrar_temporal
from Paginas.reportes import generar_pdf
from Paginas.acerca import mostrar_acerca


st.set_page_config(
    page_title="EcoConnect Panamá",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

cargar_estilos()


# =====================================================
# BARRA SUPERIOR
# =====================================================

st.markdown("""
<div class="app-header">
    <div class="app-title">
        EConnect Panamá
    </div>
</div>
""", unsafe_allow_html=True)

pagina = st.radio(
    label="Navegación",
    options=[
        "Inicio",
        "Análisis Ambiental",
        "Machine Learning",
        "Análisis Temporal",
        "Reportes",
        "Acerca del Proyecto"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


st.markdown("<hr class='nav-separator'>", unsafe_allow_html=True)


# =====================================================
# CONTROL DE PÁGINAS
# =====================================================

if pagina == "Inicio":

    mostrar_inicio()

elif pagina == "Análisis Ambiental":

    mostrar_ambiental()

elif pagina == "Machine Learning":

    mostrar_machine_learning()

elif pagina == "Análisis Temporal":

    mostrar_temporal()

elif pagina == "Reportes":

    generar_pdf()

else:

    mostrar_acerca()