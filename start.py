import streamlit as st
import os
import PyPDF2

# Definir los títulos de las páginas según los bloques del PDF
TITULOS = [
    "Introducción",
    "Capacidades Técnicas y Funcionales",
    "Fortaleza y cobertura del proveedor cloud (GCP / AWS)",
    "Costo Total de Propiedad (TCO)",
    "Gobierno de Datos y Cumplimiento",
    "Capacidad de Soporte, Transferencia de Conocimiento y Acompañamiento",
    "Reputación, experiencia y casos de éxito",
    "Capacidades en analítica, IA y ML (valor añadido)",
    "Propuesta Técnica y de Valor"
]

PDF_PATH = os.path.join(os.path.expanduser("~"), "Documents", "Informe Criterios de Valor - Proveedores.pdf")

def extraer_bloques_pdf(pdf_path, titulos):
    bloques = {titulo: "" for titulo in titulos}
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        texto = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    actual = None
    for line in texto.splitlines():
        for titulo in titulos:
            if titulo.lower() in line.lower():
                actual = titulo
                break
        if actual:
            bloques[actual] += line + "\n"
    return bloques

def createPage():
    st.title("Informe de Criterios de Valor - Proveedores")
    bloques = extraer_bloques_pdf(PDF_PATH, TITULOS)
    tab_objs = st.tabs(TITULOS)
    for i, titulo in enumerate(TITULOS):
        with tab_objs[i]:
            st.header(titulo)
            st.write(bloques[titulo] if bloques[titulo] else "Contenido no disponible.")