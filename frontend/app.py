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
            f"{API_URL}/auth/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

def get_cedis(token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/cedis/", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_cedis(token: str, data: dict):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_URL}/cedis/", headers=headers, json=data)
        return response.status_code == 201
    except:
        return False

def update_cedis(token: str, cedis_id: int, data: dict):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{API_URL}/cedis/{cedis_id}", headers=headers, json=data)
        return response.status_code == 200
    except:
        return False

def get_scorecards(token: str, cedis_id: int = None):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"cedis_id": cedis_id} if cedis_id else {}
        response = requests.get(f"{API_URL}/scorecards/", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_scorecard(token: str, data: dict):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_URL}/scorecards/", headers=headers, json=data)
        return response.status_code == 201
    except:
        return False

def get_presupuestos(token: str, cedis_id: int = None, periodo: str = None):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {}
        if cedis_id:
            params["cedis_id"] = cedis_id
        if periodo:
            params["periodo"] = periodo
        response = requests.get(f"{API_URL}/presupuestos/", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_presupuesto(token: str, data: dict):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_URL}/presupuestos/", headers=headers, json=data)
        return response.status_code == 201
    except:
        return False

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
    token = st.session_state.token
    
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
            ["📊 Dashboard General", "🏢 Gestión de CEDIS", "📈 Scorecards", "💰 Presupuestos", "⚙️ Configuración"]
        )
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    # Contenido principal
    if menu == "📊 Dashboard General":
        show_dashboard_general(token)
    elif menu == "🏢 Gestión de CEDIS":
        show_cedis_management(token)
    elif menu == "📈 Scorecards":
        show_scorecards_page(token)
    elif menu == "💰 Presupuestos":
        show_presupuestos_page(token)
    elif menu == "⚙️ Configuración":
        show_configuracion()

def show_dashboard_general(token):
    st.title("📊 Dashboard General")
    st.subheader(f"Bienvenido, {st.session_state.user['nombre']}")
    
    # Cargar CEDIS
    cedis_list = get_cedis(token)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏢 CEDIS Totales", len(cedis_list), "Zona Sureste")
    
    with col2:
        if cedis_list:
            avg_score = sum([c.get("score_general", 0) for c in cedis_list]) / len(cedis_list)
            st.metric("📊 Score Promedio", f"{avg_score:.1f}%")
        else:
            st.metric("📊 Score Promedio", "N/A")
    
    with col3:
        activos = len([c for c in cedis_list if c.get("activo", True)])
        st.metric("✅ CEDIS Activos", f"{activos}")
    
    with col4:
        st.metric("🔐 Nivel General", "Óptimo", "▲")
    
    st.markdown("---")
    
    if cedis_list:
        # Gráfica de CEDIS por estado
        df = pd.DataFrame(cedis_list)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 CEDIS por Estado")
            estado_count = df.groupby("estado").size().reset_index(name="cantidad")
            fig = px.bar(estado_count, x="estado", y="cantidad", color="cantidad")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Distribución por Ciudad")
            ciudad_count = df.groupby("ciudad").size().reset_index(name="cantidad")
            ciudad_count = ciudad_count.nlargest(10, "cantidad")
            fig = px.pie(ciudad_count, names="ciudad", values="cantidad")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👉 No hay CEDIS registrados. Ve a 'Gestión de CEDIS' para agregar uno.")

def show_cedis_management(token):
    st.title("🏢 Gestión de CEDIS")
    
    tab1, tab2 = st.tabs(["📋 Lista de CEDIS", "➕ Agregar CEDIS"])
    
    with tab1:
        cedis_list = get_cedis(token)
        
        if cedis_list:
            st.write(f"**Total: {len(cedis_list)} CEDIS**")
            
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                estados = ["Todos"] + sorted(list(set([c["estado"] for c in cedis_list])))
                estado_filter = st.selectbox("Filtrar por Estado", estados)
            
            # Aplicar filtro
            filtered = cedis_list
            if estado_filter != "Todos":
                filtered = [c for c in cedis_list if c["estado"] == estado_filter]
            
            # Mostrar tabla
            df = pd.DataFrame(filtered)
            st.dataframe(df, use_container_width=True, height=400)
            
            # Editar CEDIS
            st.markdown("---")
            st.subheader("✏️ Editar CEDIS")
            
            cedis_names = [f"{c['codigo']} - {c['nombre']}" for c in filtered]
            if cedis_names:
                selected = st.selectbox("Seleccionar CEDIS", cedis_names)
                selected_idx = cedis_names.index(selected)
                selected_cedis = filtered[selected_idx]
                
                with st.form("edit_cedis_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        score_patrimonial = st.number_input("Score Patrimonial", 0.0, 100.0, float(selected_cedis.get("score_patrimonial", 0)))
                        score_civil = st.number_input("Score Protección Civil", 0.0, 100.0, float(selected_cedis.get("score_civil", 0)))
                    
                    with col2:
                        score_sst = st.number_input("Score SST", 0.0, 100.0, float(selected_cedis.get("score_sst", 0)))
                        activo = st.checkbox("Activo", value=selected_cedis.get("activo", True))
                    
                    if st.form_submit_button("💾 Guardar Cambios", use_container_width=True):
                        score_general = (score_patrimonial + score_civil + score_sst) / 3
                        
                        update_data = {
                            "score_patrimonial": score_patrimonial,
                            "score_civil": score_civil,
                            "score_sst": score_sst,
                            "score_general": score_general,
                            "activo": activo
                        }
                        
                        if update_cedis(token, selected_cedis["id"], update_data):
                            st.success("✅ CEDIS actualizado exitosamente")
                            st.rerun()
                        else:
                            st.error("❌ Error al actualizar CEDIS")
        else:
            st.info("👉 No hay CEDIS registrados. Agrega uno en la pestaña 'Agregar CEDIS'.")
    
    with tab2:
        st.subheader("➕ Agregar Nuevo CEDIS")
        
        with st.form("add_cedis_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre del CEDIS *", placeholder="Ej: CEDIS Cancún")
                codigo = st.text_input("Código *", placeholder="Ej: CAN-001")
                estado = st.selectbox("Estado *", [
                    "Campeche", "Quintana Roo", "Tabasco", "Chiapas", "Oaxaca", "Yucatán"
                ])
                ciudad = st.text_input("Ciudad *", placeholder="Ej: Cancún")
            
            with col2:
                direccion = st.text_area("Dirección", placeholder="Dirección completa")
                responsable = st.text_input("Responsable", placeholder="Nombre del responsable")
                telefono = st.text_input("Teléfono", placeholder="999-123-4567")
                email = st.text_input("Email", placeholder="cedis@ejemplo.com")
            
            if st.form_submit_button("➕ Crear CEDIS", type="primary", use_container_width=True):
                if nombre and codigo and estado and ciudad:
                    new_cedis = {
                        "nombre": nombre,
                        "codigo": codigo,
                        "estado": estado,
                        "ciudad": ciudad,
                        "direccion": direccion or None,
                        "responsable": responsable or None,
                        "telefono": telefono or None,
                        "email": email or None
                    }
                    
                    if create_cedis(token, new_cedis):
                        st.success("✅ CEDIS creado exitosamente")
                        st.rerun()
                    else:
                        st.error("❌ Error al crear CEDIS. Verifica que el código no exista.")
                else:
                    st.warning("⚠️ Completa los campos obligatorios (*)")

def show_scorecards_page(token):
    st.title("📈 Scorecards de Seguridad")
    
    tab1, tab2 = st.tabs(["📋 Ver Scorecards", "➕ Registrar Evaluación"])
    
    with tab1:
        cedis_list = get_cedis(token)
        
        if cedis_list:
            cedis_names = ["Todos"] + [f"{c['codigo']} - {c['nombre']}" for c in cedis_list]
            selected = st.selectbox("Filtrar por CEDIS", cedis_names)
            
            cedis_id = None
            if selected != "Todos":
                idx = cedis_names.index(selected) - 1
                cedis_id = cedis_list[idx]["id"]
            
            scorecards = get_scorecards(token, cedis_id)
            
            if scorecards:
                df = pd.DataFrame(scorecards)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay scorecards registrados para este filtro.")
        else:
            st.warning("⚠️ Primero debes registrar CEDIS")
    
    with tab2:
        cedis_list = get_cedis(token)
        
        if cedis_list:
            with st.form("add_scorecard_form"):
                cedis_options = [f"{c['codigo']} - {c['nombre']}" for c in cedis_list]
                selected_cedis = st.selectbox("CEDIS *", cedis_options)
                
                tipo_pilar = st.selectbox("Pilar *", ["patrimonial", "civil", "sst"])
                periodo = st.text_input("Período *", placeholder="2026-03", value="2026-03")
                score_total = st.slider("Score Total", 0.0, 100.0, 85.0)
                
                observaciones = st.text_area("Observaciones")
                evaluador = st.text_input("Evaluador", value=st.session_state.user["nombre"])
                
                if st.form_submit_button("💾 Guardar Scorecard", type="primary", use_container_width=True):
                    idx = cedis_options.index(selected_cedis)
                    cedis_id = cedis_list[idx]["id"]
                    
                    new_scorecard = {
                        "cedis_id": cedis_id,
                        "tipo_pilar": tipo_pilar,
                        "periodo": periodo,
                        "score_total": score_total,
                        "observaciones": observaciones,
                        "evaluador": evaluador
                    }
                    
                    if create_scorecard(token, new_scorecard):
                        st.success("✅ Scorecard registrado exitosamente")
                        st.rerun()
                    else:
                        st.error("❌ Error al registrar scorecard")
        else:
            st.warning("⚠️ Primero debes registrar CEDIS")

def show_presupuestos_page(token):
    st.title("💰 Gestión de Presupuestos")
    
    tab1, tab2 = st.tabs(["📋 Ver Gastos", "➕ Registrar Gasto"])
    
    with tab1:
        periodo = st.text_input("Filtrar por Período", placeholder="2026-03", value="2026-03")
        
        presupuestos = get_presupuestos(token, periodo=periodo)
        
        if presupuestos:
            df = pd.DataFrame(presupuestos)
            
            # Resumen
            total = df["monto"].sum()
            st.metric("💰 Total del Período", f"${total:,.2f} MXN")
            
            # Gráfica por categoría
            cat_sum = df.groupby("categoria")["monto"].sum().reset_index()
            fig = px.pie(cat_sum, names="categoria", values="monto", title=f"Gastos por Categoría - {periodo}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay gastos registrados para este período.")
    
    with tab2:
        cedis_list = get_cedis(token)
        
        if cedis_list:
            with st.form("add_presupuesto_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    cedis_options = [f"{c['codigo']} - {c['nombre']}" for c in cedis_list]
                    selected_cedis = st.selectbox("CEDIS *", cedis_options)
                    
                    concepto = st.text_input("Concepto *", placeholder="Ej: Mantenimiento CCTV")
                    categoria = st.selectbox("Categoría *", [
                        "Nómina Seguridad", "Mantenimiento", "Capacitación", 
                        "Equipamiento", "Servicios", "Otros"
                    ])
                    monto = st.number_input("Monto (MXN) *", min_value=0.0, step=100.0)
                
                with col2:
                    fecha_gasto = st.date_input("Fecha del Gasto *", value=date.today())
                    periodo = st.text_input("Período *", placeholder="2026-03", value="2026-03")
                    proveedor = st.text_input("Proveedor")
                    factura = st.text_input("No. Factura")
                
                descripcion = st.text_area("Descripción")
                
                if st.form_submit_button("💾 Registrar Gasto", type="primary", use_container_width=True):
                    if concepto and monto > 0:
                        idx = cedis_options.index(selected_cedis)
                        cedis_id = cedis_list[idx]["id"]
                        
                        new_presupuesto = {
                            "cedis_id": cedis_id,
                            "concepto": concepto,
                            "categoria": categoria,
                            "monto": monto,
                            "moneda": "MXN",
                            "fecha_gasto": fecha_gasto.isoformat(),
                            "periodo": periodo,
                            "proveedor": proveedor or None,
                            "factura": factura or None,
                            "descripcion": descripcion or None,
                            "registrado_por": st.session_state.user["nombre"]
                        }
                        
                        if create_presupuesto(token, new_presupuesto):
                            st.success("✅ Gasto registrado exitosamente")
                            st.rerun()
                        else:
                            st.error("❌ Error al registrar gasto")
                    else:
                        st.warning("⚠️ Completa los campos obligatorios")
        else:
            st.warning("⚠️ Primero debes registrar CEDIS")

def show_configuracion():
    st.title("⚙️ Configuración")
    
    st.subheader("Perfil de Usuario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Nombre", value=st.session_state.user["nombre"], disabled=True)
        st.text_input("Email", value=st.session_state.user["email"], disabled=True)
    
    with col2:
        st.text_input("Rol", value=st.session_state.user["rol"], disabled=True)
        st.selectbox("Zona", ["Sureste"], disabled=True)
    
    st.info("💡 Para cambiar tu información, contacta al administrador del sistema.")

# Main
def main():
    if st.session_state.token is None:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
