import streamlit as st
import os

def createPage():
    st.title("Informe de Criterios de Valor - Proveedores")
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf_content", "Informe Criterios de Valor - Proveedores.pdf")
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            base64_pdf = f.read()
            import base64
            b64 = base64.b64encode(base64_pdf).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="800px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            st.info("Si el PDF no se visualiza correctamente, descárgalo desde el siguiente enlace:")
            st.download_button("Descargar PDF", base64_pdf, file_name="Informe Criterios de Valor - Proveedores.pdf", mime="application/pdf")
    else:
        st.error("El archivo PDF no se encuentra en la carpeta 'pdf_content'.")
    
    return True