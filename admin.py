import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import plotly.express as px

DB = "database.db"

def registrar_usuario():
    st.subheader("Registrar nuevo usuario")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    usuario = st.text_input("Usuario (formato: nombre.apellido)")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["user", "admin"])
    if st.button("Registrar"):
        if not (nombre and apellido and usuario and password):
            st.warning("Todos los campos son obligatorios.")
            return
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("INSERT INTO usuarios (nombre, apellido, usuario, contraseña, rol) VALUES (?, ?, ?, ?, ?)",
                      (nombre, apellido, usuario, hash_pw, rol))
            conn.commit()
            conn.close()
            st.success(f"Usuario {usuario} registrado correctamente.")
        except sqlite3.IntegrityError:
            st.error("El usuario ya existe.")

def graficos_votaciones():
    st.subheader("Histograma de votaciones por bloque y total")
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM evaluacion", conn)
    conn.close()
    if df.empty:
        st.info("Aún no hay evaluaciones registradas.")
        return
    # Histograma general
    st.markdown("### Histograma General")
    fig_total = px.histogram(df, x="puntuacion_cuantitativa", color="proveedor", barmode="group",
                            labels={"puntuacion_cuantitativa": "Puntuación Cuantitativa"},
                            title="Distribución de puntuaciones por proveedor")
    st.plotly_chart(fig_total, use_container_width=True)
    # Histograma por bloque
    st.markdown("### Histograma por Bloque")
    bloques = df["bloque"].unique()
    for bloque in bloques:
        st.markdown(f"**{bloque}**")
        df_bloque = df[df["bloque"] == bloque]
        fig = px.histogram(df_bloque, x="puntuacion_cuantitativa", color="proveedor", barmode="group",
                           labels={"puntuacion_cuantitativa": "Puntuación Cuantitativa"},
                           title=f"Puntuaciones en {bloque}")
        st.plotly_chart(fig, use_container_width=True)

def reset_cuestionario():
    st.subheader("Reiniciar intento de cuestionario para usuario")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT usuario, nombre, apellido FROM usuarios WHERE rol = 'user'")
    usuarios = c.fetchall()
    conn.close()
    if usuarios:
        user_dict = {f"{u[1]} {u[2]} ({u[0]})": u[0] for u in usuarios}
        selected = st.selectbox("Selecciona el usuario a reiniciar", list(user_dict.keys()))
        if st.button("Reiniciar cuestionario", key="reset_cuestionario"):
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("DELETE FROM evaluacion WHERE usuario = ?", (user_dict[selected],))
            conn.commit()
            conn.close()
            st.success(f"Se ha reiniciado el intento de cuestionario para {selected}.")
    else:
        st.info("No hay usuarios tipo 'user' registrados.")

def createPage():
    st.title("Panel de Administración")
    tab1, tab2, tab3 = st.tabs(["Registrar Usuario", "Gráficos de Evaluaciones", "Reiniciar Cuestionario"])
    with tab1:
        registrar_usuario()
    with tab2:
        graficos_votaciones()
    with tab3:
        reset_cuestionario()
