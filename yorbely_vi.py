import streamlit as st
import json
import os

# Nombre del archivo donde se guardarán las citas de forma persistente
DATA_FILE = "citas_pintura.json"

def cargar_citas():
    """Carga las citas guardadas desde el archivo JSON si existe."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_citas(citas):
    """Guarda el diccionario de citas en el archivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(citas, f, ensure_ascii=False, indent=4)

# Configuración inicial de la página en Streamlit
st.set_page_config(page_title="Citas de Pintura", page_icon="🎨", layout="centered")

st.title("🎨 Registro de Citas de Pintura")
st.write("Hola preciosa, aquí puedes agendar y consultar todas tus ideas y proyectos.")

# Cargar los datos actuales almacenados
fecha_lugar = cargar_citas()

# Crear un menú lateral para elegir entre registrar o consultar
menu = st.sidebar.selectbox("Menú de opciones", ["Agendar Cita", "Consultar Citas"])

if menu == "Agendar Cita":
    st.subheader("Agregar una nueva cita o cuadro")
    
    # Formulario para que se vea ordenado
    with st.form("form_cita"):
        descripcion = st.text_input("Descripción de la cita / Idea del cuadro:")
        fecha = st.date_input("Fecha de la cita:")
        lugar = st.text_input("Lugar:")
        
        boton_enviar = st.form_submit_button("Guardar Cita")
        
        if boton_enviar:
            if descripcion.strip() == "":
                st.error("Por favor, ingresa una descripción válida.")
            else:
                # Guardamos usando la descripción como llave
                fecha_lugar[descripcion] = {
                    "fecha": str(fecha),
                    "lugar": lugar
                }
                guardar_citas(fecha_lugar)
                
                # Mensaje de éxito limpio al registrar
                st.success(f"¡Listo, mi vida! Registrada la cita: {descripcion}")

elif menu == "Consultar Citas":
    st.subheader("Tus citas y proyectos agendados")
    
    if not fecha_lugar:
        st.info("No hay citas registradas todavía. ¡Ve a agendar una!")
    else:
        # Recorremos el diccionario
        for descripcion, datos in fecha_lugar.items():
            with st.container():
                st.markdown(f"**📌 {descripcion}**")
                st.write(f"📅 **Fecha:** {datos['fecha']} | 📍 **Lugar:** {datos['lugar']}")
                st.markdown("---")
        
        # Mensaje tierno al momento de consultar
        st.info("🎨✨ Recuerda llevar tu bolso, tus papeles, tus pinturas y todo lo demás. ¡Te amo! ❤️")