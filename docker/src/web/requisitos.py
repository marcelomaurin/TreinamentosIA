import streamlit as st
from db_utils import carregar_dados, inserir_dados

def pagina_requisitos():
    st.header("?? Gerenciar Requisitos")
    reqs = carregar_dados("SELECT * FROM requisitos")
    st.table(reqs)

    grupos = carregar_dados("SELECT id, nome FROM grupo")
    grupo_map = {g["nome"]: g["id"] for g in grupos}

    with st.form("novo_req"):
        st.subheader("? Novo Requisito")
        grupo_sel = st.selectbox("Grupo", list(grupo_map.keys()))
        descricao = st.text_area("Descrição")
        criterio = st.text_area("Critério de Identificação")
        info = st.text_area("Informação Necessária")
        if st.form_submit_button("Salvar"):
            inserir_dados("INSERT INTO requisitos (id_grupo, descricao, criterio_identificacao, informacao_necessaria) VALUES (%s,%s,%s,%s)",
                          (grupo_map[grupo_sel], descricao, criterio, info))
            st.success("? Requisito adicionado!")
