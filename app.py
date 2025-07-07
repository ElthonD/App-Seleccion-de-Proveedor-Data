
# Este archivo solo debe mostrar el menú y las páginas si el usuario ya está autenticado
import streamlit as st
from streamlit_option_menu import option_menu
import start, evaluation # Importar páginas acá

def show_menu():
    st.set_page_config(page_title="GIM Desarrollos", layout="wide")
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    v_menu=["Inicio", "Evaluación"]
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Evaluación"],
        icons=["house", "card-checklist"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "10px", "background-color": "#fafafa"},
            "icon": {"font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "salmon"},
            "nav-link-selected": {"background-color": "tomato"},
        }
    )
    if selected=="Inicio":
        start.createPage()
    if selected=="Evaluación":
        evaluation.createPage()