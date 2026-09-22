import streamlit as st
import pandas as pd
import base64

# Configuración de la página
st.set_page_config(page_title="Plantilla Maestra Oficial - DDUMA", layout="wide")

st.title("🎨 Creador de Plantilla Maestra y Credenciales Oficiales")
st.markdown("Dirección de Desarrollo Urbano y Medio Ambiente (DDUMA) - Alcaldía de Campeche")

# Inicializar DataFrame por defecto
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"NUMERO DE EMPLEADO": 5332, "Nombre completo": "MAY MASS REYNA ANTONIA", "Puesto": "ANALISTA"}
    ])

# ---------------------------------------------------------
# BARRA LATERAL: CONFIGURACIÓN GENERAL Y TEXTOS ILIMITADOS
# ---------------------------------------------------------
st.sidebar.header("🛠️ Controles de Plantilla Maestra")

st.sidebar.subheader("1. Imagen de Fondo (Plantilla Completa Frente y Reverso)")
bg_file = st.sidebar.file_uploader("Sube tu plantilla base (JPG/PNG)", type=["jpg", "jpeg", "png"])
bg_b64 = ""
if bg_file is not None:
    bg_b64 = base64.b64encode(bg_file.getvalue()).decode("utf-8")

st.sidebar.subheader("2. Posición y Tamaño de la Foto")
foto_left = st.sidebar.slider("Posición Izquierda (X %)", 0, 80, 18)
foto_top = st.sidebar.slider("Posición Arriba (Y %)", 0, 80, 24)
foto_width = st.sidebar.slider("Ancho de la Foto (px)", 80, 250, 130)
foto_height = st.sidebar.slider("Alto de la Foto (px)", 100, 300, 160)

# Gestión de Textos Ilimitados
st.sidebar.subheader("3. Textos Personalizados Ilimitados")
if "textos_libres" not in st.session_state:
    st.session_state.textos_libres = [
        {"texto": "Se autoriza al", "x": 30, "y": 50, "size": 11, "color": "#64748b", "bold": True},
        {"texto": "DIRECCIÓN DE DESARROLLO URBANO Y MEDIO AMBIENTE", "x": 12, "y": 74, "size": 9, "color": "#64748b", "bold": True}
    ]

if st.sidebar.button("➕ Agregar Nuevo Texto"):
    st.session_state.textos_libres.append({"texto": "Nuevo Texto", "x": 10, "y": 60, "size": 10, "color": "#334155", "bold": False})

for i, t in enumerate(st.session_state.textos_libres):
    st.sidebar.markdown(f"--- **Texto #{i+1}** ---")
    st.session_state.textos_libres[i]["texto"] = st.sidebar.text_input(f"Contenido #{i+1}", t["texto"], key=f"t_val_{i}")
    st.session_state.textos_libres[i]["x"] = st.sidebar.slider(f"X (%) #{i+1}", 0, 80, t["x"], key=f"t_x_{i}")
    st.session_state.textos_libres[i]["y"] = st.sidebar.slider(f"Y (%) #{i+1}", 0, 95, t["y"], key=f"t_y_{i}")
    st.session_state.textos_libres[i]["size"] = st.sidebar.slider(f"Tamaño (px) #{i+1}", 6, 25, t["size"], key=f"t_size_{i}")
    st.session_state.textos_libres[i]["color"] = st.sidebar.color_picker(f"Color #{i+1}", t["color"], key=f"t_color_{i}")

st.sidebar.markdown("---")
st.sidebar.subheader("4. Cargar Base de Datos y Fotos")
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
st.subheader("🖨️ Vista Previa Fiel al Formato Oficial (Media Carta)")
st.markdown("Visualiza y ajusta cada elemento para obtener un resultado idéntico al gafete institucional.")

if not df.empty:
    
    bg_style = f"background-image: url('data:image/jpeg;base64,{bg_b64}'); background-size: cover; background-position: center;" if bg_b64 else "background-color: #ffffff; border: 2px dashed #cbd5e1;"

    st.markdown(f"""
    <style>
        .master-canvas {{
            width: 816px;
            height: 528px;
            border-radius: 8px;
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
        .side-back {{
            width: 50%;
            height: 100%;
            padding: 30px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
            position: relative;
        }}
        .rev-folio {{ display: inline-block; background-color: #f28c28; color: white; font-size: 11px; font-weight: bold; padding: 3px 12px; border-radius: 4px; }}
        .rev-legal {{ font-size: 7.5px; color: #475569; text-align: justify; line-height: 1.25; }}
        .rev-signs {{ display: flex; justify-content: space-around; font-size: 8px; color: #1e293b; }}
        .rev-sign-line {{ border-top: 1px solid #64748b; width: 130px; margin: 15px auto 2px auto; }}
        .rev-alert-box {{ background-color: #f28c28; color: white; border-radius: 6px; padding: 5px; font-size: 8px; text-align: center; }}
        .rev-vigencia {{ font-size: 10px; font-weight: bold; color: #c2410c; }}
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

        textos_html = ""
        for t in st.session_state.textos_libres:
            txt_contenido = t["texto"].replace("{NOMBRE}", nombre_formateado).replace("{PUESTO}", cargo).replace("{ID}", emp_id)
            textos_html += f'<div style="position: absolute; top: {t["y"]}%; left: {t["x"]}%; font-size: {t["size"]}px; color: {t["color"]}; font-weight: {"bold" if t["bold"] else "normal"}; z-index: 10; text-transform: uppercase;">{txt_contenido}</div>'

        # HTML estructurado estrictamente en una sola línea para evitar problemas de visualización
        canvas_html = f'<div class="master-canvas"><div class="side-front"><div class="canvas-photo">{img_html}</div>{textos_html}</div><div class="side-back"><div><div style="font-size:11px; font-weight:bold; color:#f28c28;">ALCALDÍA DE CAMPECHE</div><span class="rev-folio">Folio &nbsp; 0{emp_id[-3:] if len(emp_id)>=3 else emp_id}/DDUMA/2026</span></div><div class="rev-legal"><b>Esta credencial es válida únicamente para actos de naturaleza indicadas.</b><br>La presente identificación se emite con fundamento en los artículos 14, 16, 115 fracción V, de la Constitución Política de los Estados Unidos Mexicanos; 105 de la Constitución Política del Estado de Campeche; y ordenamientos aplicables de la Dirección de Desarrollo Urbano y Medio Ambiente.</div><div class="rev-signs"><div><div class="rev-sign-line"></div><b>{nombre_formateado}</b><br>Firma del Trabajador</div><div><div class="rev-sign-line"></div><b>Lic. Rosendo Sánchez Preve</b><br>Director de Desarrollo Urbano</div></div><div class="rev-alert-box"><b>° El uso indebido de esta credencial constituye un delito.<br>° En caso de extravío reportar al:</b><br><span style="font-size:9.5px; font-weight:bold;">Tel: 981 102 1212</span></div><div class="rev-vigencia">Vigencia al 31 de diciembre de 2026</div></div></div>'

        st.markdown(f"**Credencial para: {nombre_formateado} (Emp: {emp_id})**")
        st.markdown(canvas_html, unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px dashed #cbd5e1; margin: 25px 0;'>", unsafe_allow_html=True)

    st.success("💡 **Plantilla Actualizada:** El código HTML se ha compactado en una sola línea para que se renderice correctamente en la interfaz gráfica. Presiona `Ctrl + P` para imprimir.")

else:
    st.warning("No hay registros en la base de datos.")
