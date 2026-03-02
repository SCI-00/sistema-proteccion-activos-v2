"""
Dashboard Sistema de Protección de Activos - Conectado a API
"""
import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Configuración
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="Sistema de Protección de Activos",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .big-metric {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .status-green { color: #2ecc71; }
    .status-yellow { color: #f39c12; }
    .status-red { color: #e74c3c; }
</style>
""", unsafe_allow_html=True)

# Funciones de API
def login(email: str, password: str):
    try:
        response = requests.post(
            f"{
