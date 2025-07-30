import streamlit as st
from db_utils import carregar_dados, inserir_dados, excluir_dados

def pagina_area():
    st.header("?? Gerenciar Áreas")

    dados = carregar_dados("SELECT * FROM area ORDER BY id DESC")
    if dados:
        st.table(dados)

    with st.form("nova_area"):
        st.subheader("? Adicionar Nova Área")
        nome = st.text_input("Nome da Área")
        papel_ia = st.text_area("Papel da IA")
        criterio = st.text_area("Critério de Identificação")
        if st.form_submit_button("Salvar"):
            inserir_dados("INSERT INTO area (nome, papel_ia, criterio_identificacao) VALUES (%s,%s,%s)",
                          (nome, papel_ia, criterio))
            st.success("? Área adicionada!")

    excluir_id = st.number_input("ID para excluir", min_value=0, step=1)
    if st.button("Excluir Área"):
        excluir_dados("area", excluir_id)
        st.success("?? Área excluída!")
