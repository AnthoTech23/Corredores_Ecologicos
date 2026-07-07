import streamlit as st
import pandas as pd
import plotly.express as px
import json
import joblib

from sklearn.metrics import classification_report
from Utils.cargar_datos import cargar_dataset

def mostrar_machine_learning():

    st.title("Machine Learning")

    st.markdown("""
Esta sección presenta el modelo de Inteligencia Artificial desarrollado para clasificar
la conectividad ecológica del corredor urbano utilizando índices ambientales derivados
de imágenes Sentinel-2.
""")
    
    modelo = joblib.load("Modelos/modelo.pkl")

    with open("Modelos/metricas.json") as f:
        metricas = json.load(f)

    df = cargar_dataset()
    
    
    st.divider()

    st.subheader("📊 Rendimiento del Modelo")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Accuracy",
        f"{metricas['Accuracy']*100:.2f}%"
    )

    c2.metric(
        "Precision",
        f"{metricas['Precision']*100:.2f}%"
    )

    c3.metric(
        "Recall",
        f"{metricas['Recall']*100:.2f}%"
    )

    c4.metric(
        "F1 Score",
        f"{metricas['F1']*100:.2f}%"
    )
    
    st.divider()

    st.subheader("📌 Matriz de Confusión")

    st.image(
        "Modelos/matriz_confusion.png",
        use_container_width=True
    )
    
    st.divider()

    st.subheader("🌿 Importancia de las Variables")

    importancia = pd.read_csv(
        "Modelos/importancia_variables.csv"
    )

    fig = px.bar(

        importancia,

        x="Importancia",

        y="Variable",

        orientation="h",

        color="Importancia",

        text="Importancia",

        color_continuous_scale="Greens"

    )

    fig.update_layout(

        height=450,

        coloraxis_showscale=False

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    
    st.info("""
    ### Interpretación

    La importancia de variables muestra cuánto influye cada índice ambiental en la decisión del modelo.

    - 🌿 NDVI → Vegetación.
    - 💧 NDWI → Agua y humedad.
    - 🏙 NDBI → Urbanización.
    - 🌳 ICE → Conectividad ecológica.

    Las variables con mayor importancia son las que más contribuyen a la clasificación final.
    """)
    
    st.divider()

    st.subheader("📄 Reporte de Clasificación")

    X = df[["NDVI","NDWI","NDBI","ICE"]]

    y = df["Clase"]

    pred = modelo.predict(X)

    reporte = classification_report(

        y,

        pred,

        output_dict=True

    )

    tabla = pd.DataFrame(reporte).transpose()

    st.dataframe(
        tabla,
        use_container_width=True
    )
    
    st.success(f"""
    ### Conclusión

    El modelo Random Forest alcanzó una precisión de **{metricas['Accuracy']*100:.2f}%**, demostrando una alta capacidad para clasificar automáticamente la conectividad ecológica del área de estudio.

    Este desempeño confirma que los índices ambientales derivados de imágenes Sentinel-2 constituyen variables adecuadas para apoyar el monitoreo ambiental mediante técnicas de Inteligencia Artificial.
    """)