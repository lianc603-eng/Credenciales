import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Credenciales - DDUMA", layout="wide")

st.title("🏷️ Sistema de Generación Masiva de Credenciales Oficiales")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA) - Alcaldía de Campeche")

# Inicializar DataFrame por defecto
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"NUMERO DE EMPLEADO": 9820, "Nombre completo": "BROWN OCAÑA CITLALLI ESTEFANIA", "Puesto": "JEFE DE DEPARTAMENTO"}
    ])

# Barra lateral para cargar archivo
st.sidebar.header("📁 Cargar Plantilla Maestra")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo base.xlsx o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.data = pd.read_csv(uploaded_file)
        else:
            st.session_state.data = pd.read_excel(uploaded_file)
        st.sidebar.success(f"¡Archivo cargado con {len(st.session_state.data)} registros!")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")

df = st.session_state.data
columnas = list(df.columns)

# Mapeo de columnas automático o manual
def_id = "NUMERO DE EMPLEADO" if "NUMERO DE EMPLEADO" in columnas else columnas[0]
def_nombre = "Nombre completo" if "Nombre completo" in columnas else (columnas[1] if len(columnas) > 1 else columnas[0])
def_puesto = "Puesto" if "Puesto" in columnas else (columnas[2] if len(columnas) > 2 else columnas[0])

st.subheader("⚙️ Configuración de Columnas")
col1, col2, col3 = st.columns(3)
with col1:
    col_id = st.selectbox("Columna de Número de Empleado", columnas, index=columnas.index(def_id) if def_id in columnas else 0)
with col2:
    col_nombre = st.selectbox("Columna de Nombre Completo", columnas, index=columnas.index(def_nombre) if def_nombre in columnas else 0)
with col3:
    col_puesto = st.selectbox("Columna de Puesto / Cargo", columnas, index=columnas.index(def_puesto) if def_puesto in columnas else 0)

st.markdown("---")

st.subheader("🖨️ Credenciales Oficiales (Frente y Reverso)")

if not df.empty:
    
    # Estilos CSS avanzados para ambas caras de la credencial
    st.markdown("""
    <style>
        .badge-wrapper {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .badge-card {
            width: 310px;
            height: 470px;
            border: 2px solid #cbd5e1;
            border-radius: 8px;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            font-family: Arial, sans-serif;
            overflow: hidden;
            position: relative;
            text-align: center;
            padding: 10px;
        }
        /* FRENTE */
        .badge-header {
            background-color: #f28c28;
            height: 95px;
            border-bottom-left-radius: 140px;
            border-bottom-right-radius: 140px;
            color: white;
            padding-top: 10px;
            margin: -10px -10px 0 -10px;
        }
        .badge-header h4 { font-size: 10px; margin: 0; font-weight: bold; }
        .badge-header p { font-size: 6px; margin: 2px 0 0 0; }
        .badge-photo {
            width: 68px;
            height: 80px;
            background-color: #e2e8f0;
            border: 3px solid #ffffff;
            border-radius: 3px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            margin: -25px auto 4px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            position: relative;
            z-index: 5;
        }
        .badge-auth { font-size: 7.5px; color: #64748b; margin-top: 1px; }
        .badge-name { font-size: 10.5px; font-weight: bold; color: #d35400; margin: 2px 8px; text-transform: uppercase; line-height: 1.1; }
        .badge-role-title { font-size: 7px; color: #94a3b8; margin: 0; font-weight: bold; }
        .badge-role { font-size: 9.5px; font-weight: bold; color: #1e293b; text-transform: uppercase; margin-bottom: 4px; }
        .badge-footer-dept {
            font-size: 7.5px;
            color: #555;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 3px;
            margin: 4px auto 8px auto;
            width: 85%;
            background-color: #f8fafc;
            font-weight: bold;
        }
        .badge-fields-box { padding: 0 10px; }
        .badge-field-row { display: flex; margin-bottom: 3px; border-radius: 3px; overflow: hidden; font-size: 8px; font-family: monospace; border: 1px solid #cbd5e1; }
        .badge-field-label { background-color: #f28c28; color: white; padding: 2px 4px; font-weight: bold; width: 40%; text-align: center; }
        .badge-field-val { background-color: #f1f5f9; color: #334155; padding: 2px 4px; width: 60%; text-align: center; font-weight: bold; }

        /* REVERSO */
        .rev-header { border-bottom: 1px solid #f28c28; padding-bottom: 4px; margin-bottom: 4px; text-align: center; }
        .rev-header img, .rev-header-text { font-size: 9px; font-weight: bold; color: #f28c28; }
        .rev-folio { display: inline-block; background-color: #f28c28; color: white; font-size: 8px; font-weight: bold; padding: 2px 10px; border-radius: 4px; margin: 3px 0; }
        .rev-legal { font-size: 5px; color: #666; text-align: justify; line-height: 1.1; margin-bottom: 4px; height: 135px; overflow: hidden; }
        .rev-signs { display: flex; justify-content: space-around; font-size: 5.5px; color: #444; margin-top: 5px; }
        .rev-sign-line { border-top: 1px solid #94a3b8; width: 110px; margin: 15px auto 2px auto; }
        .rev-alert-box { background-color: #f28c28; color: white; border-radius: 6px; padding: 4px; font-size: 6px; margin-top: 6px; text-align: center; }
        .rev-vigencia { font-size: 8px; font-weight: bold; color: #d35400; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

    rows_data = list(df.iterrows())
    
    for _, row in rows_data:
        emp_id = str(row.get(col_id, ''))
        nombre_raw = str(row.get(col_nombre, ''))
        cargo_raw = str(row.get(col_puesto, ''))

        if emp_id == 'nan': emp_id = ''
        nombre = nombre_raw if nombre_raw != 'nan' else ''
        cargo = cargo_raw if cargo_raw != 'nan' else 'SIN PUESTO'
        nombre_formateado = nombre if nombre.upper().startswith("C.") else f"C. {nombre}"

        # FRENTE HTML
        front_html = f'''
        <div class="badge-card">
            <div class="badge-header">
                <h4>ALCALDÍA DE CAMPECHE</h4>
                <p>H. AYUNTAMIENTO DEL MUNICIPIO DE CAMPECHE 2024-2027</p>
            </div>
            <div class="badge-photo">👤</div>
            <div class="badge-auth">Se autoriza al</div>
            <div class="badge-name">{nombre_formateado}</div>
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
        '''

        # REVERSO HTML (con todos los elementos legales, firmas y recuadro inferior de contacto)
        back_html = f'''
        <div class="badge-card">
            <div class="rev-header">
                <div style="font-size:8px; font-weight:bold; color:#777;">ALCALDÍA DE</div>
                <div style="font-size:11px; font-weight:bold; color:#f28c28; letter-spacing:0.5px;">CAMPECHE</div>
            </div>
            <div><span class="rev-folio">Folio &nbsp; 0{emp_id[-3:] if len(emp_id)>=3 else emp_id}/DDUMA/2026</span></div>
            <div class="rev-legal">
                <b>Esta credencial es válida únicamente para actos de naturaleza indicadas.</b><br>
                La presente identificación se emite con fundamento en los artículos 14, 16, 115 fracción V, de la Constitución Política de los Estados Unidos Mexicanos; 105 de la Constitución Política del Estado de Campeche; 189, 190 de la Ley Orgánica de los Municipios del Estado de Campeche; 3, 37, 38, 39, 62, 63, 64, 65, 66, 67, 69 de la Ley de Procedimiento Administrativo para el Estado y los Municipios de Campeche; y ordenamientos aplicables; con vigencia al 31 de diciembre de 2026.
            </div>
            <div class="rev-signs">
                <div>
                    <div class="rev-sign-line"></div>
                    <b>{nombre_formateado}</b><br>Firma del Trabajador
                </div>
                <div>
                    <div class="rev-sign-line"></div>
                    <b>Lic. Rosendo Sánchez Preve</b><br>Director de Desarrollo Urbano y Medio Ambiente
                </div>
            </div>
            <div class="rev-alert-box">
                <b>° El uso indebido de esta credencial constituye un delito.<br>° Quejas, denuncias y en caso de extravió:</b><br>
                <span style="font-size:9px; font-weight:bold;">Tel: 981 102 1212</span>
            </div>
            <div class="rev-vigencia">Vigencia al 31 de diciembre de 2026</div>
        </div>
        '''

        # Mostrar ambas caras lado a lado para cada empleado
        col_f, col_r = st.columns(2)
        with col_f:
            st.markdown(f"**Frente (Empleado: {emp_id})**")
            st.markdown(front_html, unsafe_allow_html=True)
        with col_r:
            st.markdown(f"**Reverso (Empleado: {emp_id})**")
            st.markdown(back_html, unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 1px dashed #cbd5e1; margin: 20px 0;'>", unsafe_allow_html=True)

    st.success("💡 **Impresión masiva:** Presiona `Ctrl + P` en tu teclado para mandar a imprimir todas las credenciales (Frente y Reverso) en formato físico o guardarlas en PDF.")

else:
    st.warning("No hay registros disponibles para mostrar.")
