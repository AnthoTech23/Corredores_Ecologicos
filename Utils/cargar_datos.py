import pandas as pd
import streamlit as st


@st.cache_data
def cargar_dataset():

    return pd.read_csv(
        "Datos/dataset_clasificado.csv"
    )