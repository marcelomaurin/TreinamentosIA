import streamlit as st
from db_utils import carregar_dados, inserir_dados

def pagina_acoes():
    st.header("?? Gerenciar Ações")
    acoes = carregar_dados("SELECT * FROM acoes")
    st.table(acoes)

    reqs = carregar_dados("SELECT id, descricao FROM requisitos")
    req_map = {r["descricao"]: r["id"] for r in reqs}

    with st.form("nova_acao"):
        st.subheader("? Nova Ação")
        req_sel = st.selectbox("Requisito", list(req_map.keys()))
        nome = st.text_input("Nome da Ação")
        criterio = st.text_area("Critério de Disparo")
        detalhes = st.text_area("Detalhes")
        if st.form_submit_button("Salvar"):
            inserir_dados("INSERT INTO acoes (id_requisito, nome, criterio_disparo, detalhes_acao) VALUES (%s,%s,%s,%s)",
                          (req_map[req_sel], nome, criterio, detalhes))
            st.success("? Ação adicionada!")
