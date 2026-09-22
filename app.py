import streamlit as st
import pandas as pd
import base64

# Configuración de la página
st.set_page_config(page_title="Plantilla Maestra de Credenciales - DDUMA", layout="wide")

st.title("🏷️ Diseñador de Plantilla Maestra (Frente y Reverso Integrados)")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA) - Alcaldía de Campeche")

# Inicializar DataFrame por defecto
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"NUMERO DE EMPLEADO": 9820, "Nombre completo": "BROWN OCAÑA CITLALLI ESTEFANIA", "Puesto": "JEFE DE DEPARTAMENTO"}
    ])

# ---------------------------------------------------------
# BARRA LATERAL: CONFIGURACIÓN GENERAL DE LA PLANTILLA MAESTRA
# ---------------------------------------------------------
st.sidebar.header("🎨 Editor de Plantilla Maestra")

st.sidebar.subheader("1. Textos Institucionales")
texto_header_1 = st.sidebar.text_input("Texto Superior 1", "ALCALDÍA DE CAMPECHE")
texto_header_2 = st.sidebar.text_input("Texto Superior 2", "H. AYUNTAMIENTO DEL MUNICIPIO DE CAMPECHE 2024-2027")
texto_depto = st.sidebar.text_input("Texto de Dependencia", "Dirección de Desarrollo Urbano y Medio Ambiente")

st.sidebar.subheader("2. Imagen de Fondo de la Plantilla")
bg_image_file = st.sidebar.file_uploader("Subir Imagen Base de la Credencial (Fondo)", type=["jpg", "jpeg", "png"])

bg_image_b64 = ""
if bg_image_file is not None:
    bg_bytes = bg_image_file.getvalue()
    bg_image_b64 = base64.b64encode(bg_bytes).decode("utf-8")

st.sidebar.subheader("3. Cargar Datos y Fotos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo base.xlsx o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.data = pd.read_csv(uploaded_file)
        else:
            st.session_state.data = pd.read_excel(uploaded_file)
        st.sidebar.success(f"¡Cargado con {len(st.session_state.data)} registros!")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")

df = st.session_state.data
columnas = list(df.columns)

# Mapeo automático de columnas
def_id = "NUMERO DE EMPLEADO" if "NUMERO DE EMPLEADO" in columnas else columnas[0]
def_nombre = "Nombre completo" if "Nombre completo" in columnas else (columnas[1] if len(columnas) > 1 else columnas[0])
def_puesto = "Puesto" if "Puesto" in columnas else (columnas[2] if len(columnas) > 2 else columnas[0])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Columnas de la Base")
col_id = st.sidebar.selectbox("Columna ID / No. Empleado", columnas, index=columnas.index(def_id) if def_id in columnas else 0)
col_nombre = st.sidebar.selectbox("Columna Nombre", columnas, index=columnas.index(def_nombre) if def_nombre in columnas else 0)
col_puesto = st.sidebar.selectbox("Columna Puesto", columnas, index=columnas.index(def_puesto) if def_puesto in columnas else 0)

uploaded_images = st.sidebar.file_uploader("Subir fotos de empleados (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
dict_images = {}
if uploaded_images:
    for img_file in uploaded_images:
        dict_images[img_file.name] = img_file

# ---------------------------------------------------------
# CONTENEDOR PRINCIPAL: VISTA PREVIA (PLANTILLA INTEGRADA)
# ---------------------------------------------------------
st.subheader("🖨️ Vista Previa de la Plantilla Maestra (Mitad Hoja Carta)")
st.markdown("Esta vista integra el diseño base con la sección izquierda (Frente) y la sección derecha (Reverso) sin iconos sobrantes.")

if not df.empty:
    
    bg_style = f"background-image: url('data:image/jpeg;base64,{bg_image_b64}'); background-size: cover; background-position: center;" if bg_image_b64 else "background-color: #ffffff;"

    st.markdown(f"""
    <style>
        .master-card {{
            width: 700px;
            height: 480px;
            border: 2px solid #cbd5e1;
            border-radius: 10px;
            {bg_style}
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;
            position: relative;
            margin: 0 auto 30px auto;
            display: flex;
            overflow: hidden;
        }}
        /* Lado Izquierdo: FRENTE */
        .side-front {{
            width: 50%;
            height: 100%;
            position: relative;
            text-align: center;
            padding: 10px;
        }}
        .badge-photo-box {{
            width: 75px;
            height: 90px;
            background-color: #e2e8f0;
            border: 2px solid #ffffff;
            border-radius: 3px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            position: absolute;
            top: 75px;
            left: 110px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 5;
        }}
        .badge-photo-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .badge-content {{
            position: absolute;
            top: 180px;
            width: 100%;
            left: 0;
            padding: 0 15px;
        }}
        .badge-auth {{ font-size: 8.5px; color: #475569; font-weight: bold; margin-bottom: 2px; }}
        .badge-name {{ font-size: 11px; font-weight: bold; color: #c2410c; text-transform: uppercase; line-height: 1.1; margin-bottom: 4px; }}
        .badge-role-title {{ font-size: 7.5px; color: #64748b; font-weight: bold; margin: 0; }}
        .badge-role {{ font-size: 10px; font-weight: bold; color: #0f172a; text-transform: uppercase; margin-bottom: 10px; }}
        .badge-footer-dept {{
            font-size: 8px;
            color: #1e293b;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 3px;
            margin: 0 auto 8px auto;
            width: 85%;
            background-color: rgba(255, 255, 255, 0.9);
            font-weight: bold;
        }}
        .badge-field-row {{ display: flex; margin-bottom: 3px; border-radius: 3px; overflow: hidden; font-size: 8px; font-family: monospace; border: 1px solid #cbd5e1; width: 85%; margin-left: auto; margin-right: auto; }}
        .badge-field-label {{ background-color: #f28c28; color: white; padding: 2px 4px; font-weight: bold; width: 40%; text-align: center; }}
        .badge-field-val {{ background-color: rgba(241, 245, 249, 0.9); color: #1e293b; padding: 2px 4px; width: 60%; text-align: center; font-weight: bold; }}

        /* Lado Derecho: REVERSO */
        .side-back {{
            width: 50%;
            height: 100%;
            padding: 15px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
        }}
        .rev-folio {{ display: inline-block; background-color: #f28c28; color: white; font-size: 8px; font-weight: bold; padding: 2px 10px; border-radius: 4px; }}
        .rev-legal {{ font-size: 5.5px; color: #334155; text-align: justify; line-height: 1.2; }}
        .rev-signs {{ display: flex; justify-content: space-around; font-size: 6px; color: #1e293b; }}
        .rev-sign-line {{ border-top: 1px solid #64748b; width: 100px; margin: 12px auto 2px auto; }}
        .rev-alert-box {{ background-color: #f28c28; color: white; border-radius: 5px; padding: 4px; font-size: 6px; text-align: center; }}
        .rev-vigencia {{ font-size: 8px; font-weight: bold; color: #c2410c; }}
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

        # Si hay foto subida, la muestra; si no, deja el cuadro limpio sin icono por defecto
        img_html = ""
        for key, file_obj in dict_images.items():
            if emp_id in key or nombre.split()[0] in key:
                b64_str = base64.b64encode(file_obj.getvalue()).decode("utf-8")
                img_html = f'<img src="data:image/jpeg;base64,{b64_str}">'
                break

        master_card_html = f'''
        <div class="master-card">
            <!-- FRENTE (IZQUIERDA) -->
            <div class="side-front">
                <div class="badge-photo-box">{img_html}</div>
                <div class="badge-content">
                    <div class="badge-auth">Se autoriza al</div>
                    <div class="badge-name">{nombre_formateado}</div>
                    <div class="badge-role-title">Como:</div>
                    <div class="badge-role">{cargo}</div>
                    <div class="badge-footer-dept">{texto_depto}</div>
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

            <!-- REVERSO (DERECHA) -->
            <div class="side-back">
                <div>
                    <div style="font-size:9px; font-weight:bold; color:#f28c28;">ALCALDÍA DE CAMPECHE</div>
                    <span class="rev-folio">Folio &nbsp; 0{emp_id[-3:] if len(emp_id)>=3 else emp_id}/DDUMA/2026</span>
                </div>
                <div class="rev-legal">
                    <b>Esta credencial es válida únicamente para actos de naturaleza indicadas.</b><br>
                    La presente identificación se emite con fundamento en los artículos 14, 16, 115 fracción V, de la Constitución Política de los Estados Unidos Mexicanos; 105 de la Constitución Política del Estado de Campeche; 189, 190 de la Ley Orgánica de los Municipios del Estado de Campeche; y ordenamientos aplicables; con vigencia al 31 de diciembre de 2026.
                </div>
                <div class="rev-signs">
                    <div>
                        <div class="rev-sign-line"></div>
                        <b>{nombre_formateado}</b><br>Firma del Trabajador
                    </div>
                    <div>
                        <div class="rev-sign-line"></div>
                        <b>Lic. Rosendo Sánchez Preve</b><br>Director de Desarrollo Urbano
                    </div>
                </div>
                <div class="rev-alert-box">
                    <b>° El uso indebido de esta credencial constituye un delito.<br>° Quejas, denuncias y en caso de extravió:</b><br>
                    <span style="font-size:8.5px; font-weight:bold;">Tel: 981 102 1212</span>
                </div>
                <div class="rev-vigencia">Vigencia al 31 de diciembre de 2026</div>
            </div>
        </div>
        '''

        st.markdown(f"**Credencial Completa (Frente y Reverso) para: {nombre_formateado}**")
        st.markdown(master_card_html, unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px dashed #cbd5e1; margin: 20px 0;'>", unsafe_allow_html=True)

    st.success("💡 **Plantilla Actualizada:** El icono genérico ha sido eliminado por completo. Sube tu imagen de fondo para que empate perfectamente con el diseño de la alcaldía y presiona `Ctrl + P` para imprimir.")

else:
    st.warning("No hay registros en la base de datos.")
