import streamlit as st
from db_utils import *

st.set_page_config(page_title="Gerenciador IA", layout="wide")
st.sidebar.title("?? Navegação")

if "menu" not in st.session_state:
    st.session_state.menu = "Área"

def set_menu(value):
    st.session_state.menu = value
    st.rerun()

# Botões do menu lateral
st.sidebar.subheader("?? Gerenciamento")
if st.sidebar.button("?? Área"): set_menu("Área")
if st.sidebar.button("?? Grupo"): set_menu("Grupo")
if st.sidebar.button("?? Requisitos"): set_menu("Requisitos")
if st.sidebar.button("? Ações"): set_menu("Ações")
st.sidebar.markdown("---")
if st.sidebar.button("?? Chatbot Inteligente"): set_menu("Chatbot")
if st.sidebar.button("?? Item de Compra"): set_menu("Item de Compra")
if st.sidebar.button("? Perguntas"): set_menu("Perguntas")

# Import dinâmico da tela selecionada
menu = st.session_state.menu
if menu == "Área":
    import area
    area.exibir()
elif menu == "Grupo":
    import grupo
    grupo.exibir()
elif menu == "Requisitos":
    import requisitos
    requisitos.exibir()
elif menu == "Ações":
    import acoes
    acoes.exibir()
elif menu == "Chatbot":
    import chatbot
    chatbot.exibir()
elif menu == "Item de Compra":
    import item_compra
    item_compra.exibir()
elif menu == "Perguntas":
    import perguntas
    perguntas.exibir()
