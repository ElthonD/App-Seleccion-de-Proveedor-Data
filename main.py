import streamlit as st
import sqlite3
import bcrypt


import app
import admin

DB = "database.db"

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def login():
    st.title("🔐 Portal de Selección de Proveedor - Iniciativa: Arquitectura y Gobierno de Datos")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login_btn = st.button("Ingresar")
    if login_btn or ("usuario" not in st.session_state):
        if login_btn:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute("SELECT rol, contraseña FROM usuarios WHERE usuario = ?", (usuario,))
            result = cursor.fetchone()
            conn.close()
            if result:
                rol, stored_hash = result
                if verify_password(password, stored_hash.encode()):
                    st.session_state["usuario"] = usuario
                    st.session_state["rol"] = rol
                    st.success("Inicio de sesión exitoso. Redirigiendo...")
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("Usuario no encontrado.")

# Mostrar login siempre primero y redirigir según el rol
def logout_button():
    with st.sidebar:
        usuario = st.session_state.get("usuario", "")
        nombre, apellido = "", ""
        if usuario:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("SELECT nombre, apellido FROM usuarios WHERE usuario = ?", (usuario,))
            row = c.fetchone()
            conn.close()
            if row:
                nombre, apellido = row
        st.markdown(
            f"""
            <div style='text-align:center;margin-bottom:10px;'>
                <img src='app/img/GIM Desarrollos Logo.png' width='160' style='margin-bottom:20px;margin-top:10px;' />
            </div>
            <div class='stSidebarUserBlock'>
                <span class='user-name'>Hola, {nombre} {apellido}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Cerrar sesión", key="logout_btn"):
            st.session_state.clear()
            st.rerun()

if "usuario" not in st.session_state or "rol" not in st.session_state:
    login()
elif st.session_state.get("rol") == "admin":
    logout_button()
    admin.createPage()
else:
    logout_button()
    app.show_menu()