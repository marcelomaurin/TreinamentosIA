import streamlit as st
from db_utils import carregar_dados, inserir_dados

def pagina_grupo():
    st.header("?? Gerenciar Grupos")
    grupos = carregar_dados("SELECT * FROM grupo")
    st.table(grupos)

    areas = carregar_dados("SELECT id, nome FROM area")
    area_map = {a["nome"]: a["id"] for a in areas}

    with st.form("novo_grupo"):
        st.subheader("? Novo Grupo")
        area_sel = st.selectbox("Área", list(area_map.keys()))
        nome = st.text_input("Nome do Grupo")
        papel_ia = st.text_area("Papel da IA")
        criterio = st.text_area("Critério de Identificação")
        if st.form_submit_button("Salvar"):
            inserir_dados("INSERT INTO grupo (id_area, nome, papel_ia, criterio_identificacao) VALUES (%s,%s,%s,%s)",
                          (area_map[area_sel], nome, papel_ia, criterio))
            st.success("? Grupo adicionado!")
