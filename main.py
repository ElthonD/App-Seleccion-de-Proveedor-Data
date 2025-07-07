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
                    st.experimental_rerun()
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("Usuario no encontrado.")

# Mostrar login siempre primero y redirigir según el rol
if "usuario" not in st.session_state or "rol" not in st.session_state:
    login()
elif st.session_state.get("rol") == "admin":
    admin.run()
else:
    app.run()