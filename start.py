import streamlit as st
import os

def createPage():
    st.title("Informe de Criterios de Valor - Proveedores")

    folder_path = "pdf_content"
    pages = sorted([img for img in os.listdir(folder_path) if img.endswith(".png")])

    if not pages:
        st.error("No se encontraron imágenes del PDF.")
        return

    for page in pages:
        st.image(os.path.join(folder_path, page), use_column_width=True)

    with open("pdf_content/Informe Criterios de Valor - Proveedores.pdf", "rb") as f:
        st.download_button("Descargar PDF", f.read(), file_name="Informe Criterios de Valor - Proveedores.pdf", mime="application/pdf")

    return True