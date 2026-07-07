import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📆 Análisis Temporal de Conectividad")

st.write("""
Comparación del estado de la vegetación en diferentes momentos
usando NDVI y ICE.
""")

# =========================
# SIMULACIÓN DE 2 FECHAS
# =========================

df1 = pd.read_csv("Datos/dataset_clasificado.csv")
df2 = df1.copy()

# simulamos cambio (DEFORESTACIÓN ligera)
df2["NDVI"] = df2["NDVI"] * 0.85
df2["ICE"] = df2["ICE"] * 0.80

df1["Fecha"] = "Antes"
df2["Fecha"] = "Después"

df_total = pd.concat([df1, df2])

# =========================
# GRÁFICO CAMBIO NDVI
# =========================

st.subheader("📉 Cambio en NDVI")

fig = px.box(
    df_total,
    x="Fecha",
    y="NDVI",
    color="Fecha"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# GRÁFICO CAMBIO ICE
# =========================

st.subheader("📉 Cambio en ICE")

fig2 = px.box(
    df_total,
    x="Fecha",
    y="ICE",
    color="Fecha"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# INDICADOR DE CAMBIO
# =========================

st.subheader("📊 Resumen de Cambio")

col1, col2 = st.columns(2)

col1.metric(
    "Cambio NDVI",
    f"{df2['NDVI'].mean() - df1['NDVI'].mean():.3f}"
)

col2.metric(
    "Cambio ICE",
    f"{df2['ICE'].mean() - df1['ICE'].mean():.3f}"
)