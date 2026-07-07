import streamlit as st


def cargar_estilos():

    st.markdown("""
    <style>
    
    
    /* ===================================================== */
    /* ENCABEZADO SUPERIOR TRABAJADO */
    /* ===================================================== */

    .app-header {
        background: linear-gradient(90deg, #E8F5E9, #FFFFFF);
        padding: 28px 35px;
        border-radius: 22px;
        margin-bottom: 22px;
        text-align: center;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
        border: 1px solid #D8EAD8;
    }

    .app-title {
        font-size: 44px;
        font-weight: 900;
        color: #1B4332;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .app-subtitle {
        font-size: 20px;
        font-weight: 600;
        color: #2D6A4F;
        margin-top: 4px;
    }

    .app-location {
        font-size: 16px;
        font-weight: 500;
        color: #4F772D;
        margin-top: 12px;
    }

    .top-navbar{
        width:100%;
        background:white;
        padding:18px 28px;
        border-radius:0px 0px 16px 16px;
        box-shadow:0px 4px 15px rgba(0,0,0,0.10);
        margin-bottom:15px;
        display:flex;
        align-items:center;
    }

    .brand{
        font-size:24px;
        font-weight:800;
        color:#1B4332;
        display:flex;
        align-items:center;
        gap:10px;
    }

    div[role="radiogroup"]{
        margin: 0 0 45px auto;
        background: white;
        padding: 14px 22px;
        border-radius: 18px;
        box-shadow: 0px 5px 16px rgba(0,0,0,0.09);
        display: flex;
        justify-content: center;
        gap: 18px;
        margin-bottom: 24px;
        flex-wrap: wrap;
        border: 1px solid #DDEBDD;
    }

    div[role="radiogroup"] label{
        font-size: 16px;
        font-weight: 700;
        color: #1B4332;
        padding: 10px 16px;
        border-radius: 12px;
        transition: 0.3s ease;
    }

    div[role="radiogroup"] label:hover{
        background:#E8F5E9;
        cursor:pointer;
    }

    </style>
    """, unsafe_allow_html=True)

