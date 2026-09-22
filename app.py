import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Gafetes - Alcaldía de Campeche", layout="wide")

st.title("🏷️ Sistema de Generación Masiva de Gafetes")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA)")

# Inicializar un DataFrame por defecto con la estructura requerida
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {
            "ID": "DDUMA-EMP-5527", 
            "No_Empleado": "5527", 
            "Folio": "049/DDUMA/2026", 
            "Nombre": "C. LEIDY CONSUELO NAVARRO PACHECO", 
            "Cargo": "AUXILIAR ADMINISTRATIVO", 
            "Vigencia": "01 de enero al 31 de diciembre de 2026",
            "Foto_URL": ""
        }
    ])

# Barra lateral para cargar archivo de Excel / CSV maestro
st.sidebar.header("📁 Plantilla Maestra")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo de Excel o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.data = pd.read_csv(uploaded_file)
        else:
            st.session_state.data = pd.read_excel(uploaded_file)
        st.sidebar.success(f"¡Se cargaron {len(st.session_state.data)} registros!")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")

# Sección 1: Editor de la Base de Datos
st.subheader("📋 Base de Datos de Personal")
edited_data = st.data_editor(
    st.session_state.data, 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_gafetes"
)
st.session_state.data = edited_data

st.markdown("---")

# Sección 2: Vista previa masiva adaptada al diseño oficial
st.subheader("🖨️ Credenciales Oficiales Generadas")

if not st.session_state.data.empty:
    
    # Estilos CSS idénticos al formato oficial de la Alcaldía de Campeche
    st.markdown("""
    <style>
        .badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            justify-content: center;
            margin-top: 20px;
        }
        .badge-card {
            width: 380px;
            height: 540px;
            border: 2px solid #ccc;
            border-radius: 8px;
            background-color: #ffffff;
            position: relative;
            box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
            font-family: Arial, sans-serif;
            overflow: hidden;
            display: inline-block;
            margin-bottom: 20px;
        }
        /* Semicírculo superior naranja */
        .badge-header-bg {
            width: 100%;
            height: 160px;
            background-color: #f28c28;
            border-bottom-left-radius: 190px;
            border-bottom-right-radius: 190px;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
        }
        .badge-content {
            position: relative;
            z-index: 2;
            padding: 15px;
            text-align: center;
        }
        .badge-title {
            font-size: 11px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 5px;
            line-height: 1.2;
        }
        .badge-photo-box {
            width: 110px;
            height: 130px;
            background-color: #e9ecef;
            border: 3px solid #ffffff;
            border-radius: 4px;
            margin: 25px auto 10px auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
        }
        .badge-auth {
            font-size: 11px;
            color: #444;
            margin-top: 5px;
            font-weight: bold;
        }
        .badge-name {
            font-size: 14px;
            font-weight: bold;
            color: #d35400;
            margin: 4px 0;
            text-transform: uppercase;
        }
        .badge-role-title {
            font-size: 10px;
            color: #666;
            margin: 0;
        }
        .badge-role {
            font-size: 12px;
            font-weight: bold;
            color: #333;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .badge-footer-text {
            font-size: 9px;
            color: #666;
            margin-top: 5px;
        }
        .badge-badge-info {
            background-color: #e2e8f0;
            border-radius: 4px;
            padding: 4px;
            margin: 6px auto;
            width: 80%;
            font-size: 10px;
            font-family: monospace;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Renderizar tarjetas en contenedor flexible
    grid_html = '<div class="badge-container">'

    for index, row in st.session_state.data.iterrows():
        nombre = row.get('Nombre', 'NOMBRE DEL TRABAJADOR')
        cargo = row.get('Cargo', 'CARGO')
        empleado_id = row.get('ID', 'DDUMA-EMP-0000')
        num_emp = row.get('No_Empleado', '0000')

        grid_html += f"""
        <div class="badge-card">
            <div class="badge-header-bg"></div>
            <div class="badge-content">
                <div class="badge-title">ALCALDÍA DE CAMPECHE<br><span style="font-size:8px; font-weight:normal;">H. AYUNTAMIENTO DEL MUNICIPIO DE CAMPECHE 2024-2027</span></div>
                
                <div class="badge-photo-box">👤</div>
                
                <div class="badge-auth">Se autoriza al</div>
                <div class="badge-name">{nombre}</div>
                <div class="badge-role-title">Como:</div>
                <div class="badge-role">{cargo}</div>
                
                <div class="badge-footer-text">Dirección de Desarrollo Urbano y Medio Ambiente</div>
                
                <div class="badge-badge-info" style="background-color: #f28c28; color: white;">
                    ID: {empleado_id}
                </div>
                <div class="badge-badge-info">
                    No. Empleado: {num_emp}
                </div>
            </div>
        </div>
        """

    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown("---")
    
    # Botón para descargar el CSV actualizado
    csv_data = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Plantilla Actualizada en CSV",
        data=csv_data,
        file_name="plantilla_maestra_actualizada.csv",
        mime="text/csv"
    )

else:
    st.warning("No hay registros disponibles para mostrar.")
