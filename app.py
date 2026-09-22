import streamlit as st
import pandas as pd
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Generador Masivo de Gafetes", layout="wide")

st.title("🏷️ Generador Masivo de Gafetes Institucionales")
st.markdown("Sube tu hoja de cálculo con la lista para generar y visualizar todos los gafetes de forma masiva.")

# Inicializar un DataFrame por defecto si no existe
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"ID": "GAF-001", "Nombre": "Juan Pérez López", "Cargo": "Analista Administrativo", "Área": "Desarrollo Urbano y Medio Ambiente"},
        {"ID": "GAF-002", "Nombre": "María González Moo", "Cargo": "Coordinadora de Proyectos", "Área": "Obras Públicas"},
        {"ID": "GAF-003", "Nombre": "Carlos Tun Naal", "Cargo": "Supervisor de Campo", "Área": "Medio Ambiente"}
    ])

# Barra lateral para carga de archivo
st.sidebar.header("📁 Cargar Plantilla Maestra")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo (Excel .xlsx o CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.data = pd.read_csv(uploaded_file)
        else:
            st.session_state.data = pd.read_excel(uploaded_file)
        st.sidebar.success(f"¡Se cargaron {len(st.session_state.data)} registros exitosamente!")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")

# Sección 1: Tabla editable y de revisión
st.subheader("📋 Vista Previa de la Plantilla Maestra")
st.markdown("Puedes verificar los datos o hacer correcciones rápidas antes de la impresión masiva:")

edited_data = st.data_editor(
    st.session_state.data, 
    num_rows="dynamic", 
    use_container_width=True,
    key="mass_badge_editor"
)
st.session_state.data = edited_data

st.markdown("---")

# Sección 2: Generación Masiva en Pantalla
st.subheader("🖨️ Vista Masiva de Gafetes (Listos para Impresión)")

if not st.session_state.data.empty:
    col_config1, col_config2 = st.columns([2, 1])
    with col_config1:
        st.info(f"Mostrando **{len(st.session_state.data)} gafetes** generados a partir de la hoja de cálculo.")
    with col_config2:
        # Botón para exportar la base de datos limpia
        csv_export = st.session_state.data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Base Actualizada (CSV)",
            data=csv_export,
            file_name="base_gafetes_actualizada.csv",
            mime="text/csv",
        )

    # Contenedor con diseño de tarjetas en cuadrícula (Grid) para masivo
    badge_container_html = """
    <style>
        .badge-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
        }
        .badge-card {
            border: 3px solid #1b4332;
            border-radius: 12px;
            padding: 15px;
            width: 280px;
            background-color: #ffffff;
            text-align: center;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
            font-family: sans-serif;
        }
    </style>
    <div class="badge-grid">
    """

    for index, row in st.session_state.data.iterrows():
        nombre = row.get('Nombre', 'Sin Nombre')
        cargo = row.get('Cargo', 'Sin Cargo')
        area = row.get('Área', 'Sin Área')
        emp_id = row.get('ID', f'GAF-00{index+1}')

        badge_container_html += f"""
        <div class="badge-card">
            <h5 style="color: #1b4332; margin-bottom: 2px; font-size: 13px;">H. AYUNTAMIENTO DE CAMPECHE</h5>
            <p style="font-size: 9px; color: #555; margin-top: 0; text-transform: uppercase;">Dirección de Desarrollo Urbano y Medio Ambiente</p>
            <hr style="border: 0; border-top: 2px solid #2d6a4f; margin: 8px 0;">
            <div style="background-color: #e9ecef; width: 70px; height: 70px; border-radius: 50%; margin: 10px auto; display: flex; align-items: center; justify-content: center; font-size: 28px; border: 2px dashed #ced4da;">👤</div>
            <h4 style="color: #212529; margin: 8px 0 3px 0; font-size: 16px;">{nombre}</h4>
            <p style="font-size: 12px; font-weight: bold; color: #2d6a4f; margin: 0;">{cargo}</p>
            <p style="font-size: 11px; color: #6c757d; margin-top: 4px;">{area}</p>
            <hr style="border: 0; border-top: 1px solid #dee2e6; margin: 10px 0 5px 0;">
            <p style="font-size: 9px; color: #adb5bd; margin: 0; font-family: monospace;">ID: {emp_id}</p>
        </div>
        """

    badge_container_html += "</div>"

    # Renderizar todos los gafetes en pantalla distribuidos en cuadrícula
    st.markdown(badge_container_html, unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("💡 **Tip de impresión:** Para imprimir todos los gafetes en papel físico desde tu navegador, presiona las teclas `Ctrl + P` y ajusta la escala de impresión a tu preferencia.")

else:
    st.warning("No hay registros en la tabla. Sube un archivo o agrega datos manualmente.")
