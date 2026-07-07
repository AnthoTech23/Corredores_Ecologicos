import streamlit as st
import plotly.express as px
import numpy as np
import folium

from folium.raster_layers import ImageOverlay
from folium.plugins import MiniMap, Fullscreen, MeasureControl, MousePosition, HeatMap
from streamlit_folium import st_folium

from Utils.cargar_datos import cargar_dataset


def asignar_coordenadas_grid(df_mapa):
    """
    Crea coordenadas simuladas tipo rejilla dentro del área de estudio.
    Esto permite visualizar los píxeles clasificados aunque el CSV no tenga lat/lon.
    """

    n = len(df_mapa)

    if n == 0:
        return df_mapa

    side = int(np.ceil(np.sqrt(n)))

    lats = np.linspace(8.951097018056902, 9.016704235652181, side)
    lons = np.linspace(-79.59576997725952, -79.53876008054836, side)

    lat_grid = np.repeat(lats, side)[:n]
    lon_grid = np.tile(lons, side)[:n]

    df_mapa = df_mapa.copy()
    df_mapa["lat"] = lat_grid
    df_mapa["lon"] = lon_grid

    return df_mapa


def color_clase(clase):
    if clase == 2:
        return "green"
    elif clase == 1:
        return "orange"
    else:
        return "red"


def texto_clase(clase):
    if clase == 2:
        return "Alta conectividad"
    elif clase == 1:
        return "Conectividad media"
    else:
        return "Baja conectividad"


def mostrar_ambiental():

    # ==========================================
    # CARGA DE DATOS
    # ==========================================

    df_original = cargar_dataset()

    st.title("🌿 Análisis Ambiental")

    st.write("""
    En esta sección se presentan los indicadores ambientales obtenidos a partir de imágenes
    Sentinel-2 procesadas en Google Earth Engine. Además, se visualiza la conectividad
    ecológica mediante un mapa interactivo, un heatmap y un mapa de riesgo ecológico.
    """)

    st.divider()

    # ==========================================
    # FILTROS
    # ==========================================

    st.sidebar.markdown("## 🎛️ Filtros")

    clases = st.sidebar.multiselect(
        "Clase de conectividad",
        options=[0, 1, 2],
        default=[0, 1, 2]
    )

    ndvi_min, ndvi_max = st.sidebar.slider(
        "Rango NDVI",
        float(df_original["NDVI"].min()),
        float(df_original["NDVI"].max()),
        (
            float(df_original["NDVI"].min()),
            float(df_original["NDVI"].max())
        )
    )

    ice_min, ice_max = st.sidebar.slider(
        "Rango ICE",
        float(df_original["ICE"].min()),
        float(df_original["ICE"].max()),
        (
            float(df_original["ICE"].min()),
            float(df_original["ICE"].max())
        )
    )

    df = df_original[
        (df_original["Clase"].isin(clases)) &
        (df_original["NDVI"] >= ndvi_min) &
        (df_original["NDVI"] <= ndvi_max) &
        (df_original["ICE"] >= ice_min) &
        (df_original["ICE"] <= ice_max)
    ].copy()

    if len(df) == 0:
        st.warning("No hay datos disponibles con los filtros seleccionados.")
        return

    # ==========================================
    # INDICADORES
    # ==========================================

    st.subheader("📊 Indicadores Ambientales")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("NDVI Promedio", f"{df['NDVI'].mean():.3f}")
    c2.metric("ICE Promedio", f"{df['ICE'].mean():.3f}")
    c3.metric("Registros", f"{len(df):,}")
    c4.metric("Clases", df["Clase"].nunique())

    st.divider()

    # ==========================================
    # ESTADÍSTICAS
    # ==========================================

    st.subheader("📈 Estadísticas Generales")

    a, b, c = st.columns(3)

    a.info(f"""
    **NDVI máximo**

    {df['NDVI'].max():.3f}
    """)

    b.info(f"""
    **ICE máximo**

    {df['ICE'].max():.3f}
    """)

    c.info(f"""
    **NDBI promedio**

    {df['NDBI'].mean():.3f}
    """)

    st.divider()

    # ==========================================
    # GRÁFICO 1
    # ==========================================

    st.subheader("📊 Distribución de Clases")

    conteo = df["Clase"].value_counts().reset_index()
    conteo.columns = ["Clase", "Cantidad"]

    fig_clases = px.bar(
        conteo,
        x="Clase",
        y="Cantidad",
        color="Clase",
        text="Cantidad",
        title="Cantidad de píxeles por clase de conectividad"
    )

    fig_clases.update_layout(
        height=450,
        xaxis_title="Clase",
        yaxis_title="Cantidad"
    )

    st.plotly_chart(fig_clases, use_container_width=True)

    # ==========================================
    # GRÁFICO 2
    # ==========================================

    st.subheader("📈 Relación NDVI vs ICE")

    muestra = df.sample(
        min(5000, len(df)),
        random_state=42
    )

    fig_scatter = px.scatter(
        muestra,
        x="NDVI",
        y="ICE",
        color="Clase",
        opacity=0.6,
        title="Relación entre cobertura vegetal y conectividad ecológica"
    )

    fig_scatter.update_layout(
        height=550,
        xaxis_title="NDVI",
        yaxis_title="ICE"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # ==========================================
    # MAPA INTERACTIVO
    # ==========================================

    st.subheader("🗺️ Mapa de Conectividad y Riesgo Ecológico")

    st.info("""
    El mapa muestra el raster del Índice de Conectividad Ecológica (ICE), un heatmap
    de conectividad y una muestra de puntos clasificados por el modelo Random Forest.
    Para evitar sobrecargar el navegador, se utiliza una muestra representativa de los datos.
    """)

    mapa = folium.Map(
        location=[8.984, -79.565],
        zoom_start=13,
        control_scale=True,
        tiles=None
    )

    # Capas base
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(mapa)
    folium.TileLayer("CartoDB positron", name="Mapa claro").add_to(mapa)
    folium.TileLayer("CartoDB dark_matter", name="Mapa oscuro").add_to(mapa)

    # Raster ICE
    ImageOverlay(
        image="Dashboard/temp/ice.png",
        bounds=[
            [8.951097018056902, -79.59576997725952],
            [9.016704235652181, -79.53876008054836]
        ],
        opacity=0.65,
        name="Raster ICE"
    ).add_to(mapa)

    # ==========================================
    # HEATMAP
    # ==========================================

    heat_sample = df.sample(
        min(5000, len(df)),
        random_state=10
    ).copy()

    heat_sample = asignar_coordenadas_grid(heat_sample)

    ice_min_h = heat_sample["ICE"].min()
    ice_max_h = heat_sample["ICE"].max()

    if ice_max_h != ice_min_h:
        heat_sample["ICE_norm"] = (
            (heat_sample["ICE"] - ice_min_h) /
            (ice_max_h - ice_min_h)
        )
    else:
        heat_sample["ICE_norm"] = 0.5

    heat_points = heat_sample[["lat", "lon", "ICE_norm"]].values.tolist()

    HeatMap(
        heat_points,
        radius=16,
        blur=22,
        min_opacity=0.25,
        name="Heatmap de conectividad",
        gradient={
            0.2: "red",
            0.5: "yellow",
            0.8: "orange",
            1.0: "green"
        }
    ).add_to(mapa)

   

    # ==========================================
    # MARCADORES DEL ÁREA DE ESTUDIO
    # ==========================================

    folium.Marker(
        [9.00038, -79.58359],
        popup="<b>Ciudad del Saber</b><br>Zona urbana con infraestructura verde.",
        tooltip="Ciudad del Saber",
        icon=folium.Icon(color="green", icon="tree", prefix="fa")
    ).add_to(mapa)

    folium.Marker(
        [9.01174, -79.54565],
        popup="<b>Camino de Cruces</b><br>Área boscosa y protegida.",
        tooltip="Camino de Cruces",
        icon=folium.Icon(color="darkgreen", icon="leaf", prefix="fa")
    ).add_to(mapa)

    folium.Marker(
        [8.95723, -79.54926],
        popup="<b>Cerro Ancón</b><br>Zona de importancia ecológica.",
        tooltip="Cerro Ancón",
        icon=folium.Icon(color="red", icon="mountain", prefix="fa")
    ).add_to(mapa)

    # ==========================================
    # CONTROLES
    # ==========================================

    MiniMap(toggle_display=True).add_to(mapa)
    Fullscreen().add_to(mapa)
    MeasureControl().add_to(mapa)
    MousePosition().add_to(mapa)
    folium.LayerControl(collapsed=False).add_to(mapa)

    # ==========================================
    # RENDER FINAL
    # ==========================================

    datos_mapa = st_folium(
        mapa,
        height=650,
        use_container_width=True
    )

    if datos_mapa and datos_mapa.get("last_clicked"):
        st.success(f"""
        📍 Coordenadas seleccionadas

        Latitud: {datos_mapa["last_clicked"]["lat"]:.6f}

        Longitud: {datos_mapa["last_clicked"]["lng"]:.6f}
        """)

    # ==========================================
    # LEYENDA
    # ==========================================

    st.markdown("""
    ### 🎨 Leyenda

    🟢 **Clase 2:** Alta conectividad ecológica  
    🟠 **Clase 1:** Conectividad media  
    🔴 **Clase 0:** Baja conectividad ecológica  

    El heatmap representa la intensidad relativa del Índice de Conectividad Ecológica (ICE).
    """)

    st.success("""
    ### 🌿 Interpretación

    Las zonas con mayor intensidad verde representan sectores con mejores condiciones de conectividad ecológica.
    Las zonas rojas y naranjas indican áreas con menor conectividad o mayor presión urbana.
    Este mapa permite identificar sectores prioritarios para conservación, restauración ecológica o planificación ambiental.
    """)