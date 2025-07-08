import streamlit as st
import os
from streamlit_book import page_navigator

def createPage():
    st.title("📘 Informe de Criterios de Valor - Proveedores")

    folder_path = "pdf_content"
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])

    total_pages = len(image_files)

    if total_pages == 0:
        st.error("No se encontraron imágenes del PDF en la carpeta 'pdf_content'.")
        return

    # Página actual con navegación tipo libro
    current_page = page_navigator(total_pages=total_pages, key="book_navigation")

    st.image(
        os.path.join(folder_path, image_files[current_page - 1]),
        caption=f"Página {current_page}",
        use_container_width=True
    )

    # Opción para descargar el PDF completo
    with open(os.path.join(folder_path, "Informe Criterios de Valor - Proveedores.pdf"), "rb") as f:
        st.download_button(
            label="📥 Descargar PDF completo",
            data=f.read(),
            file_name="Informe Criterios de Valor - Proveedores.pdf",
            mime="application/pdf"
        )
    return True