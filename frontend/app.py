"""
Dashboard Sistema de Protección de Activos
"""
import streamlit as st
import requests
import os
from datetime import datetime

# Configuración
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="Sistema de Protección de Activos",
    page_icon="🔒",
    layout="wide"
)

# Funciones de API
def login(email: str, password: str):
    """Login de usuario"""
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

def get_user_info(token: str):
    """Obtener información del usuario"""
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
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
        st.caption(f"Sistema desarrollado para Victor Manuel De La Torre")
        st.caption(f"Gerente de Protección de Activos - Zona Sureste")

# Página principal (dashboard)
def show_dashboard():
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.title("🔒 Protección de Activos")
        st.markdown("---")
        st.write(f"👤 **{user['nombre']}**")
        st.write(f"📧 {user['email']}")
        st.write(f"🎭 Rol: {user['rol']}")
        st.markdown("---")
        
        menu = st.selectbox(
            "📋 Menú",
            ["📊 Dashboard", "🏢 CEDIS", "👥 Usuarios", "📈 Reportes", "⚙️ Configuración"]
        )
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    # Contenido principal
    if menu == "📊 Dashboard":
        st.title("📊 Dashboard Principal")
        st.subheader(f"Bienvenido, {user['nombre']}")
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏢 CEDIS Totales", "20", "+2")
        
        with col2:
            st.metric("✅ CEDIS Activos", "18", "90%")
        
        with col3:
            st.metric("👥 Usuarios", "45", "+5")
        
        with col4:
            st.metric("🔐 Nivel Seguridad", "Alta", "▲")
        
        st.markdown("---")
        
        # Información de zona
        st.subheader("📍 Zona Sureste")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Estados bajo supervisión:**
            - 🌴 Campeche
            - 🏝️ Quintana Roo  
            - 🌊 Tabasco
            - 🌄 Chiapas
            - 🎭 Oaxaca
            - 🏛️ Yucatán
            """)
        
        with col2:
            st.success("""
            **Pilares de protección:**
            - 🔒 Seguridad Patrimonial
            - 🚨 Protección Civil
            - 👷 Seguridad y Salud en el Trabajo (SST)
            """)
        
        st.markdown("---")
        st.write(f"🕐 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    elif menu == "🏢 CEDIS":
        st.title("🏢 Gestión de CEDIS")
        st.info("Módulo de CEDIS en desarrollo")
    
    elif menu == "👥 Usuarios":
        st.title("👥 Gestión de Usuarios")
        st.info("Módulo de usuarios en desarrollo")
    
    elif menu == "📈 Reportes":
        st.title("📈 Reportes y Análisis")
        st.info("Módulo de reportes en desarrollo")
    
    elif menu == "⚙️ Configuración":
        st.title("⚙️ Configuración")
        st.info("Módulo de configuración en desarrollo")

# Main
def main():
    if st.session_state.token is None:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
