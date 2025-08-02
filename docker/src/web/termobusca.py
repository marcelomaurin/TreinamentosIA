import streamlit as st
from db_utils import carregar_dados, inserir_dados, excluir_dados

def pagina_termobusca():
    st.header("🔍 TermoBusca - Gerenciamento de Termos")

    # Estado inicial
    if "expanded_termo" not in st.session_state:
        st.session_state.expanded_termo = None

    # 📋 Listagem dos termos
    termos = carregar_dados("SELECT id, termo, texto, qtd_videos, processado, ativo, data_cadastro FROM termobusca ORDER BY data_cadastro DESC")

    st.subheader("📋 Termos Cadastrados")
    for termo in termos:
        col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
        with col1: st.write(f"**{termo['termo']}**")
        with col2: st.write(f"🎥 Vídeos: {termo['qtd_videos']}")
        with col3: st.write("✅ Processado" if termo["processado"] else "⏳ Pendente")
        with col4: st.write("🟢 Ativo" if termo["ativo"] else "🔴 Inativo")
        with col5:
            if st.button("🗑 Excluir", key=f"del_{termo['id']}"):
                excluir_dados("termobusca", termo["id"])
                st.rerun()

    st.markdown("---")

    # ➕ Cadastro de novo termo
    st.subheader("➕ Adicionar Novo Termo")
    with st.form("form_termobusca"):
        termo = st.text_input("📝 Termo de Busca")
        texto = st.text_input("🔤 Texto (compatível com Python)")
        qtd_videos = st.number_input("🎥 Quantidade de Vídeos", min_value=1, max_value=10, value=3, step=1)
        id_origem = st.number_input("🔗 ID da Origem", min_value=1, step=1)

        if st.form_submit_button("💾 Salvar"):
            if termo and texto:
                inserir_dados(
                    "INSERT INTO termobusca (termo, texto, qtd_videos, processado, id_origem) VALUES (%s,%s,%s,0,%s)",
                    (termo, texto, qtd_videos, id_origem)
                )
                st.success("✅ Termo adicionado com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios.")
