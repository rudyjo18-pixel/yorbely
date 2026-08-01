import streamlit as st
import json
import os

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

# --- ENCABEZADO CON LOGO EN LA ESQUINA ---
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🎨 Registro de Citas de Pintura")
    st.write("Hola preciosa, aquí puedes agendar y consultar todas tus ideas y proyectos.")

with col2:
    # Aquí cargamos la imagen en la esquina derecha del título
    st.image("https://i.imgur.com/ihYjSE8.jpeg", use_container_width=True)

st.markdown("---")

fecha_lugar = cargar_citas()

# Menú lateral normal
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