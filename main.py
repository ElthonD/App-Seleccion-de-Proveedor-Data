import streamlit as st
import sqlite3
import bcrypt


import app
import admin

DB = "database.db"

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def login():
    import os
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "GIM Desarrollos Logo.png")
    st.markdown("""
        <div style='width:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:30px;'>
    """, unsafe_allow_html=True)
    if os.path.exists(logo_path):
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; width: 100%;'>
        """, unsafe_allow_html=True)
        st.markdown(f"<img src='data:image/png;base64,{get_base64_of_bin_file(logo_path)}' width='120' style='display:block;margin-left:auto;margin-right:auto;' />", unsafe_allow_html=True)
        st.markdown("""</div>""", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='margin-top:10px; margin-bottom:25px; text-align:center;'>🔐 Portal de Selección de Proveedor<br>Iniciativa: Arquitectura y Gobierno de Datos</h3>
        </div>
    """, unsafe_allow_html=True)
    # Campos de login centrados y pequeños
    col1, col2, col3 = st.columns([2,2,2])
    with col2:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        usuario = st.text_input("Usuario", key="login_usuario")
        password = st.text_input("Contraseña", type="password", key="login_password")
        login_btn = st.button("Ingresar", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
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

def get_base64_of_bin_file(bin_file):
    import base64
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
    # Campos de login centrados y pequeños
    col1, col2, col3 = st.columns([2,2,2])
    with col2:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        usuario = st.text_input("Usuario", key="login_usuario")
        password = st.text_input("Contraseña", type="password", key="login_password")
        login_btn = st.button("Ingresar")
        st.markdown("</div>", unsafe_allow_html=True)
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
        # Mostrar logo usando st.image para evitar problemas de ruta
        import os
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "GIM Desarrollos Logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=160)
        st.markdown(
            f"""
            <div class='stSidebarUserBlock' style='text-align:center;'>
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