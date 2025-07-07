import streamlit as st
import os

def createPage():
    st.title("Informe de Criterios de Valor - Proveedores")
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf_content", "Informe Criterios de Valor - Proveedores.pdf")
    if os.path.exists(pdf_path):
        st.markdown(f'<iframe src="file:///{pdf_path}" width="100%" height="800px" type="application/pdf"></iframe>', unsafe_allow_html=True)
        st.info("Si el PDF no se visualiza correctamente, descárgalo desde el siguiente enlace:")
        with open(pdf_path, "rb") as f:
            st.download_button("Descargar PDF", f, file_name="Informe Criterios de Valor - Proveedores.pdf", mime="application/pdf")
    else:
        st.error("El archivo PDF no se encuentra en la carpeta 'pdf_content'.")
    
    return True