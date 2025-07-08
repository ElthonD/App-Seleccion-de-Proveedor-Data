from pdf2image import convert_from_path
from PIL import Image
import streamlit as st
import os
def createPage():
    st.title("Informe de Criterios de Valor - Proveedores")

    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf_content", "Informe Criterios de Valor - Proveedores.pdf")
    
    if os.path.exists(pdf_path):
        st.info("Vista previa del PDF (modo imagen):")
        pages = convert_from_path(pdf_path, dpi=150)
        for i, page in enumerate(pages):
            st.image(page, caption=f"Página {i+1}")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Descargar PDF",
                data=f.read(),
                file_name="Informe Criterios de Valor - Proveedores.pdf",
                mime="application/pdf"
            )
    else:
        st.error("El archivo PDF no se encuentra en la carpeta 'pdf_content'.")
    
    return True