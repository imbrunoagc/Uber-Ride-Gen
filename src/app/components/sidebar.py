import streamlit as st

def sidebar():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Ir para", ['Home', 'Análises', 'Sobre'])
    return page
