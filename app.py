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

# Sección 1: Mapeo de Columnas (Para que coincida con cualquier formato de Excel)
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

# Sección 2: Vista previa masiva adaptada al diseño oficial
st.subheader("🖨️ Credenciales Oficiales Generadas")

if not df.empty:
    
    # Estilos CSS exactos para replicar el diseño de la credencial
    st.markdown("""
    <style>
        .badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 25px;
            justify-content: center;
            margin-top: 20px;
        }
        .badge-card {
            width: 340px;
            height: 500px;
            border: 2px solid #dcdcdc;
            border-radius: 10px;
            background-color: #ffffff;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;
            overflow: hidden;
            display: inline-block;
            margin-bottom: 20px;
            padding: 15px;
            text-align: center;
        }
        /* Semicírculo superior naranja */
        .badge-header {
            background-color: #f28c28;
            height: 120px;
            border-bottom-left-radius: 170px;
            border-bottom-right-radius: 170px;
            margin: -15px -15px 10px -15px;
            padding-top: 15px;
            color: white;
        }
        .badge-header h3 {
            font-size: 13px;
            margin: 0;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        .badge-header p {
            font-size: 8px;
            margin: 3px 0 0 0;
        }
        .badge-photo {
            width: 90px;
            height: 105px;
            background-color: #e2e8f0;
            border: 3px solid #ffffff;
            border-radius: 4px;
            margin: -40px auto 10px auto;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            position: relative;
            z-index: 5;
        }
        .badge-auth {
            font-size: 10px;
            color: #555;
            margin-top: 5px;
        }
        .badge-name {
            font-size: 13px;
            font-weight: bold;
            color: #d35400;
            margin: 6px 0;
            text-transform: uppercase;
            line-height: 1.2;
        }
        .badge-role-title {
            font-size: 9px;
            color: #777;
            margin: 0;
        }
        .badge-role {
            font-size: 11px;
            font-weight: bold;
            color: #222;
            text-transform: uppercase;
            margin-bottom: 15px;
        }
        .badge-footer {
            font-size: 8.5px;
            color: #666;
            border-top: 1px solid #eee;
            padding-top: 8px;
            margin-top: 10px;
        }
        .badge-id-box {
            background-color: #f28c28;
            color: white;
            border-radius: 4px;
            padding: 4px;
            margin-top: 8px;
            font-size: 10px;
            font-family: monospace;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Renderizar tarjetas en cuadrícula
    grid_html = '<div class="badge-container">'

    for index, row in df.iterrows():
        emp_id = str(row.get(col_id, ''))
        nombre = str(row.get(col_nombre, ''))
        cargo = str(row.get(col_cargo, ''))

        grid_html += f"""
        <div class="badge-card">
            <div class="badge-header">
                <h3>ALCALDÍA DE CAMPECHE</h3>
                <p>H. AYUNTAMIENTO DEL MUNICIPIO DE CAMPECHE 2024-2027</p>
            </div>
            
            <div class="badge-photo">👤</div>
            
            <div class="badge-auth">Se autoriza al</div>
            <div class="badge-name">{nombre}</div>
            <div class="badge-role-title">Como:</div>
            <div class="badge-role">{cargo}</div>
            
            <div class="badge-footer">
                Dirección de Desarrollo Urbano y Medio Ambiente<br>
                <div class="badge-id-box">No. EMPLEADO: {emp_id}</div>
            </div>
        </div>
        """

    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown("---")
    st.success("💡 **Impresión masiva:** Presiona `Ctrl + P` en tu teclado para mandar a imprimir todos los gafetes en formato físico o guardarlos en PDF directamente desde tu navegador.")

else:
    st.warning("No hay registros disponibles para mostrar.")
