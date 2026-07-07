import streamlit as st


def mostrar_acerca():

    st.title("ℹ️ Acerca del Proyecto")

    st.markdown("""
## Plataforma Inteligente para el Monitoreo de la Conectividad Ecológica
### Ciudad del Saber – Camino de Cruces – Cerro Ancón
""")

    st.divider()

    st.subheader("🎯 Objetivo General")

    st.write("""
Desarrollar una plataforma inteligente para monitorear la conectividad ecológica
utilizando imágenes satelitales, procesamiento geoespacial e inteligencia artificial.
""")

    st.subheader("🎯 Objetivos Específicos")

    st.markdown("""

- Procesar imágenes Sentinel-2 mediante Google Earth Engine.
- Calcular índices ambientales (NDVI, NDWI, NDBI e ICE).
- Clasificar automáticamente la conectividad ecológica utilizando Random Forest.
- Visualizar los resultados mediante un dashboard interactivo.

""")

    st.divider()

    st.subheader("🏗 Arquitectura")

    st.code("""
Sentinel-2
      ↓
Google Earth Engine
      ↓
Índices Ambientales
      ↓
Python
(Rasterio - Pandas)
      ↓
Random Forest
      ↓
Streamlit
""")

    st.divider()

    st.subheader("🛠 Tecnologías")

    c1, c2 = st.columns(2)

    with c1:

        st.success("""
🛰 Sentinel-2

🌍 Google Earth Engine

🐍 Python

📊 Rasterio
""")

    with c2:

        st.success("""
🤖 Scikit-Learn

📈 Plotly

🗺 Folium

💻 Streamlit
""")

    st.divider()

    st.subheader("🌎 Objetivos de Desarrollo Sostenible")

    st.markdown("""

- ODS 11 — Ciudades y comunidades sostenibles.
- ODS 13 — Acción por el clima.
- ODS 15 — Vida de ecosistemas terrestres.

""")

    st.divider()

    st.info("""
Proyecto desarrollado como parte de la asignatura de Tópicos Especiales II
utilizando herramientas de análisis geoespacial e Inteligencia Artificial.
""")