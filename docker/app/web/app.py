import streamlit as st
from area import pagina_area
from grupo import pagina_grupo
from requisitos import pagina_requisitos
from acoes import pagina_acoes
from chatbot import pagina_chatbot
from item_compra import pagina_item_compra
from perguntas import pagina_perguntas
from termobusca import pagina_termobusca 
# Importação correta
from face import pagina_face
from email_modulo import pagina_email




# ================== CONFIGURAÇÃO ==================
st.set_page_config(page_title="Gerenciador IA", layout="wide")
st.title("⚙️ Gerenciador de Classificação IA")
st.sidebar.title("📋 Navegação")

# Estado inicial do menu
if "menu" not in st.session_state:
    st.session_state.menu = "Área"

def set_menu(value):
    st.session_state.menu = value
    st.rerun()
    


# ================== MENU LATERAL ==================
st.sidebar.subheader("🗂 Gerenciamento")
if st.sidebar.button("📌 Área"): set_menu("Área")
if st.sidebar.button("👥 Grupo"): set_menu("Grupo")
if st.sidebar.button("📄 Requisitos"): set_menu("Requisitos")
if st.sidebar.button("⚡ Ações"): set_menu("Ações")

st.sidebar.markdown("---")

if st.sidebar.button("🤖 Chatbot Inteligente"): set_menu("Chatbot")
if st.sidebar.button("🛒 Item de Compra"): set_menu("Item de Compra")
if st.sidebar.button("❓ Perguntas"): set_menu("Perguntas")
if st.sidebar.button("🔍 TermoBusca"): 
    set_menu("TermoBusca")    
if st.sidebar.button("📷 Faces"): 
    set_menu("Face")    

if st.sidebar.button("📧 E-mails"): 
    set_menu("Emails")    
    
   

menu = st.session_state.menu

# 🎨 Estilo dos botões
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px !important;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)
 
# ================== ROTAS ==================
if menu == "Área":
    pagina_area()
elif menu == "Grupo":
    pagina_grupo()
elif menu == "Requisitos":
    pagina_requisitos()
elif menu == "Ações":
    pagina_acoes()
elif menu == "Chatbot":
    pagina_chatbot()
elif menu == "Item de Compra":
    pagina_item_compra()
elif menu == "Perguntas":
    pagina_perguntas()    
elif menu == "TermoBusca":
    pagina_termobusca()
elif menu == "Face":
    pagina_face()    
elif menu == "Emails":
    pagina_email()    
    
