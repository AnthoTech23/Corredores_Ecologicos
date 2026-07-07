import streamlit as st

from Utils.configuracion import (
    TITULO,
    SUBTITULO,
    AREA_ESTUDIO,
    SATELITE,
    MODELO,
    RESOLUCION,
    PRECISION
)

def mostrar_inicio():

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(f"""
    <div class="header">

    <h1> {TITULO}</h1>

    <h3>{SUBTITULO}</h3>

    <p> Ciudad del Saber • Camino de Cruces • Cerro Ancón</p>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # RESUMEN
    # =====================================================

    st.markdown("""
    <div class="summary-box">

    <h3> Resumen Ejecutivo</h3>

    <p style="text-align:justify;">

    EcoConnect Panamá es una plataforma desarrollada para monitorear la
    conectividad ecológica del corredor urbano comprendido entre Ciudad del Saber,
    Camino de Cruces y Cerro Ancón.

    El sistema integra imágenes satelitales Sentinel-2, procesamiento geoespacial
    con Google Earth Engine, análisis en Python y un modelo de Machine Learning
    basado en Random Forest para clasificar automáticamente el estado de la
    conectividad ecológica.

    </p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # TARJETAS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(f"""
        <div class="card">

        <h3>Área de Estudio</h3>

        <ul>

        <li>{AREA_ESTUDIO[0]}</li>

        <li>{AREA_ESTUDIO[1]}</li>

        <li>{AREA_ESTUDIO[2]}</li>

        </ul>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="card">

        <h3>Información Técnica</h3>

        <b>Satélite:</b> {SATELITE}<br>

        <b>Resolución:</b> {RESOLUCION}<br>

        <b>Modelo IA:</b> {MODELO}<br>

        <b>Precisión:</b> {PRECISION}

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # TECNOLOGÍAS
    # =====================================================

    st.subheader("Tecnologías Utilizadas")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info("""
### 🛰 Google Earth Engine

Obtención y procesamiento de imágenes Sentinel-2.
""")

        st.info("""
### Python

Procesamiento geoespacial y análisis de datos.
""")

    with c2:

        st.info("""
### Rasterio

Lectura y procesamiento de datos ráster.
""")

        st.info("""
### Índices Ambientales

NDVI

NDWI

NDBI

ICE
""")

    with c3:

        st.info("""
### Machine Learning

Random Forest

Clasificación automática
""")

        st.info("""
### Streamlit

Visualización interactiva
""")

    st.divider()

    # =====================================================
    # OBJETIVOS
    # =====================================================

    st.subheader("Objetivo del Proyecto")

    st.success("""
Desarrollar una plataforma inteligente para el monitoreo de la conectividad ecológica
del corredor Ciudad del Saber – Camino de Cruces – Cerro Ancón mediante imágenes
satelitales, procesamiento geoespacial e inteligencia artificial.
""")

    st.divider()

    # =====================================================
    # FLUJO DEL SISTEMA
    # =====================================================

    st.subheader("Flujo General del Sistema")

    st.markdown("""
```text
Sentinel-2
      │
      ▼
Google Earth Engine
      │
      ▼
Índices Ambientales
(NDVI - NDWI - NDBI)
      │
      ▼
Python
(Rasterio - Pandas)
      │
      ▼
Machine Learning
(Random Forest)
      │
      ▼
Dashboard Interactivo
(Streamlit)
    """)