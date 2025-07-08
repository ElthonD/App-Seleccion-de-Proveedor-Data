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
    #st.subheader("Histograma de votaciones por bloque y total")
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM evaluacion", conn)
    conn.close()
    if df.empty:
        st.info("Aún no hay evaluaciones registradas.")
        return

    # --- Tabla tipo semáforo con lógica de ponderación y totales ---
    st.markdown("### Tabla de Evaluación por Proveedor y Criterio")
    import plotly.graph_objects as go
    bloques = [
        ("Capacidades Técnicas y Funcionales", 6, 30, 20),
        ("Fortaleza y cobertura del proveedor cloud (GCP / AWS)", 5, 25, 5),
        ("Costo Total de Propiedad (TCO)", 4, 20, 10),
        ("Gobierno de Datos y Cumplimiento", 3, 15, 20),
        ("Capacidad de Soporte, Transferencia de Conocimiento y Acompañamiento", 4, 20, 10),
        ("Reputación, experiencia y casos de éxito", 4, 20, 5),
        ("Capacidades en analítica, IA y ML (valor añadido)", 3, 15, 15),
        ("Propuesta Técnica y de Valor", 3, 15, 15)
    ]
    proveedores = sorted(df['proveedor'].unique().tolist())
    if not proveedores:
        st.info("No hay criterios evaluados para mostrar la tabla semáforo.")
        return
    matriz = {p: [] for p in proveedores}
    for bloque, num_preg, max_punt, ponderacion in bloques:
        for p in proveedores:
            df_filtrado = df[(df['bloque'] == bloque) & (df['proveedor'] == p)]
            if not df_filtrado.empty:
                punt_total = df_filtrado['puntuacion_cuantitativa'].sum()
                promedio = punt_total / num_preg if num_preg else 0
                resultado_pond = promedio * (ponderacion / 100)
                matriz[p].append(round(resultado_pond, 2))
            else:
                matriz[p].append(None)
    totales = []
    for p in proveedores:
        total = sum([v for v in matriz[p] if v is not None])
        totales.append(round(total, 2))
    def color_text(val):
        if val is None:
            return 'black'
        if val < 2:
            return 'red'
        elif val < 4:
            return 'orange'
        else:
            return 'green'
    # Construir tabla Plotly
    headers = ["Criterio", "Peso (%)"] + proveedores
    data = [
        [b[0] for b in bloques] + ["TOTAL FINAL"],
        [b[3] for b in bloques] + ["-"],
    ]
    for p in proveedores:
        col = matriz[p] + [totales[proveedores.index(p)]]
        data.append(col)
    # Colores de texto: solo la fila de totales (última fila de cada columna de proveedor) lleva color, el resto negro
    cell_font_colors = [
        ['black']*(len(bloques)+1),  # criterios
        ['black']*(len(bloques)+1),  # ponderaciones
    ]
    for idx, p in enumerate(proveedores):
        colores = ['black']*len(bloques) + [color_text(totales[idx])]
        cell_font_colors.append(colores)
    # Fondo blanco
    fill_colors = [['white']*(len(bloques)+1) for _ in range(2+len(proveedores))]
    # Centrar todas las columnas excepto la primera
    align_header = ['left'] + ['center'] * (len(headers) - 1)
    align_cells = ['left'] + ['center'] * (len(headers) - 1)
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headers,
            fill_color='darkblue',
            font=dict(color='white', size=12),
            align=align_header
        ),
        cells=dict(
            values=data,
            fill_color=fill_colors,
            align=align_cells,
            font=dict(size=11, color=cell_font_colors),
            format=[None, None] + [".2f"]*len(proveedores)
        )
    )])
    st.plotly_chart(fig, use_container_width=True)

    # Histograma general
    st.markdown("### Histograma General")
    fig_total = px.histogram(
        df,
        x="puntuacion_cualitativa",
        color="proveedor",
        barmode="group",
        labels={
            "puntuacion_cualitativa": "Puntuación Cualitativa",
            "count": "Resultados",
            "y": "Resultados"
        },
        title="Distribución de puntuaciones cualitativas por proveedor"
    )
    st.plotly_chart(fig_total, use_container_width=True)
    # Histograma por bloque
    st.markdown("### Histograma por Bloque")
    bloques = df["bloque"].unique()
    for bloque in bloques:
        st.markdown(f"**{bloque}**")
        df_bloque = df[df["bloque"] == bloque]
        fig = px.histogram(
            df_bloque,
            x="puntuacion_cualitativa",
            color="proveedor",
            barmode="group",
            labels={
                "puntuacion_cualitativa": "Puntuación Cualitativa",
                "count": "Resultados",
                "y": "Resultados"
            },
            title=f"Puntuaciones cualitativas en {bloque}"
        )
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
    tab1, tab2, tab3, tab4 = st.tabs(["Registrar Usuario", "Gráficos de Evaluaciones", "Reiniciar Cuestionario", "Cambiar Contraseña"])
    with tab1:
        registrar_usuario()
    with tab2:
        graficos_votaciones()
    with tab3:
        reset_cuestionario()
    with tab4:
        cambiar_contrasena()

# Nueva función para cambiar contraseña de cualquier usuario
def cambiar_contrasena():
    st.subheader("Cambiar contraseña de usuario")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT usuario FROM usuarios")
    usuarios = [row[0] for row in c.fetchall()]
    conn.close()
    usuario_sel = st.selectbox("Selecciona el usuario", usuarios)
    nueva_contra = st.text_input("Nueva contraseña", type="password")
    if st.button("Actualizar contraseña"):
        if not nueva_contra:
            st.warning("Debes ingresar una nueva contraseña.")
            return
        hash_pw = bcrypt.hashpw(nueva_contra.encode(), bcrypt.gensalt()).decode()
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("UPDATE usuarios SET contraseña = ? WHERE usuario = ?", (hash_pw, usuario_sel))
        conn.commit()
        conn.close()
        st.success(f"Contraseña actualizada para {usuario_sel}.")
