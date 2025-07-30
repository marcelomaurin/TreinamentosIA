import streamlit as st
from db_utils import carregar_dados

def pagina_perguntas():
    st.header("❓ Perguntas e Respostas")

    if "expanded_pergunta" not in st.session_state:
        st.session_state.expanded_pergunta = None

    st.subheader("🔍 Filtros de Pesquisa")
    col1, col2 = st.columns(2)
    with col1:
        data_inicial = st.date_input("📅 Data Inicial", value=None)
    with col2:
        data_final = st.date_input("📅 Data Final", value=None)

    palavra_chave = st.text_input("🔤 Palavra contida na pergunta", placeholder="Digite parte do texto...")
    status_resposta = st.selectbox("📌 Status da Pergunta", ["Todas", "Com Resposta", "Sem Resposta"])

    if st.button("🔎 Pesquisar"):
        query = "SELECT id, data, texto, processado FROM perguntas WHERE 1=1"
        params = []
        if data_inicial:
            query += " AND DATE(data) >= %s"
            params.append(data_inicial)
        if data_final:
            query += " AND DATE(data) <= %s"
            params.append(data_final)
        if palavra_chave:
            query += " AND texto LIKE %s"
            params.append(f"%{palavra_chave}%")
        if status_resposta == "Com Resposta":
            query += " AND processado = 1"
        elif status_resposta == "Sem Resposta":
            query += " AND processado = 0"
        query += " ORDER BY data DESC"
        perguntas = carregar_dados(query, tuple(params))
    else:
        perguntas = carregar_dados("SELECT id, data, texto, processado FROM perguntas ORDER BY data DESC")

    if perguntas:
        st.subheader("📋 Resultados")
        for perg in perguntas:
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(f"**{perg['texto']}**")
            with col2:
                st.write("✅ Respondida" if perg["processado"] else "⏳ Pendente")
            with col3:
                if st.button("💬 Ver Detalhes", key=f"resp_{perg['id']}"):
                    if st.session_state.expanded_pergunta == perg["id"]:
                        st.session_state.expanded_pergunta = None
                    else:
                        st.session_state.expanded_pergunta = perg["id"]

            # Detalhes da pergunta expandida
            if st.session_state.expanded_pergunta == perg["id"]:
                # Mostrar respostas
                respostas = carregar_dados(
                    "SELECT texto, data FROM respostas WHERE id_pergunta = %s ORDER BY data DESC",
                    (perg["id"],)
                )
                if respostas:
                    for resp in respostas:
                        st.markdown(f"""
                            <div style="margin-left: 40px; border-left: 2px solid #4CAF50; padding-left: 15px; margin-bottom: 8px;">
                                <b>💡 Resposta:</b> {resp['texto']}<br>
                                <i>📅 {resp['data']}</i>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-left: 40px; color: gray;'>⚠️ Nenhuma resposta encontrada.</div>", unsafe_allow_html=True)

                # Mostrar subperguntas
                subperguntas = carregar_dados(
                    "SELECT id, texto, data, processado FROM subpergunta WHERE id_pergunta = %s ORDER BY data ASC",
                    (perg["id"],)
                )
                if subperguntas:
                    st.markdown("<div style='margin-left: 20px; margin-top: 10px;'><b>🔎 Subperguntas:</b></div>", unsafe_allow_html=True)
                    for sub in subperguntas:
                        st.markdown(f"""
                            <div style="margin-left: 60px; border-left: 2px dashed #999; padding-left: 15px; margin-bottom: 8px;">
                                <b>❓ Subpergunta:</b> {sub['texto']}<br>
                                <i>📅 {sub['data']}</i> | {'✅ Respondida' if sub['processado'] else '⏳ Pendente'}
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-left: 40px; color: gray;'>ℹ️ Nenhuma subpergunta registrada.</div>", unsafe_allow_html=True)
    else:
        st.info("⚠️ Nenhuma pergunta encontrada.")

