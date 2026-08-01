import streamlit as st
import json
import os
import base64

# --- CONFIGURACIÓN DEL FONDO ---
FONDO_URL = "https://i.imgur.com/ihYjSE8.jpeg" 

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_from_url(url):
    """
    Inyecta estilos CSS para el fondo y ajusta los contrastes de los textos y cajas.
    """
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("{url}");
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             background-attachment: local;
         }}
         
         /* Fondo semitransparente para el contenedor principal para que resalte el texto */
         .stApp > div {{
             background-color: rgba(255, 255, 255, 0.85); 
             padding: 25px;
             border-radius: 12px;
         }}
         
         /* Forzar color oscuro y negrita para títulos, subtítulos y párrafos */
         h1, h2, h3, p, label, span, div[data-testid="stMarkdownContainer"] > p {{
             color: #2C2C2C !important;
             font-weight: bold !important;
         }}
         
         /* Ajuste para que las cajas de texto sean blancas y legibles */
         input, textarea {{
             background-color: #FFFFFF !important;
             color: #2C2C2C !important;
         }}
         
         /* Fondo de la barra lateral */
         [data-testid="stSidebar"] {{
             background-color: rgba(255, 255, 255, 0.9) !important;
         }}
         
         </style>
         """,
         unsafe_allow_html=True
     )

# --- FIN CONFIGURACIÓN FONDO ---

DATA_FILE = "citas_pintura.json"

def cargar_citas():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_citas(citas):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(citas, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="Citas de Pintura", page_icon="🎨", layout="centered")

# Aplicar el fondo y los estilos mejorados
set_bg_from_url(FONDO_URL)

st.title("🎨 Registro de Citas de Pintura")
st.write("Hola preciosa, aquí puedes agendar y consultar todas tus ideas y proyectos.")

fecha_lugar = cargar_citas()

menu = st.sidebar.selectbox("Menú de opciones", ["Agendar Cita", "Consultar Citas"])

if menu == "Agendar Cita":
    st.subheader("Agregar una nueva cita o cuadro")
    
    with st.form("form_cita"):
        descripcion = st.text_input("Descripción de la cita: ")
        fecha = st.date_input("Fecha de la cita:")
        lugar = st.text_input("Lugar:")
        
        boton_enviar = st.form_submit_button("Guardar Cita")
        
        if boton_enviar:
            if descripcion.strip() == "":
                st.error("Por favor, ingresa una descripción válida.")
            else:
                fecha_lugar[descripcion] = {
                    "fecha": str(fecha),
                    "lugar": lugar
                }
                guardar_citas(fecha_lugar)
                st.success(f"¡Listo, mi vida! Registrada la cita: {descripcion}")

elif menu == "Consultar Citas":
    st.subheader("Tus citas y proyectos agendados")
    
    if not fecha_lugar:
        st.info("No hay citas registradas todavía. ¡Ve a agendar una!")
    else:
        for descripcion, datos in list(fecha_lugar.items()):
            with st.container():
                st.markdown(f"**📌 {descripcion}**")
                st.write(f"📅 **Fecha:** {datos['fecha']} | 📍 **Lugar:** {datos['lugar']}")
                
                if st.button("🗑️ Borrar cita", key=f"btn_{descripcion}") and descripcion in fecha_lugar:
                    del fecha_lugar[descripcion]
                    guardar_citas(fecha_lugar)
                    st.success(f"¡Cita borrada: {descripcion}!")
                    st.rerun()
                        
                st.markdown("---")
        
        st.info("🎨✨ Recuerda llevar tu bolso, tus papeles, tus pinturas y todo lo demás. ¡Te amo! ❤️")