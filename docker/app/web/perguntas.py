import streamlit as st
import subprocess
import os
from db_utils import carregar_dados, inserir_dados

# ==========================================================
# 🔧 Funções auxiliares para processamento
# ==========================================================
def executar_script(script, id_pergunta):
    """Executa scripts Python externos passando o ID da pergunta."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.abspath(os.path.join(base_dir, "..", script))
        result = subprocess.run(
            ["python3", script_path, str(id_pergunta)],
            capture_output=True, text=True, check=True
        )
        st.success(f"✅ Script {script} executado com sucesso!")
        st.text_area("📄 Log de execução:", result.stdout, height=200)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Erro ao executar script {script}:\n{e.stderr or e.stdout}")
        return False

# ==========================================================
# 🔍 Exibição das análises
# ==========================================================
def exibir_analises(perg_id):
    """Exibe tipo de operação, idioma e sentimento relacionados à pergunta."""
    tipo_operacao = carregar_dados(
        """
        SELECT t.id, t.texto 
        FROM analise_tipooperacao a 
        JOIN tipo_operacao t ON t.id = a.id_tipo_operacao 
        WHERE a.id_pergunta = %s
        """, (perg_id,)
    )
    if tipo_operacao:
        st.markdown(f"**⚙️ Tipo de Operação:** `{tipo_operacao[0]['id']}` - {tipo_operacao[0]['texto']}")
    else:
        st.markdown("⚙️ **Tipo de Operação:** _Não identificado_")

    idioma = carregar_dados(
        """
        SELECT i.id, i.nome 
        FROM analise_idioma a 
        JOIN idiomas i ON i.id = a.id_idioma 
        WHERE a.id_pergunta = %s
        """, (perg_id,)
    )
    if idioma:
        st.markdown(f"**🌐 Idioma Detectado:** `{idioma[0]['id']}` - {idioma[0]['nome']}")
    else:
        st.markdown("🌐 **Idioma:** _Não identificado_")

    sentimento = carregar_dados(
        """
        SELECT s.id, s.texto 
        FROM analise_sentimentos a 
        JOIN sentimentos s ON s.id = a.id_sentimento 
        WHERE a.id_pergunta = %s
        """, (perg_id,)
    )
    if sentimento:
        st.markdown(f"**🎭 Sentimento Identificado:** `{sentimento[0]['id']}` - {sentimento[0]['texto']}")
    else:
        st.markdown("🎭 **Sentimento:** _Não identificado_")

# ==========================================================
# 💡 Exibição das respostas
# ==========================================================
def exibir_respostas(perg_id):
    """Exibe todas as respostas associadas à pergunta."""
    respostas = carregar_dados(
        "SELECT texto, data FROM respostas WHERE id_pergunta = %s ORDER BY data DESC",
        (perg_id,)
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

# ==========================================================
# 🔎 Exibição de subperguntas e subrespostas
# ==========================================================
def exibir_subperguntas(perg_id):
    """Exibe subperguntas, subrespostas e botões de reprocessamento."""
    subperguntas = carregar_dados(
        "SELECT id, texto, data, processado FROM subpergunta WHERE id_pergunta = %s ORDER BY data ASC",
        (perg_id,)
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

            # Subresposta
            subresposta = carregar_dados(
                "SELECT id, texto, data FROM subresposta WHERE id_subpergunta = %s ORDER BY data DESC LIMIT 1",
                (sub['id'],)
            )
            with st.expander(f"✍️ Subresposta para Subpergunta ID {sub['id']}"):
                if subresposta:
                    resposta_existente = subresposta[0]['texto']
                    resposta_texto = st.text_area(
                        "Edite a subresposta se necessário:",
                        value=resposta_existente,
                        key=f"subresp_text_{sub['id']}"
                    )
                    if st.button("💾 Salvar Alteração", key=f"subresp_btn_{sub['id']}"):
                        if resposta_texto.strip() and resposta_texto.strip() != resposta_existente.strip():
                            inserir_dados(
                                "UPDATE subresposta SET texto = %s, data = NOW() WHERE id = %s",
                                (resposta_texto.strip(), subresposta[0]['id'])
                            )
                            st.success("✅ Subresposta atualizada com sucesso!")
                            st.rerun()
                else:
                    resposta_texto = st.text_area("Digite a subresposta:", key=f"subresp_text_{sub['id']}")
                    if st.button("💾 Salvar Subresposta", key=f"subresp_nova_btn_{sub['id']}"):
                        if resposta_texto.strip():
                            inserir_dados(
                                "INSERT INTO subresposta (id_pergunta, id_subpergunta, texto) VALUES (%s, %s, %s)",
                                (perg_id, sub["id"], resposta_texto.strip())
                            )
                            st.success("✅ Subresposta salva com sucesso!")
                            st.rerun()

        # Botão de reprocessamento de subperguntas
        if st.button("🔄 Reprocessar Subperguntas", key=f"reproc_{perg_id}"):
            executar_script("processasubpergunta.py", perg_id)
            st.rerun()
    else:
        st.markdown("<div style='margin-left: 40px; color: gray;'>ℹ️ Nenhuma subpergunta registrada.</div>", unsafe_allow_html=True)

# ==========================================================
# 🏷️ Página principal
# ==========================================================
def pagina_perguntas():
    st.header("❓ Perguntas e Respostas")

    if "expanded_pergunta" not in st.session_state:
        st.session_state.expanded_pergunta = None

    # 🔍 Filtros
    st.subheader("🔍 Filtros de Pesquisa")
    col1, col2 = st.columns(2)
    with col1:
        data_inicial = st.date_input("📅 Data Inicial", value=None)
    with col2:
        data_final = st.date_input("📅 Data Final", value=None)
    palavra_chave = st.text_input("🔤 Palavra contida na pergunta", placeholder="Digite parte do texto...")
    status_resposta = st.selectbox("📌 Status da Pergunta", ["Todas", "Com Resposta", "Sem Resposta"])

    # 🔎 Pesquisa
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

    # 🖥️ Resultados
    if perguntas:
        st.subheader("📋 Resultados")
        for perg in perguntas:
            col1, col2, col3, col4, col5 = st.columns([5, 2, 2, 2, 2])
            with col1:
                st.write(f"**{perg['texto']}**")
            with col2:
                st.write("✅ Respondida" if perg["processado"] else "⏳ Pendente")
            with col3:
                if st.button("💬 Ver Detalhes", key=f"resp_{perg['id']}"):
                    st.session_state.expanded_pergunta = perg["id"] if st.session_state.expanded_pergunta != perg["id"] else None
            with col4:
                if not perg["processado"]:
                    if st.button("⚡ Processar", key=f"proc_{perg['id']}"):
                        executar_script("processachatbot.py", perg["id"])
                        st.rerun()
            with col5:
                if st.button("🔄 Reprocessar Tudo", key=f"reproc_all_{perg['id']}"):
                    executar_script("reprocessacomsubpergunta.py", perg["id"])
                    st.rerun()

            if st.session_state.expanded_pergunta == perg["id"]:
                exibir_analises(perg["id"])
                exibir_respostas(perg["id"])
                exibir_subperguntas(perg["id"])
    else:
        st.info("⚠️ Nenhuma pergunta encontrada.")
