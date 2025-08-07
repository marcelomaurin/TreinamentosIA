import os
import streamlit as st
import subprocess
import time
from db_utils import conectar_mysql, carregar_dados

def pagina_chatbot():
    st.title("🤖 Chatbot Inteligente")

    # Histórico minimalista
    if "historico" not in st.session_state:
        st.session_state.historico = []

    # Exibe o histórico
    st.subheader("💬 Conversa")
    for item in st.session_state.historico:
        st.markdown(f"🧑 **Você:** {item['pergunta']}")
        st.markdown(f"🤖 **IA:** {item['resposta']}")
        st.markdown("---")

    # Campo de entrada da pergunta
    st.subheader("✍️ Envie uma nova pergunta:")
    pergunta = st.text_input("Digite sua pergunta aqui:", key="pergunta_input")

    if st.button("🚀 Enviar Pergunta"):
        if pergunta.strip():
            # Inserir pergunta no banco
            conn = conectar_mysql()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO perguntas (texto, processado, id_origem) VALUES (%s, 0, 1)",
                (pergunta,)
            )
            conn.commit()
            id_pergunta = cursor.lastrowid
            conn.close()

            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                script_path = os.path.abspath(os.path.join(base_dir, "..", "processachatbot.py"))

                with st.spinner("🤖 Processando pergunta..."):
                    subprocess.run(
                        ["python3", script_path, str(id_pergunta)],
                        capture_output=True, text=True, check=True
                    )

                # Polling para buscar resposta
                resposta = None
                for _ in range(10):
                    dados = carregar_dados(
                        "SELECT texto FROM respostas WHERE id_pergunta = %s ORDER BY data DESC LIMIT 1",
                        (id_pergunta,)
                    )
                    if dados:
                        resposta = dados[0]['texto']
                        break
                    time.sleep(1)

                if resposta:
                    # Adiciona histórico
                    st.session_state.historico.append({
                        "pergunta": pergunta,
                        "resposta": resposta
                    })
                    # Limpa o campo apenas reiniciando a página
                    st.rerun()

                else:
                    st.warning("⚠️ Nenhuma resposta encontrada.")

            except subprocess.CalledProcessError as e:
                st.error(f"❌ Erro ao executar script:\n{e.stderr or e.stdout}")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")
        else:
            st.warning("⚠️ Digite uma pergunta antes de enviar.")
