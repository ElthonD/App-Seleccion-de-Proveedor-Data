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

    if st.button("Ingresar"):
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
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
        else:
            st.error("Usuario no encontrado.")

# Mostrar login siempre primero
if "usuario" not in st.session_state:
    login()
else:
    if st.session_state.get("rol") == "admin":
        admin.run()
    else:
        app.run()