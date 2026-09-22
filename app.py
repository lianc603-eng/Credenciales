import streamlit as st
import pandas as pd
import base64

# Configuración de la página
st.set_page_config(page_title="Plantilla Maestra de Gafetes - DDUMA", layout="wide")

st.title("🏷️ Diseñador de Plantilla Maestra y Generador de Gafetes")
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

st.sidebar.subheader("2. Elementos Gráficos y Fondo")
bg_color_header = st.sidebar.color_picker("Color del Encabezado", "#f28c28")
bg_image_file = st.sidebar.file_uploader("Subir Imagen de Fondo para la Credencial", type=["jpg", "jpeg", "png"])

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

# Carga masiva de fotos individuales
uploaded_images = st.sidebar.file_uploader("Subir fotos de empleados (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
dict_images = {}
if uploaded_images:
    for img_file in uploaded_images:
        dict_images[img_file.name] = img_file

# ---------------------------------------------------------
# CONTENEDOR PRINCIPAL: VISTA PREVIA OPTIMIZADA (MITAD CARTA)
# ---------------------------------------------------------
st.subheader("🖨️ Vista Previa de la Plantilla (Diseñada para Mitad de Hoja Carta)")
st.markdown("Modifica los parámetros en la barra lateral izquierda y se actualizará toda la plantilla maestra al instante.")

if not df.empty:
    
    # Estilos CSS con llaves escapadas correctamente {{ }}
    bg_style = f"background-image: url('data:image/jpeg;base64,{bg_image_b64}'); background-size: cover; background-position: center;" if bg_image_b64 else "background-color: #ffffff;"

    st.markdown(f"""
    <style>
        .page-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }}
        .badge-card {{
            width: 340px;
            height: 500px;
            border: 2px dashed #94a3b8;
            border-radius: 8px;
            {bg_style}
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;
            overflow: hidden;
            position: relative;
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
        }}
        .badge-header {{
            background-color: {bg_color_header};
            height: 105px;
            border-bottom-left-radius: 160px;
            border-bottom-right-radius: 160px;
            color: white;
            padding-top: 12px;
            margin: -10px -10px 0 -10px;
        }}
        .badge-header h4 {{ font-size: 11px; margin: 0; font-weight: bold; }}
        .badge-header p {{ font-size: 6.5px; margin: 2px 0 0 0; }}
        .badge-photo-box {{
            width: 75px;
            height: 90px;
            background-color: #e2e8f0;
            border: 3px solid #ffffff;
            border-radius: 3px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            margin: -30px auto 4px auto;
            overflow: hidden;
            position: relative;
            z-index: 5;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .badge-photo-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .badge-auth {{ font-size: 8px; color: #475569; margin-top: 2px; font-weight: bold; }}
        .badge-name {{ font-size: 11.5px; font-weight: bold; color: #c2410c; margin: 3px 8px; text-transform: uppercase; line-height: 1.1; }}
        .badge-role-title {{ font-size: 7.5px; color: #64748b; margin: 0; font-weight: bold; }}
        .badge-role {{ font-size: 10px; font-weight: bold; color: #0f172a; text-transform: uppercase; margin-bottom: 6px; }}
        .badge-footer-dept {{
            font-size: 8px;
            color: #1e293b;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 4px;
            margin: 4px auto 10px auto;
            width: 90%;
            background-color: rgba(255, 255, 255, 0.9);
            font-weight: bold;
        }}
        .badge-fields-box {{ padding: 0 10px; }}
        .badge-field-row {{ display: flex; margin-bottom: 3px; border-radius: 3px; overflow: hidden; font-size: 8.5px; font-family: monospace; border: 1px solid #cbd5e1; }}
        .badge-field-label {{ background-color: {bg_color_header}; color: white; padding: 3px 4px; font-weight: bold; width: 40%; text-align: center; }}
        .badge-field-val {{ background-color: rgba(241, 245, 249, 0.9); color: #1e293b; padding: 3px 4px; width: 60%; text-align: center; font-weight: bold; }}
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

        img_html = "👤"
        for key, file_obj in dict_images.items():
            if emp_id in key or nombre.split()[0] in key:
                b64_str = base64.b64encode(file_obj.getvalue()).decode("utf-8")
                img_html = f'<img src="data:image/jpeg;base64,{b64_str}">'
                break

        front_html = f'''
        <div class="badge-card">
            <div class="badge-header">
                <h4>{texto_header_1}</h4>
                <p>{texto_header_2}</p>
            </div>
            <div class="badge-photo-box">{img_html}</div>
            <div class="badge-auth">Se autoriza al</div>
            <div class="badge-name">{nombre_formateado}</div>
            <div class="badge-role-title">Como:</div>
            <div class="badge-role">{cargo}</div>
            <div class="badge-footer-dept">{texto_depto}</div>
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

        col_center = st.columns([1, 2, 1])
        with col_center[1]:
            st.markdown(f"**Credencial para: {nombre_formateado} (Emp: {emp_id})**")
            st.markdown(front_html, unsafe_allow_html=True)
            
        st.markdown("<hr style='border: 1px dashed #cbd5e1; margin: 15px 0;'>", unsafe_allow_html=True)

    st.success("💡 **Plantilla Maestra Lista:** Modifica cualquier texto o color en el menú lateral izquierdo. Al presionar `Ctrl + P`, la interfaz está adaptada para imprimir cómodamente en formato físico o PDF a la mitad de tu hoja carta.")

else:
    st.warning("No hay registros en la base de datos.")
