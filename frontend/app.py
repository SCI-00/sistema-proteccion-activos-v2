"""
Dashboard Sistema de Protección de Activos - Mejorado
"""
import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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

# Datos de CEDIS Zona Sureste
CEDIS_DATA = [
    {"id": 1, "nombre": "CEDIS Cancún", "estado": "Quintana Roo", "ciudad": "Cancún", "score": 95},
    {"id": 2, "nombre": "CEDIS Playa del Carmen", "estado": "Quintana Roo", "ciudad": "Playa del Carmen", "score": 92},
    {"id": 3, "nombre": "CEDIS Chetumal", "estado": "Quintana Roo", "ciudad": "Chetumal", "score": 88},
    {"id": 4, "nombre": "CEDIS Mérida Norte", "estado": "Yucatán", "ciudad": "Mérida", "score": 94},
    {"id": 5, "nombre": "CEDIS Mérida Sur", "estado": "Yucatán", "ciudad": "Mérida", "score": 91},
    {"id": 6, "nombre": "CEDIS Valladolid", "estado": "Yucatán", "ciudad": "Valladolid", "score": 87},
    {"id": 7, "nombre": "CEDIS Campeche", "estado": "Campeche", "ciudad": "Campeche", "score": 90},
    {"id": 8, "nombre": "CEDIS Ciudad del Carmen", "estado": "Campeche", "ciudad": "Ciudad del Carmen", "score": 86},
    {"id": 9, "nombre": "CEDIS Villahermosa Centro", "estado": "Tabasco", "ciudad": "Villahermosa", "score": 93},
    {"id": 10, "nombre": "CEDIS Villahermosa Norte", "estado": "Tabasco", "ciudad": "Villahermosa", "score": 89},
    {"id": 11, "nombre": "CEDIS Cárdenas", "estado": "Tabasco", "ciudad": "Cárdenas", "score": 85},
    {"id": 12, "nombre": "CEDIS Tuxtla Gutiérrez", "estado": "Chiapas", "ciudad": "Tuxtla Gutiérrez", "score": 92},
    {"id": 13, "nombre": "CEDIS Tapachula", "estado": "Chiapas", "ciudad": "Tapachula", "score": 88},
    {"id": 14, "nombre": "CEDIS San Cristóbal", "estado": "Chiapas", "ciudad": "San Cristóbal de las Casas", "score": 84},
    {"id": 15, "nombre": "CEDIS Comitán", "estado": "Chiapas", "ciudad": "Comitán", "score": 83},
    {"id": 16, "nombre": "CEDIS Oaxaca Centro", "estado": "Oaxaca", "ciudad": "Oaxaca", "score": 91},
    {"id": 17, "nombre": "CEDIS Salina Cruz", "estado": "Oaxaca", "ciudad": "Salina Cruz", "score": 87},
    {"id": 18, "nombre": "CEDIS Juchitán", "estado": "Oaxaca", "ciudad": "Juchitán", "score": 85},
    {"id": 19, "nombre": "CEDIS Huatulco", "estado": "Oaxaca", "ciudad": "Huatulco", "score": 89},
    {"id": 20, "nombre": "CEDIS Puerto Escondido", "estado": "Oaxaca", "ciudad": "Puerto Escondido", "score": 86}
]

# Funciones de API
def login(email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

# Estado de sesión
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Página de login
def show_login():
    st.title("🔒 Sistema de Protección de Activos")
    st.subheader("SCI DE OCCIDENTE & Omnilife México")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        st.subheader("🔐 Iniciar Sesión")
        
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Contraseña", type="password", key="login_password")
        
        if st.button("Iniciar Sesión", type="primary", use_container_width=True):
            if email and password:
                with st.spinner("Verificando credenciales..."):
                    result = login(email, password)
                    if result:
                        st.session_state.token = result["access_token"]
                        st.session_state.user = result["user"]
                        st.success("✅ Login exitoso")
                        st.rerun()
                    else:
                        st.error("❌ Email o contraseña incorrectos")
            else:
                st.warning("Por favor ingresa email y contraseña")
        
        st.markdown("---")
        st.caption("Sistema desarrollado para Victor Manuel De La Torre")
        st.caption("Gerente de Protección de Activos - Zona Sureste")

# Página principal (dashboard)
def show_dashboard():
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.title("🔒 Protección de Activos")
        st.markdown("---")
        st.write(f"👤 **{user['nombre']}**")
        st.write(f"📧 {user['email']}")
        st.write(f"🎭 {user['rol']}")
        st.markdown("---")
        
        menu = st.selectbox(
            "📋 Menú Principal",
            ["📊 Dashboard General", "🏢 Gestión de CEDIS", "📈 Scorecards", "💰 Presupuestos", "📑 Reportes", "⚙️ Configuración"]
        )
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    # Contenido principal
    if menu == "📊 Dashboard General":
        show_dashboard_general()
    elif menu == "🏢 Gestión de CEDIS":
        show_cedis_management()
    elif menu == "📈 Scorecards":
        show_scorecards()
    elif menu == "💰 Presupuestos":
        show_presupuestos()
    elif menu == "📑 Reportes":
        show_reportes()
    elif menu == "⚙️ Configuración":
        show_configuracion()

def show_dashboard_general():
    st.title("📊 Dashboard General")
    st.subheader(f"Bienvenido, {st.session_state.user['nombre']}")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏢 CEDIS Totales", "20", "Zona Sureste")
    
    with col2:
        avg_score = sum([c["score"] for c in CEDIS_DATA]) / len(CEDIS_DATA)
        st.metric("📊 Score Promedio", f"{avg_score:.1f}%", "+2.3%")
    
    with col3:
        activos = len([c for c in CEDIS_DATA if c["score"] >= 85])
        st.metric("✅ CEDIS Óptimos", f"{activos}", f"{(activos/20)*100:.0f}%")
    
    with col4:
        st.metric("🔐 Nivel General", "Alto", "▲")
    
    st.markdown("---")
    
    # Gráfica de scores por estado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Scores por Estado")
        df = pd.DataFrame(CEDIS_DATA)
        avg_by_state = df.groupby("estado")["score"].mean().reset_index()
        avg_by_state = avg_by_state.sort_values("score", ascending=False)
        
        fig = px.bar(
            avg_by_state,
            x="estado",
            y="score",
            color="score",
            color_continuous_scale="RdYlGn",
            range_color=[80, 100]
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Distribución de Scores")
        bins = ["80-84", "85-89", "90-94", "95-100"]
        counts = [
            len([c for c in CEDIS_DATA if 80 <= c["score"] < 85]),
            len([c for c in CEDIS_DATA if 85 <= c["score"] < 90]),
            len([c for c in CEDIS_DATA if 90 <= c["score"] < 95]),
            len([c for c in CEDIS_DATA if 95 <= c["score"] <= 100])
        ]
        
        fig = go.Figure(data=[go.Pie(labels=bins, values=counts, hole=.3)])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Zona Sureste
    st.markdown("---")
    st.subheader("📍 Zona Sureste - Cobertura")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Estados bajo supervisión:**
        - 🌴 Campeche (2 CEDIS)
        - 🏝️ Quintana Roo (3 CEDIS)
        - 🌊 Tabasco (3 CEDIS)
        - 🌄 Chiapas (4 CEDIS)
        - 🎭 Oaxaca (5 CEDIS)
        - 🏛️ Yucatán (3 CEDIS)
        """)
    
    with col2:
        st.success("""
        **Pilares de protección:**
        - 🔒 Seguridad Patrimonial
        - 🚨 Protección Civil
        - 👷 Seguridad y Salud (SST)
        """)
    
    with col3:
        st.warning("""
        **Próximas acciones:**
        - Auditoría CEDIS Comitán
        - Capacitación SST Tabasco
        - Actualización protocolos
        """)

def show_cedis_management():
    st.title("🏢 Gestión de CEDIS")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        estados = ["Todos"] + sorted(list(set([c["estado"] for c in CEDIS_DATA])))
        estado_filter = st.selectbox("Estado", estados)
    
    with col2:
        score_min = st.slider("Score Mínimo", 0, 100, 80)
    
    with col3:
        buscar = st.text_input("🔍 Buscar CEDIS")
    
    # Filtrar datos
    filtered_data = CEDIS_DATA.copy()
    
    if estado_filter != "Todos":
        filtered_data = [c for c in filtered_data if c["estado"] == estado_filter]
    
    filtered_data = [c for c in filtered_data if c["score"] >= score_min]
    
    if buscar:
        filtered_data = [c for c in filtered_data if buscar.lower() in c["nombre"].lower()]
    
    st.markdown(f"**Mostrando {len(filtered_data)} de {len(CEDIS_DATA)} CEDIS**")
    
    # Tabla de CEDIS
    df = pd.DataFrame(filtered_data)
    
    def color_score(val):
        if val >= 90:
            return 'background-color: #d4edda'
        elif val >= 85:
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #f8d7da'
    
    st.dataframe(
        df.style.applymap(color_score, subset=['score']),
        use_container_width=True,
        height=600
    )

def show_scorecards():
    st.title("📈 Scorecards de Seguridad")
    
    cedis_seleccionado = st.selectbox(
        "Selecciona CEDIS",
        [c["nombre"] for c in CEDIS_DATA]
    )
    
    cedis = next(c for c in CEDIS_DATA if c["nombre"] == cedis_seleccionado)
    
    st.subheader(f"{cedis['nombre']} - {cedis['ciudad']}, {cedis['estado']}")
    
    # Scores por pilar
    col1, col2, col3 = st.columns(3)
    
    import random
    random.seed(cedis["id"])
    
    score_patrimonial = cedis["score"] + random.randint(-3, 3)
    score_civil = cedis["score"] + random.randint(-3, 3)
    score_sst = cedis["score"] + random.randint(-3, 3)
    
    with col1:
        st.metric("🔒 Seguridad Patrimonial", f"{score_patrimonial}%")
        st.progress(score_patrimonial / 100)
    
    with col2:
        st.metric("🚨 Protección Civil", f"{score_civil}%")
        st.progress(score_civil / 100)
    
    with col3:
        st.metric("👷 SST", f"{score_sst}%")
        st.progress(score_sst / 100)
    
    st.markdown("---")
    
    # Detalles por pilar
    tab1, tab2, tab3 = st.tabs(["🔒 Patrimonial", "🚨 Civil", "👷 SST"])
    
    with tab1:
        st.write("**Indicadores de Seguridad Patrimonial:**")
        st.write("- Control de accesos: ✅ Óptimo")
        st.write("- CCTV funcional: ✅ 100%")
        st.write("- Guardias activos: ✅ 24/7")
        st.write("- Alarmas: ✅ Operativas")
    
    with tab2:
        st.write("**Indicadores de Protección Civil:**")
        st.write("- Extintores vigentes: ✅ 100%")
        st.write("- Rutas de evacuación: ✅ Señalizadas")
        st.write("- Simulacros: ✅ Al día")
        st.write("- Brigadas: ✅ Capacitadas")
    
    with tab3:
        st.write("**Indicadores de SST:**")
        st.write("- Capacitaciones: ✅ Al corriente")
        st.write("- EPP disponible: ✅ 100%")
        st.write("- Comisión mixta: ✅ Activa")
        st.write("- NOM compliance: ✅ Cumplimiento")

def show_presupuestos():
    st.title("💰 Gestión de Presupuestos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Presupuesto Mensual", "$450,000 MXN")
        st.metric("Gastado Este Mes", "$387,250 MXN", "-14%")
    
    with col2:
        st.metric("Disponible", "$62,750 MXN")
        st.progress(387250 / 450000)
    
    st.markdown("---")
    
    # Gráfica de gastos
    categorias = ["Nómina Seguridad", "Mantenimiento", "Capacitación", "Equipamiento", "Otros"]
    gastos = [180000, 95000, 45000, 52250, 15000]
    
    fig = px.pie(names=categorias, values=gastos, title="Distribución de Gastos Febrero 2026")
    st.plotly_chart(fig, use_container_width=True)

def show_reportes():
    st.title("📑 Reportes y Análisis")
    
    tipo_reporte = st.selectbox(
        "Tipo de Reporte",
        ["Mensual Ejecutivo", "Por CEDIS", "Por Pilar", "Incidentes"]
    )
    
    if tipo_reporte == "Mensual Ejecutivo":
        st.subheader("📊 Reporte Ejecutivo - Febrero 2026")
        
        st.write("""
        **Resumen General:**
        - Total CEDIS operativos: 20/20 (100%)
        - Score promedio zona: 88.9%
        - Incidentes reportados: 3 (todos resueltos)
        - Capacitaciones realizadas: 45
        - Inversión en seguridad: $387,250 MXN
        
        **Highlights:**
        - ✅ CEDIS Cancún alcanzó score 95%
        - ✅ Cero accidentes laborales
        - ⚠️ CEDIS Comitán requiere auditoría
        """)
        
        if st.button("📥 Descargar PDF"):
            st.success("Reporte generado (funcionalidad próximamente)")

def show_configuracion():
    st.title("⚙️ Configuración")
    
    st.subheader("Perfil de Usuario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Nombre", value=st.session_state.user["nombre"])
        st.text_input("Email", value=st.session_state.user["email"])
    
    with col2:
        st.text_input("Rol", value=st.session_state.user["rol"], disabled=True)
        st.selectbox("Zona", ["Sureste"], disabled=True)
    
    if st.button("💾 Guardar Cambios"):
        st.success("Cambios guardados (funcionalidad próximamente)")

# Main
def main():
    if st.session_state.token is None:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
