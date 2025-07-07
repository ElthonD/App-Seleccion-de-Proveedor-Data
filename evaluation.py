import streamlit as st
import sqlite3
import pandas as pd


def createPage():
    DB = "database.db"
    PROVEEDORES = ["KEYRUS", "EON", "MULTIPLICA", "SCANDA"]
    BLOQUES = [
        ("Capacidades Técnicas y Funcionales", [
            "Compatibilidad tecnológica con tu stack actual (bases de datos, lenguajes, herramientas ETL, BI, etc.)",
            "Servicios nativos de datos: calidad y madurez de servicios como BigQuery (GCP), Redshift (AWS), Glue, Dataflow, Dataproc, Pub/Sub, Kinesis, etc.",
            "Gobierno y seguridad de datos: soporte para políticas de acceso, clasificación, cifrado, enmascaramiento, cumplimiento de regulaciones (GDPR, HIPAA, ISO 27001).",
            "Facilidad de integración con sistemas existentes (ERP, CRM, legacy, etc.)",
            "Soporte para multicloud o híbrido, si se requiere.",
            "Automatización y DevOps: herramientas CI/CD, infraestructura como código (Terraform, CloudFormation), gestión de pipelines."
        ]),
        ("Fortaleza y cobertura del proveedor cloud (GCP / AWS)", [
            "Presencia regional y baja latencia (centros de datos cercanos).",
            "SLA y alta disponibilidad (HA) de sus servicios.",
            "Ecosistema de partners y soporte técnico especializado.",
            "Innovación y roadmap: frecuencia de actualización, nuevas capacidades IA/ML, data mesh, etc.",
            "Soporte y alineación con herramientas de gobernanza de datos: catálogo, calidad, linaje (Data Catalog, Glue Data Catalog, Collibra, Alation)."
        ]),
        ("Costo Total de Propiedad (TCO)", [
            "Modelo de precios: por demanda, instancias reservadas, serverless.",
            "Escalabilidad económica: ¿cómo crecen los costos al escalar usuarios, datos, consultas?",
            "Costos ocultos: transferencias de datos, almacenamiento de largo plazo, licencias adicionales.",
            "Facilidad para estimar y controlar el gasto: dashboards, cotizadores, alertas de uso."
        ]),
        ("Gobierno de Datos y Cumplimiento", [
            "Herramientas nativas de gobierno de datos (lineage, metadatos, calidad, permisos).",
            "Soporte para políticas de privacidad y cumplimiento normativo: GDPR, CCPA, SOC 2, ISO, PCI.",
            "Capacidad de auditar accesos y cambios en los datos y en los pipelines."
        ]),
        ("Capacidad de Soporte, Transferencia de Conocimiento y Acompañamiento", [
            "Soporte técnico certificado, en idioma local si es necesario.",
            "Transferencia de conocimiento y entrenamiento: formación, workshops, documentación.",
            "Metodología de implementación: enfoques ágiles, iterativos, enfoque en quick wins.",
            "Capacidad del proveedor para entregar un equipo sólido (arquitectos, data engineers, gobernanza, seguridad)."
        ]),
        ("Reputación, experiencia y casos de éxito", [
            "Experiencia comprobada en proyectos similares.",
            "Clientes de referencia: ¿tienen casos exitosos en tu sector o región?",
            "Reconocimiento en el mercado: participación en evaluaciones de Gartner, Forrester, etc.",
            "Certificaciones de sus consultores (AWS Certified Data Analytics, Google Cloud Professional Data Engineer, etc.)."
        ]),
        ("Capacidades en analítica, IA y ML (valor añadido)", [
            "Integración con herramientas de IA/ML: Vertex AI (GCP), SageMaker (AWS).",
            "Capacidades de analítica en tiempo real o streaming: Dataflow (GCP), Kinesis/Flink (AWS).",
            "Soporte para Data Lakehouse, Mesh, Fabric: arquitectura moderna y flexible."
        ]),
        ("Propuesta Técnica y de Valor", [
            "Claridad de alcance: entregables, fases, arquitectura objetivo.",
            "Tiempo estimado del proyecto: duración, cronograma, hitos.",
            "Plan de sostenibilidad y evolución futura: escalabilidad, portabilidad, vendor lock-in."
        ]),
    ]

    OPCIONES = [
        (1, "No cumple"),
        (2, "Cumple de forma muy limitada"),
        (3, "Cumple parcialmente"),
        (4, "Cumple en gran medida"),
        (5, "Cumple totalmente o excede expectativas")
    ]

    def guardar_respuestas(usuario, proveedor, respuestas):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        for bloque, preguntas in respuestas.items():
            for pregunta, (punt_cuant, punt_cual) in preguntas.items():
                c.execute("""
                    INSERT INTO evaluacion (usuario, proveedor, bloque, pregunta, puntuacion_cuantitativa, puntuacion_cualitativa)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (usuario, proveedor, bloque, pregunta, punt_cuant, punt_cual))
        conn.commit()
        conn.close()

    def descargar_excel(usuario):
        conn = sqlite3.connect(DB)
        df = pd.read_sql_query("SELECT * FROM evaluacion WHERE usuario = ?", conn, params=(usuario,))
        conn.close()
        return df

    def proveedores_pendientes(usuario):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT DISTINCT proveedor FROM evaluacion WHERE usuario = ?", (usuario,))
        evaluados = set(row[0] for row in c.fetchall())
        conn.close()
        return [p for p in PROVEEDORES if p not in evaluados]

    def cuestionario(usuario):
        st.title("Evaluación de Proveedores")
        pendientes = proveedores_pendientes(usuario)
        if not pendientes:
            # Obtener nombre y apellido
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("SELECT nombre, apellido FROM usuarios WHERE usuario = ?", (usuario,))
            row = c.fetchone()
            conn.close()
            nombre, apellido = row if row else (usuario, "")
            st.success(f"Hola, {nombre} {apellido}, ya evaluaste a todos tus proveedores, muchas gracias por tu colaboración.")
            # Descargar Excel con todos los resultados del usuario
            df_resultados = descargar_excel(usuario)
            if not df_resultados.empty:
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_resultados.to_excel(writer, index=False)
                output.seek(0)
                st.download_button(
                    label="Descargar resultados en Excel",
                    data=output,
                    file_name=f"resultados_evaluacion_{usuario}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            return
        proveedor = st.selectbox("Selecciona el proveedor a evaluar", pendientes, key="proveedor_select")
        respuestas = {}
        for bloque, preguntas in BLOQUES:
            st.header(bloque)
            respuestas[bloque] = {}
            for pregunta in preguntas:
                idx = f"{proveedor}_{bloque}_{pregunta}"
                opcion = st.selectbox(
                    pregunta,
                    [o[1] for o in OPCIONES],
                    key=idx
                )
                punt_cuant = next(o[0] for o in OPCIONES if o[1] == opcion)
                respuestas[bloque][pregunta] = (punt_cuant, opcion)
        if st.button("Enviar respuestas", key=f"enviar_{proveedor}"):
            guardar_respuestas(usuario, proveedor, respuestas)
            st.session_state["modal_proveedor"] = proveedor
            st.rerun()

        # Mostrar modal si corresponde
        if st.session_state.get("modal_proveedor"):
            proveedor_modal = st.session_state["modal_proveedor"]
            st.info(f"Evaluación de Proveedor '{proveedor_modal}' culminada, continuar con el siguiente proveedor del listado.")
            # Limpiar modal al siguiente render
            del st.session_state["modal_proveedor"]

    # Obtener usuario de la sesión
    usuario = st.session_state.get("usuario", None)
    if usuario:
        cuestionario(usuario)
    else:
        st.warning("Debes iniciar sesión para acceder a la evaluación.")