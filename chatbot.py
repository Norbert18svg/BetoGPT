import streamlit as st
import groq
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192','llama-3.3-70b-versatile']

def configurar_pagina():
   st.set_page_config(page_title="BetoGPT", page_icon="🤖",)
   st.markdown("""<h1 style="background: linear-gradient(90deg, red, orange, yellow, green, cyan, blue, violet); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 60px; font-family: arial, sans-serif;">BetoGPT</h1>""", unsafe_allow_html=True)






def mostrar_sidebar():
    st.sidebar.title("Elegi un modelo de IA")
    modelo = st.sidebar.selectbox("¿cual elejis ? ", MODELOS, index =0)
    st.write("Has elegido el modelo:", {modelo})
    return modelo



def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)


def inicializacion_estado_chat():
   if "mensajes" not in st.session_state:
        st.session_state.mensajes = []






def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
           

import datetime

if "historial_conversaciones" not in st.session_state:
    st.session_state.historial_conversaciones = {}

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


if st.button("💾 Guardar conversación"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.historial_conversaciones[timestamp] = st.session_state.mensajes.copy()
    st.success("¡Conversación guardada!")


st.sidebar.title("📜 Historial de chats")

conversaciones = list(st.session_state.historial_conversaciones.keys())

if conversaciones:
    seleccion = st.sidebar.selectbox("Elegí una conversación:", conversaciones)

    if st.sidebar.button("🔍 Ver conversación seleccionada"):
        st.session_state.mensajes = st.session_state.historial_conversaciones[seleccion]
        st.success(f"Mostrando chat del: {seleccion}")
else:
    st.sidebar.info("No hay conversaciones guardadas.")



def obtener_mensaje_usuario():
    return st.chat_input("Escribe tu mensaje aquí:")


def  mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)



def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role":role, "content":content})





def mostrar_mensaje_usuario(rule,content): 
    with st.chat_message(rule):
        st.markdown(content)


def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create (
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content


def ejecutar_app():
    configurar_pagina()
    inicializacion_estado_chat()  
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()
    mostrar_historial_chat()
    mensaje_usuario = obtener_mensaje_usuario()


    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje_usuario("user", mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensaje_al_historial("assistant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)




if __name__ == "__main__":
    ejecutar_app()
  



