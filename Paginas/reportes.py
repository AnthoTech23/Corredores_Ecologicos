import os
import json
from datetime import datetime

import streamlit as st
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from Utils.cargar_datos import cargar_dataset


def crear_pdf():

    os.makedirs("Reportes", exist_ok=True)

    archivo_pdf = "Reportes/Informe_Ejecutivo_EcoConnect.pdf"

    df = cargar_dataset()

    df_2022 = pd.read_csv("Datos/dataset_2022_clasificado.csv")
    df_2025 = pd.read_csv("Datos/dataset_2025_clasificado.csv")

    with open("Modelos/metricas.json", "r") as f:
        metricas = json.load(f)

    ndvi = df["NDVI"].mean()
    ndwi = df["NDWI"].mean()
    ndbi = df["NDBI"].mean()
    ice = df["ICE"].mean()

    ndvi_2022 = df_2022["NDVI"].mean()
    ndvi_2025 = df_2025["NDVI"].mean()

    ice_2022 = df_2022["ICE"].mean()
    ice_2025 = df_2025["ICE"].mean()

    doc = SimpleDocTemplate(archivo_pdf)
    styles = getSampleStyleSheet()
    contenido = []

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    contenido.append(Paragraph("EcoConnect Panamá", styles["Title"]))
    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph(
        "Informe Ejecutivo de Conectividad Ecológica",
        styles["Heading2"]
    ))

    contenido.append(Paragraph(
        "Corredor Ciudad del Saber – Camino de Cruces – Cerro Ancón",
        styles["Normal"]
    ))

    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph(f"Fecha de generación: {fecha}", styles["Normal"]))
    contenido.append(Spacer(1, 20))

    contenido.append(Paragraph("1. Resumen Ejecutivo", styles["Heading2"]))

    resumen = """
    Este informe presenta los resultados del análisis de conectividad ecológica
    desarrollado mediante imágenes Sentinel-2, índices ambientales y un modelo
    de Machine Learning basado en Random Forest. La plataforma permite evaluar
    la cobertura vegetal, la humedad, la urbanización y la conectividad ecológica
    del corredor estudiado.
    """

    contenido.append(Paragraph(resumen, styles["Normal"]))
    contenido.append(Spacer(1, 15))

    contenido.append(Paragraph("2. Indicadores Ambientales", styles["Heading2"]))

    tabla_indicadores = [
        ["Indicador", "Valor"],
        ["NDVI promedio", f"{ndvi:.3f}"],
        ["NDWI promedio", f"{ndwi:.3f}"],
        ["NDBI promedio", f"{ndbi:.3f}"],
        ["ICE promedio", f"{ice:.3f}"],
        ["Registros analizados", f"{len(df):,}"]
    ]

    tabla = Table(tabla_indicadores)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    contenido.append(tabla)
    contenido.append(Spacer(1, 20))

    contenido.append(Paragraph("3. Resultados del Modelo Random Forest", styles["Heading2"]))

    tabla_modelo = [
        ["Métrica", "Valor"],
        ["Accuracy", f"{metricas['Accuracy'] * 100:.2f}%"],
        ["Precision", f"{metricas['Precision'] * 100:.2f}%"],
        ["Recall", f"{metricas['Recall'] * 100:.2f}%"],
        ["F1 Score", f"{metricas['F1'] * 100:.2f}%"]
    ]

    tabla_ml = Table(tabla_modelo)
    tabla_ml.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    contenido.append(tabla_ml)
    contenido.append(Spacer(1, 20))

    if os.path.exists("Modelos/matriz_confusion.png"):
        contenido.append(Paragraph("Matriz de Confusión", styles["Heading3"]))
        contenido.append(Image("Modelos/matriz_confusion.png", width=350, height=280))
        contenido.append(Spacer(1, 15))

    if os.path.exists("Modelos/importancia_variables.png"):
        contenido.append(Paragraph("Importancia de Variables", styles["Heading3"]))
        contenido.append(Image("Modelos/importancia_variables.png", width=400, height=260))
        contenido.append(Spacer(1, 15))

    contenido.append(Paragraph("4. Análisis Temporal", styles["Heading2"]))

    tabla_temporal = [
        ["Año", "NDVI promedio", "ICE promedio"],
        ["2022", f"{ndvi_2022:.3f}", f"{ice_2022:.3f}"],
        ["2025", f"{ndvi_2025:.3f}", f"{ice_2025:.3f}"]
    ]

    tabla_temp = Table(tabla_temporal)
    tabla_temp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    contenido.append(tabla_temp)
    contenido.append(Spacer(1, 20))

    contenido.append(Paragraph("5. Conclusiones", styles["Heading2"]))

    conclusion = f"""
    El análisis permitió identificar el comportamiento de la conectividad ecológica
    del corredor estudiado. El NDVI promedio general fue de {ndvi:.3f}, mientras que
    el ICE promedio fue de {ice:.3f}. El modelo Random Forest obtuvo una precisión de
    {metricas['Accuracy'] * 100:.2f}%, demostrando un desempeño alto para clasificar
    los niveles de conectividad ecológica.
    """

    contenido.append(Paragraph(conclusion, styles["Normal"]))
    contenido.append(Spacer(1, 15))

    contenido.append(Paragraph("6. Recomendaciones", styles["Heading2"]))

    recomendaciones = """
    Se recomienda continuar el monitoreo anual mediante imágenes Sentinel-2,
    fortalecer la conservación de áreas verdes urbanas y priorizar acciones de
    restauración ecológica en sectores con baja conectividad.
    """

    contenido.append(Paragraph(recomendaciones, styles["Normal"]))

    doc.build(contenido)

    return archivo_pdf


def crear_excel():

    os.makedirs("Reportes", exist_ok=True)

    archivo_excel = "Reportes/Datos_EcoConnect.xlsx"

    df = cargar_dataset()
    df_2022 = pd.read_csv("Datos/dataset_2022_clasificado.csv")
    df_2025 = pd.read_csv("Datos/dataset_2025_clasificado.csv")

    resumen = pd.DataFrame({
        "Indicador": [
            "NDVI promedio",
            "NDWI promedio",
            "NDBI promedio",
            "ICE promedio",
            "Registros"
        ],
        "Valor": [
            df["NDVI"].mean(),
            df["NDWI"].mean(),
            df["NDBI"].mean(),
            df["ICE"].mean(),
            len(df)
        ]
    })

    temporal = pd.DataFrame({
        "Año": [2022, 2025],
        "NDVI promedio": [
            df_2022["NDVI"].mean(),
            df_2025["NDVI"].mean()
        ],
        "ICE promedio": [
            df_2022["ICE"].mean(),
            df_2025["ICE"].mean()
        ]
    })

    clases = (
        df["Clase"]
        .value_counts()
        .reset_index()
    )

    clases.columns = ["Clase", "Cantidad"]

    with pd.ExcelWriter(archivo_excel, engine="openpyxl") as writer:
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
        clases.to_excel(writer, sheet_name="Clases", index=False)
        temporal.to_excel(writer, sheet_name="Temporal", index=False)
        df.head(5000).to_excel(writer, sheet_name="Muestra_Datos", index=False)

    return archivo_excel


def mostrar_reportes():

    st.title("📄 Reportes")

    st.write("""
    En esta sección se pueden generar reportes automáticos del análisis de conectividad
    ecológica. El informe PDF resume los resultados principales del proyecto, mientras
    que el archivo Excel permite exportar los datos para análisis posterior.
    """)

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("📄 Informe Ejecutivo PDF")

        st.write("""
        Genera un documento con resumen ejecutivo, indicadores ambientales,
        resultados del modelo Random Forest, análisis temporal, conclusiones
        y recomendaciones.
        """)

        if st.button("Generar PDF", use_container_width=True):

            archivo_pdf = crear_pdf()

            with open(archivo_pdf, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar Informe PDF",
                    data=f,
                    file_name="Informe_Ejecutivo_EcoConnect.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    with c2:

        st.subheader("📊 Exportar Datos Excel")

        st.write("""
        Exporta un archivo Excel con indicadores, distribución de clases,
        resultados temporales y una muestra del dataset procesado.
        """)

        if st.button("Generar Excel", use_container_width=True):

            archivo_excel = crear_excel()

            with open(archivo_excel, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar Excel",
                    data=f,
                    file_name="Datos_EcoConnect.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )


# Esta función queda por compatibilidad con tu app2.py actual
def generar_pdf():
    mostrar_reportes()