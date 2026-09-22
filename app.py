import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Gafetes - DDUMA", layout="wide")

st.title("🏷️ Sistema de Generación Masiva de Gafetes")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA) - Alcaldía de Campeche")

# Inicializar DataFrame por defecto
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"No_Empleado": "5527", "Nombre": "C. LEIDY CONSUELO NAVARRO PACHECO", "Cargo": "AUXILIAR ADMINISTRATIVO"}
    ])

# Barra lateral para cargar archivo de Excel o CSV
st.sidebar.header("📁 Cargar Plantilla Maestra")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo de Excel o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.data = pd.read_csv(uploaded_file)
        else:
            st.session_state.data = pd.read_excel(uploaded_file)
        st.sidebar.success(f"¡Archivo cargado con {len(st.session_state.data)} filas!")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")

df = st.session_state.data

# Sección 1: Mapeo de Columnas
st.subheader("⚙️ Configuración de Columnas")
st.markdown("Indica qué columna de tu archivo corresponde a cada dato del gafete:")

columnas_disponibles = list(df.columns)

col1, col2, col3 = st.columns(3)
with col1:
    col_id = st.selectbox("Columna de No. de Empleado / ID", columnas_disponibles, index=0 if len(columnas_disponibles) > 0 else 0)
with col2:
    col_nombre = st.selectbox("Columna de Nombre(s) / Apellidos", columnas_disponibles, index=1 if len(columnas_disponibles) > 1 else 0)
with col3:
    col_cargo = st.selectbox("Columna de Cargo / Puesto", columnas_disponibles, index=min(4, len(columnas_disponibles)-1))

st.markdown("---")

# Sección 2: Vista previa masiva adaptada
st.subheader("🖨️ Credenciales Oficiales Generadas")

if not df.empty:
    
    # Estilos CSS limpios para las tarjetas individuales
    st.markdown("""
    <style>
        .badge-card {
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            font-family: Arial, sans-serif;
            overflow: hidden;
            margin-bottom: 20px;
            text-align: center;
            padding-bottom: 15px;
        }
        .badge-header {
            background-color: #f28c28;
            padding: 15px 10px;
            border-bottom-left-radius: 120px;
            border-bottom-right-radius: 120px;
            color: white;
            margin-bottom: 15px;
        }
        .badge-header h4 {
            font-size: 12px;
            margin: 0;
            font-weight: bold;
        }
        .badge-header p {
            font-size: 7.5px;
            margin: 2px 0 0 0;
        }
        .badge-name {
            font-size: 12px;
            font-weight: bold;
            color: #d35400;
            margin: 8px 10px;
            text-transform: uppercase;
        }
        .badge-role {
            font-size: 11px;
            font-weight: bold;
            color: #2d3748;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .badge-footer {
            font-size: 8px;
            color: #718096;
            border-top: 1px solid #edf2f7;
            padding-top: 8px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Mostrar las tarjetas en filas de 3 columnas para que sea masivo y ordenado
    num_cols = 3
    rows_data = list(df.iterrows())
    
    for i in range(0, len(rows_data), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(rows_data):
                _, row = rows_data[i + j]
                emp_id = str(row.get(col_id, ''))
                nombre = str(row.get(col_nombre, ''))
                cargo = str(row.get(col_cargo, ''))

                with cols[j]:
                    st.markdown(f"""
                    <div class="badge-card">
                        <div class="badge-header">
                            <h4>ALCALDÍA DE CAMPECHE</h4>
                            <p>H. AYUNTAMIENTO DEL MUNICIPIO DE CAMPECHE 2024-2027</p>
                        </div>
                        <div style="font-size: 28px; margin-bottom: 5px;">👤</div>
                        <div style="font-size: 9px; color: #718096;">Se autoriza al</div>
                        <div class="badge-name">{nombre}</div>
                        <div style="font-size: 8.5px; color: #a0aec0;">Como:</div>
                        <div class="badge-role">{cargo}</div>
                        <div class="badge-footer">
                            Dirección de Desarrollo Urbano y Medio Ambiente<br>
                            <b style="color: #f28c28;">No. EMPLEADO: {emp_id}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("💡 **Impresión masiva:** Presiona `Ctrl + P` en tu teclado para mandar a imprimir todos los gafetes en formato físico o guardarlos en PDF directamente desde tu navegador.")

else:
    st.warning("No hay registros disponibles para mostrar.")
