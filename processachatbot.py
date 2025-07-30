# Programa processachatbot.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import mysql.connector
import openai
import sys
from datetime import datetime

# 🔑 Configuração da API OpenAI
client = openai.OpenAI(api_key="SUA_CHAVE_OPENAI")

# 🔧 Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "user": "usuario",
    "password": "senha",
    "database": "IAdb",
}

# 🎯 Função para conectar ao MySQL
def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)

# 🔍 Buscar pergunta específica pelo ID
def buscar_pergunta_por_id(conn, id_pergunta):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, texto FROM perguntas WHERE id = %s AND processado = 0", (id_pergunta,))
    return cursor.fetchone()

# 🤖 Perguntar para o ChatGPT
def gerar_resposta(pergunta):
    try:
        mensagens = [
            {
                "role": "system",
                "content": (
                    "Você é um assistente virtual inteligente. Responda de forma clara, objetiva e com linguagem natural. "
                    "Evite frases muito longas e explique de forma simples."
                )
            },
            {"role": "user", "content": pergunta}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )
        resposta = response.choices[0].message.content.strip()
        return resposta
    except Exception as e:
        print(f"⚠️ Erro ao gerar resposta: {e}")
        return "Desculpe, ocorreu um erro ao processar sua pergunta."

# 💾 Inserir resposta no banco
def salvar_resposta(conn, id_pergunta, resposta):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO respostas (id_pergunta, texto) VALUES (%s, %s)",
        (id_pergunta, resposta)
    )
    conn.commit()

# ✅ Marcar pergunta como processada
def marcar_pergunta_processada(conn, id_pergunta):
    cursor = conn.cursor()
    cursor.execute("UPDATE perguntas SET processado = 1 WHERE id = %s", (id_pergunta,))
    conn.commit()

# 🔁 Processamento principal
def processar_chatbot(id_pergunta):
    conn = conectar_mysql()
    print(f"🤖 Processando pergunta ID {id_pergunta}...")

    pergunta = buscar_pergunta_por_id(conn, id_pergunta)
    if not pergunta:
        print(f"⚠️ Pergunta ID {id_pergunta} não encontrada ou já processada.")
        return

    print(f"📥 Pergunta ({pergunta['id']}): {pergunta['texto']}")

    resposta = gerar_resposta(pergunta['texto'])
    print(f"💬 Resposta: {resposta}")

    salvar_resposta(conn, pergunta['id'], resposta)
    marcar_pergunta_processada(conn, pergunta['id'])

    print(f"✅ Pergunta {pergunta['id']} processada e resposta salva.")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python3 processachatbot.py <id_pergunta>")
        sys.exit(1)

    id_pergunta = int(sys.argv[1])
    processar_chatbot(id_pergunta)
