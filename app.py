import streamlit as st
import pandas as pd
import base64

# Configuración de la página
st.set_page_config(page_title="Editor de Credenciales - Tamaño Media Carta", layout="wide")

st.title("🎨 Creador de Plantilla Maestra (Tamaño Media Carta)")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA) - Alcaldía de Campeche")

# Inicializar DataFrame por defecto
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"NUMERO DE EMPLEADO": 9820, "Nombre completo": "BROWN OCAÑA CITLALLI ESTEFANIA", "Puesto": "JEFE DE DEPARTAMENTO"}
    ])

# ---------------------------------------------------------
# BARRA LATERAL: CONTROLES DE LA PLANTILLA MAESTRA
# ---------------------------------------------------------
st.sidebar.header("🛠️ Controles de Plantilla (Media Carta)")

# 1. Subir Imagen de Fondo
st.sidebar.subheader("1. Imagen de Fondo (Plantilla Media Carta)")
bg_file = st.sidebar.file_uploader("Sube tu plantilla base (JPG/PNG)", type=["jpg", "jpeg", "png"])
bg_b64 = ""
if bg_file is not None:
    bg_b64 = base64.b64encode(bg_file.getvalue()).decode("utf-8")

# 2. Control de Posición de la Fotografía
st.sidebar.subheader("2. Posición y Tamaño de la Foto")
foto_left = st.sidebar.slider("Posición Izquierda (X %)", 0, 80, 12)
foto_top = st.sidebar.slider("Posición Arriba (Y %)", 0, 80, 25)
foto_width = st.sidebar.slider("Ancho de la Foto (px)", 80, 300, 150)
foto_height = st.sidebar.slider("Alto de la Foto (px)", 100, 350, 200)

# 3. Textos Libres Adicionales
st.sidebar.subheader("3. Texto Personalizado")
texto_extra = st.sidebar.text_input("Texto Adicional", "Válido por el periodo 2026")
texto_x = st.sidebar.slider("Posición Texto X (%)", 0, 80, 10)
texto_y = st.sidebar.slider("Posición Texto Y (%)", 0, 90, 80)
texto_size = st.sidebar.slider("Tamaño de Fuente (px)", 10, 35, 16)
texto_color = st.sidebar.color_picker("Color del Texto", "#334155")

# 4. Cargar Base de Datos
st.sidebar.subheader("4. Base de Datos y Fotos")
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

def_id = "NUMERO DE EMPLEADO" if "NUMERO DE EMPLEADO" in columnas else columnas[0]
def_nombre = "Nombre completo" if "Nombre completo" in columnas else (columnas[1] if len(columnas) > 1 else columnas[0])
def_puesto = "Puesto" if "Puesto" in columnas else (columnas[2] if len(columnas) > 2 else columnas[0])

st.sidebar.markdown("---")
col_id = st.sidebar.selectbox("Columna ID / No. Empleado", columnas, index=columnas.index(def_id) if def_id in columnas else 0)
col_nombre = st.sidebar.selectbox("Columna Nombre", columnas, index=columnas.index(def_nombre) if def_nombre in columnas else 0)
col_puesto = st.sidebar.selectbox("Columna Puesto", columnas, index=columnas.index(def_puesto) if def_puesto in columnas else 0)

uploaded_images = st.sidebar.file_uploader("Subir fotos individuales (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
dict_images = {}
if uploaded_images:
    for img_file in uploaded_images:
        dict_images[img_file.name] = img_file

# ---------------------------------------------------------
# RENDERIZADO DEL LIENZO: TAMAÑO MEDIA CARTA REAL
# ---------------------------------------------------------
st.subheader("🖨️ Vista Previa en Formato Media Carta")
st.markdown("Cada credencial está escalada a proporciones de Media Carta (Frente a la izquierda y Reverso a la derecha).")

if not df.empty:
    
    bg_style = f"background-image: url('data:image/jpeg;base64,{bg_b64}'); background-size: cover; background-position: center;" if bg_b64 else "background-color: #f8fafc; border: 2px dashed #cbd5e1;"

    st.markdown(f"""
    <style>
        .master-canvas {{
            width: 816px;
            height: 528px;
            border-radius: 10px;
            {bg_style}
            box-shadow: 0 8px 25px rgba(0,0,0,0.18);
            font-family: Arial, sans-serif;
            position: relative;
            margin: 0 auto 35px auto;
            display: flex;
            overflow: hidden;
        }}
        .side-front {{
            width: 50%;
            height: 100%;
            position: relative;
        }}
        .canvas-photo {{
            width: {foto_width}px;
            height: {foto_height}px;
            background-color: #e2e8f0;
            border: 3px solid #ffffff;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            position: absolute;
            top: {foto_top}%;
            left: {foto_left}%;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }}
        .canvas-photo img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .canvas-custom-text {{
            position: absolute;
            top: {texto_y}%;
            left: {texto_x}%;
            font-size: {texto_size}px;
            color: {texto_color};
            font-weight: bold;
            z-index: 10;
        }}
        .side-back {{
            width: 50%;
            height: 100%;
            padding: 30px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
        }}
        .rev-folio {{ display: inline-block; background-color: #f28c28; color: white; font-size: 11px; font-weight: bold; padding: 4px 14px; border-radius: 5px; }}
        .rev-legal {{ font-size: 8px; color: #334155; text-align: justify; line-height: 1.3; }}
        .rev-signs {{ display: flex; justify-content: space-around; font-size: 9px; color: #1e293b; }}
        .rev-sign-line {{ border-top: 1px solid #64748b; width: 140px; margin: 20px auto 4px auto; }}
        .rev-alert-box {{ background-color: #f28c28; color: white; border-radius: 6px; padding: 6px; font-size: 9px; text-align: center; }}
        .rev-vigencia {{ font-size: 11px; font-weight: bold; color: #c2410c; }}
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

        img_html = ""
        for key, file_obj in dict_images.items():
            if emp_id in key or nombre.split()[0] in key:
                b64_str = base64.b64encode(file_obj.getvalue()).decode("utf-8")
                img_html = f'<img src="data:image/jpeg;base64,{b64_str}">'
                break

        canvas_html = f'''
        <div class="master-canvas">
            <!-- FRENTE (IZQUIERDA) -->
            <div class="side-front">
                <div class="canvas-photo">{img_html}</div>
                <div class="canvas-custom-text">{texto_extra}</div>
            </div>

            <!-- REVERSO (DERECHA) -->
            <div class="side-back">
                <div>
                    <div style="font-size:12px; font-weight:bold; color:#f28c28;">ALCALDÍA DE CAMPECHE</div>
                    <span class="rev-folio">Folio &nbsp; 0{emp_id[-3:] if len(emp_id)>=3 else emp_id}/DDUMA/2026</span>
                </div>
                <div class="rev-legal">
                    <b>Credencial oficial de identificación institucional.</b><br>
                    Emitida conforme a la normatividad aplicable para la Dirección de Desarrollo Urbano y Medio Ambiente de la Alcaldía de Campeche, con validez al 31 de diciembre de 2026.
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
                    <b>° El uso indebido de esta credencial constituye un delito.<br>° En caso de extravío reportar al:</b><br>
                    <span style="font-size:11px; font-weight:bold;">Tel: 981 102 1212</span>
                </div>
                <div class="rev-vigencia">Vigencia al 31 de diciembre de 2026</div>
            </div>
        </div>
        '''

        st.markdown(f"**Credencial Tamaño Media Carta para: {nombre_formateado} (Emp: {emp_id})**")
        st.markdown(canvas_html, unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px dashed #cbd5e1; margin: 25px 0;'>", unsafe_allow_html=True)

    st.success("💡 **Plantilla en Formato Media Carta:** Las dimensiones se han ampliado a escala real (816x528 px). Ajusta la posición de la foto y el texto en la barra lateral, y al presionar `Ctrl + P` se adaptará perfectamente para su impresión.")

else:
    st.warning("No hay registros en la base de datos.")
