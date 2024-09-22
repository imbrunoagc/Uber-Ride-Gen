import streamlit as st

def sidebar():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Ir para", ['Home', 'feedbacks', 'Sobre'])
    return page
