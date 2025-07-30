# Programa assistente2.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import pyttsx3
import subprocess
import tempfile
from gtts import gTTS 
import os
from collections import deque
from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import speech_recognition as sr
import mysql.connector

# Configurações
TipoSaida = 1  # 1 = GTTS, 2 = eSpeak
palavra_ativacao = "computador"

# Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "user": "usuario",
    "password": "senha",
    "database": "IAdb",
}

# Inicialização condicional para pyttsx3
espeak_engine = None
if TipoSaida in [2, 3]:
    espeak_engine = pyttsx3.init()
    if TipoSaida == 2:
        espeak_engine.setProperty('voice', 'brazil')
    elif TipoSaida == 3:
        espeak_engine.setProperty('voice', 'mb-pt4')
    espeak_engine.setProperty('rate', 150)
    espeak_engine.setProperty('volume', 1.0)

# Histórico
historico_completo = deque(maxlen=50)
buffer_resumido = deque(maxlen=10)

def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)

def iniciar_janela_historico():
    global historico_janela, texto_historico
    historico_janela = tk.Tk()
    historico_janela.title("Histórico do Buffer")
    texto_historico = ScrolledText(historico_janela, width=50, height=20, font=("Arial", 12))
    texto_historico.pack()
    atualizar_historico()
    historico_janela.mainloop()

def atualizar_historico():
    global texto_historico
    if texto_historico:
        texto_historico.config(state=tk.NORMAL)
        texto_historico.delete("1.0", tk.END)
        historico_formatado = "\n".join([f"{i+1:02d}. {p} ({d.strftime('%H:%M:%S')})" for i, (p, d) in enumerate(historico_completo)])
        texto_historico.insert(tk.END, historico_formatado)
        texto_historico.config(state=tk.DISABLED)

def ouvir_microfone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Aguardando sua fala com carinho...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        print(f"📝 Você disse: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        print("❌ Não entendi o que você disse.")
        return None
    except sr.RequestError as e:
        print("⚠️ Erro ao acessar o serviço de reconhecimento:", e)
        return None

def chamar_processachatbot(id_pergunta):
    print(f"🚀 Chamando processachatbot.py para a pergunta ID {id_pergunta}...")
    subprocess.run(["python3", "processachatbot.py", str(id_pergunta)], check=True)

def buscar_ultima_resposta(conn, id_pergunta):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT texto 
        FROM respostas 
        WHERE id_pergunta = %s 
        ORDER BY data DESC LIMIT 1
    """, (id_pergunta,))
    resultado = cursor.fetchone()
    return resultado['texto'] if resultado else None

def falar_resposta(resposta):
    print("🗣️ Falando com carinho...")
    if TipoSaida == 1:
        tts = gTTS(text=resposta, lang='pt-br')
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts.save(fp.name)
            os.system(f"mpg123 -a default -q {fp.name}")
    elif TipoSaida in [2, 3]:
        espeak_engine.say(resposta)
        espeak_engine.runAndWait()

def assistente_loop():
    threading.Thread(target=iniciar_janela_historico, daemon=True).start()
    conn = conectar_mysql()

    while True:
        texto = ouvir_microfone()
        if texto is None:
            continue

        agora = datetime.now()
        nova_pergunta = texto.strip()

        if palavra_ativacao in nova_pergunta:
            historico_completo.clear()
            buffer_resumido.clear()
            nova_pergunta = nova_pergunta.replace(palavra_ativacao, '').strip()
            historico_completo.append((nova_pergunta, agora))

            # Insere a pergunta na tabela e pega o ID
            cursor = conn.cursor()
            cursor.execute("INSERT INTO perguntas (texto, id_origem) VALUES (%s, %s)", (nova_pergunta, 1))
            conn.commit()
            id_pergunta = cursor.lastrowid

            print(f"📌 Pergunta inserida com ID {id_pergunta}")

            # Chama o processachatbot.py com o ID da pergunta
            chamar_processachatbot(id_pergunta)

            # Busca a resposta para essa pergunta
            resposta = buscar_ultima_resposta(conn, id_pergunta)
            if resposta:
                falar_resposta(resposta)
                historico_completo.append((resposta, datetime.now()))
                atualizar_historico()
            else:
                print("⚠️ Nenhuma resposta encontrada após o processamento.")
        else:
            print("⛔ Palavra de ativação não detectada. Ignorando...")

if __name__ == "__main__":
    assistente_loop()
