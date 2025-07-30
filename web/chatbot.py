import streamlit as st
import subprocess
from db_utils import conectar_mysql, carregar_dados

def pagina_chatbot():
    st.header("?? Chatbot Inteligente")
    pergunta = st.text_area("?? Sua pergunta:")

    if st.button("Enviar Pergunta"):
        if pergunta.strip():
            conn = conectar_mysql()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO perguntas (texto, processado, id_origem) VALUES (%s, 0, 1)", (pergunta,))
            conn.commit()
            id_pergunta = cursor.lastrowid
            conn.close()

            st.info(f"?? Pergunta registrada com ID: {id_pergunta}")

            try:
                subprocess.run(["python3", "processachatbot.py", str(id_pergunta)], check=True)
                st.success("? Pergunta processada com sucesso!")
            except Exception as e:
                st.error(f"? Erro: {e}")

            resposta = carregar_dados("SELECT texto FROM respostas WHERE id_pergunta = %s ORDER BY data DESC LIMIT 1", (id_pergunta,))
            if resposta:
                st.subheader("?? Resposta da IA:")
                st.success(resposta[0]['texto'])
            else:
                st.warning("?? Nenhuma resposta encontrada.")
