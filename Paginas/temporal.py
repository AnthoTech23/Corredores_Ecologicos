import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_temporal():

    st.title("📊 Análisis Temporal de Conectividad")

    st.write("""
    Esta sección compara datos reales obtenidos de imágenes Sentinel-2 para los años 2022 y 2025.
    A partir de la tendencia observada, también se genera una simulación prospectiva para años futuros.
    """)

    # ==============================
    # CARGAR DATASETS REALES
    # ==============================

    df_2022 = pd.read_csv("Datos/dataset_2022_clasificado.csv")
    df_2025 = pd.read_csv("Datos/dataset_2025_clasificado.csv")

    df_2022["Periodo"] = "2022"
    df_2025["Periodo"] = "2025"

    df_real = pd.concat([df_2022, df_2025], ignore_index=True)

    st.divider()

    # ==============================
    # KPIs REALES
    # ==============================

    ndvi_2022 = df_2022["NDVI"].mean()
    ndvi_2025 = df_2025["NDVI"].mean()

    ice_2022 = df_2022["ICE"].mean()
    ice_2025 = df_2025["ICE"].mean()

    cambio_ndvi = ndvi_2025 - ndvi_2022
    cambio_ice = ice_2025 - ice_2022

    st.subheader("📌 Indicadores Reales 2022 vs 2025")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("NDVI 2022", f"{ndvi_2022:.3f}")
    c2.metric("NDVI 2025", f"{ndvi_2025:.3f}", f"{cambio_ndvi:.3f}")

    c3.metric("ICE 2022", f"{ice_2022:.3f}")
    c4.metric("ICE 2025", f"{ice_2025:.3f}", f"{cambio_ice:.3f}")

    st.divider()

    # ==============================
    # GRÁFICOS REALES
    # ==============================

    muestra_real = df_real.sample(
        min(12000, len(df_real)),
        random_state=42
    )

    st.subheader("🌿 Comparación Real del NDVI")

    fig_ndvi = px.box(
        muestra_real,
        x="Periodo",
        y="NDVI",
        color="Periodo",
        title="Comparación real del NDVI entre 2022 y 2025"
    )

    st.plotly_chart(fig_ndvi, use_container_width=True)

    st.subheader("🌎 Comparación Real del ICE")

    fig_ice = px.box(
        muestra_real,
        x="Periodo",
        y="ICE",
        color="Periodo",
        title="Comparación real del ICE entre 2022 y 2025"
    )

    st.plotly_chart(fig_ice, use_container_width=True)

    st.divider()

    # ==============================
    # DISTRIBUCIÓN DE CLASES
    # ==============================

    st.subheader("📊 Distribución de Clases por Año")

    conteo_clases = (
        df_real
        .groupby(["Periodo", "Clase"])
        .size()
        .reset_index(name="Cantidad")
    )

    fig_clases = px.bar(
        conteo_clases,
        x="Clase",
        y="Cantidad",
        color="Periodo",
        barmode="group",
        title="Distribución de clases de conectividad por año"
    )

    st.plotly_chart(fig_clases, use_container_width=True)

    st.divider()

    # ==============================
    # SIMULACIÓN FUTURA
    # ==============================

    st.subheader("Simulación Prospectiva 2026–2030")

    st.write("""
    La simulación futura se calcula a partir de la tasa de cambio anual observada entre 2022 y 2025.
    No representa una predicción exacta, sino una proyección de escenario basada en tendencia.
    """)

    anio_futuro = st.selectbox(
        "Seleccione año futuro",
        [2026, 2027, 2028, 2029, 2030]
    )

    escenario = st.selectbox(
        "Seleccione escenario",
        [
            "Conservación",
            "Tendencial",
            "Urbanización"
        ]
    )

    # Cambio anual observado entre 2022 y 2025
    tasa_ndvi = cambio_ndvi / 3
    tasa_ice = cambio_ice / 3

    # Años desde 2025
    delta_anios = anio_futuro - 2025

    if escenario == "Conservación":
        factor = 0.5

    elif escenario == "Tendencial":
        factor = 1.0

    else:
        factor = 1.5

    ndvi_futuro = ndvi_2025 + (tasa_ndvi * delta_anios * factor)
    ice_futuro = ice_2025 + (tasa_ice * delta_anios * factor)

    col1, col2 = st.columns(2)

    col1.metric(
        f"NDVI estimado {anio_futuro}",
        f"{ndvi_futuro:.3f}",
        f"{ndvi_futuro - ndvi_2025:.3f}"
    )

    col2.metric(
        f"ICE estimado {anio_futuro}",
        f"{ice_futuro:.3f}",
        f"{ice_futuro - ice_2025:.3f}"
    )

    # ==============================
    # GRÁFICO DE TENDENCIA
    # ==============================

    df_tendencia = pd.DataFrame({
        "Año": [2022, 2025, anio_futuro],
        "NDVI": [ndvi_2022, ndvi_2025, ndvi_futuro],
        "ICE": [ice_2022, ice_2025, ice_futuro]
    })

    st.subheader("📈 Tendencia Temporal NDVI e ICE")

    fig_tendencia = px.line(
        df_tendencia,
        x="Año",
        y=["NDVI", "ICE"],
        markers=True,
        title="Tendencia observada y simulación prospectiva"
    )

    st.plotly_chart(fig_tendencia, use_container_width=True)

    st.divider()

    # ==============================
    # INTERPRETACIÓN AUTOMÁTICA
    # ==============================

    if cambio_ndvi < 0:
        interpretacion_ndvi = "una disminución en la cobertura vegetal"
    else:
        interpretacion_ndvi = "una mejora en la cobertura vegetal"

    if cambio_ice < 0:
        interpretacion_ice = "una pérdida de conectividad ecológica"
    else:
        interpretacion_ice = "una mejora en la conectividad ecológica"

    st.success(f"""
    ### Interpretación del análisis temporal

    Entre 2022 y 2025, el NDVI promedio cambió de **{ndvi_2022:.3f}** a **{ndvi_2025:.3f}**,
    lo que representa **{interpretacion_ndvi}**.

    El ICE promedio cambió de **{ice_2022:.3f}** a **{ice_2025:.3f}**,
    indicando **{interpretacion_ice}**.

    Para el año **{anio_futuro}**, bajo el escenario **{escenario}**, se estima un NDVI de
    **{ndvi_futuro:.3f}** y un ICE de **{ice_futuro:.3f}**.

    Esta simulación permite explorar posibles escenarios futuros del corredor
    Ciudad del Saber – Camino de Cruces – Cerro Ancón a partir de la tendencia observada
    en imágenes Sentinel-2 reales.
    """)