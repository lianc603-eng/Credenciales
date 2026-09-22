import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Gafetes - DDUMA", layout="wide")

st.title("🏷️ Sistema de Generación Masiva de Gafetes")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA) - Alcaldía de Campeche")

# Inicializar DataFrame por defecto
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"No_Empleado": "9820", "Nombre": "C. CITLALLI ESTEFANÍA BROWN OCAÑA", "Cargo": "ANALISTA"}
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

# Sección 1: Configuración de Columnas
st.subheader("⚙️ Configuración de Columnas")
st.markdown("Selecciona con precisión qué columna de tu archivo corresponde a cada dato:")

columnas_disponibles = list(df.columns)

col1, col2, col3 = st.columns(3)
with col1:
    col_id = st.selectbox("Columna de No. de Empleado / ID", columnas_disponibles, index=0 if len(columnas_disponibles) > 0 else 0)
with col2:
    col_nombre = st.selectbox("Columna de Nombre Completo", columnas_disponibles, index=min(3, len(columnas_disponibles)-1))
with col3:
    col_cargo = st.selectbox("Columna de Cargo / Puesto", columnas_disponibles, index=min(4, len(columnas_disponibles)-1))

st.markdown("---")

# Sección 2: Credenciales Generadas con el Diseño Exacto
st.subheader("🖨️ Credenciales Oficiales Generadas")

if not df.empty:
    
    # Estilos CSS exactos para replicar la estructura visual de la credencial
    st.markdown("""
    <style>
        .badge-card {
            width: 320px;
            height: 480px;
            border: 2px solid #cbd5e1;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            font-family: Arial, sans-serif;
            overflow: hidden;
            margin-bottom: 25px;
            text-align: center;
            display: inline-block;
        }
        /* Semicírculo superior naranja */
        .badge-header {
            background-color: #f28c28;
            height: 110px;
            border-bottom-left-radius: 160px;
            border-bottom-right-radius: 160px;
            color: white;
            padding-top: 15px;
        }
        .badge-header h4 {
            font-size: 11px;
            margin: 0;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        .badge-header p {
            font-size: 7px;
            margin: 2px 0 0 0;
        }
        /* Contenedor de la foto superpuesto en el borde del semicírculo */
        .badge-photo-container {
            margin-top: -35px;
            display: flex;
            justify-content: center;
            position: relative;
            z-index: 5;
        }
        .badge-photo {
            width: 80px;
            height: 95px;
            background-color: #e2e8f0;
            border: 3px solid #ffffff;
            border-radius: 3px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
        }
        .badge-auth {
            font-size: 9px;
            color: #64748b;
            margin-top: 4px;
        }
        .badge-name {
            font-size: 12px;
            font-weight: bold;
            color: #d35400;
            margin: 4px 12px;
            text-transform: uppercase;
            line-height: 1.1;
        }
        .badge-role-title {
            font-size: 8px;
            color: #94a3b8;
            margin: 2px 0 0 0;
            font-weight: bold;
        }
        .badge-role {
            font-size: 11px;
            font-weight: bold;
            color: #1e293b;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .badge-footer-dept {
            font-size: 8px;
            color: #94a3b8;
            margin-bottom: 8px;
            padding: 0 10px;
        }
        /* Bloques inferiores de ID y No. de Empleado */
        .badge-fields-box {
            padding: 0 20px;
        }
        .badge-field-row {
            display: flex;
            margin-bottom: 4px;
            border-radius: 3px;
            overflow: hidden;
            font-size: 9px;
            font-family: monospace;
            border: 1px solid #cbd5e1;
        }
        .badge-field-label {
            background-color: #f28c28;
            color: white;
            padding: 4px 6px;
            font-weight: bold;
            width: 42%;
            text-align: center;
        }
        .badge-field-val {
            background-color: #f1f5f9;
            color: #334155;
            padding: 4px 6px;
            width: 58%;
            text-align: center;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Mostrar tarjetas en filas de 3 columnas
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
                        
                        <div class="badge-photo-container">
                            <div class="badge-photo">👤</div>
                        </div>
                        
                        <div class="badge-auth">Se autoriza al</div>
                        <div class="badge-name">{nombre}</div>
                        <div class="badge-role-title">Como:</div>
                        <div class="badge-role">{cargo}</div>
                        
                        <div class="badge-footer-dept">Dirección de Desarrollo Urbano y Medio Ambiente</div>
                        
                        <div class="badge-fields-box">
                            <div class="badge-field-row">
                                <div class="badge-field-label">ID</div>
                                <div class="badge-field-val">DDUMA-EMP-{emp_id}</div>
                            </div>
                            <div class="badge-field-row">
                                <div class="badge-field-label">No. Empleado</div>
                                <div class="badge-field-val">{emp_id}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("💡 **Impresión masiva:** Presiona `Ctrl + P` en tu teclado para mandar a imprimir todos los gafetes en formato físico o guardarlos en PDF directamente desde tu navegador.")

else:
    st.warning("No hay registros disponibles para mostrar.")
