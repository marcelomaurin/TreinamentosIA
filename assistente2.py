TipoSaida = 1  # 1 = GTTS, 2 = eSpeak

import pyttsx3
import subprocess
import tempfile
from gtts import gTTS 
import openai
import speech_recognition as sr
import os
from collections import deque
from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

# Inicialização condicional para pyttsx3 se TipoSaida 2 ou 3 for usado
espeak_engine = None
if TipoSaida in [2, 3]:
    espeak_engine = pyttsx3.init()
    if TipoSaida == 2:
        espeak_engine.setProperty('voice', 'brazil')
    elif TipoSaida == 3:
        espeak_engine.setProperty('voice', 'mb-pt4')
    espeak_engine.setProperty('rate', 150)
    espeak_engine.setProperty('volume', 1.0)

# 💖 Sua chave da OpenAI (nova versão)
client = openai.OpenAI(api_key='chave')

# Palavra que ativa o assistente
palavra_ativacao = "computador"

# Histórico completo para resumo
historico_completo = deque(maxlen=50)  # lista de (texto, datetime)

# Buffer de contexto atual resumido
buffer_resumido = deque(maxlen=10)  # apenas o resumo ativo

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

def verificar_se_e_continuacao(nova_pergunta):
    if not buffer_resumido:
        return False
    pergunta_anterior, _ = buffer_resumido[-1]
    prompt = (
        "Você é um classificador. Responda apenas com 'Sim' ou 'Não'.\n"
        "Pergunta anterior:\n"
        f"{pergunta_anterior}\n\n"
        "Nova pergunta:\n"
        f"{nova_pergunta}\n\n"
        "A nova pergunta é continuação direta da anterior?"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um classificador. Responda apenas com 'Sim' ou 'Não'."},
                {"role": "user", "content": prompt}
            ]
        )
        resultado = response.choices[0].message.content.strip().lower()
        print(f"🤖 Classificador: {resultado}")
        return resultado.startswith("sim")
    except Exception as e:
        print("⚠️ Erro na verificação de continuação:", e)
        return False

def resumir_interacao(pergunta, resposta):
    mensagens = [{"role": "system", "content": "Resuma a pergunta e a resposta em uma única frase mantendo o contexto essencial. Seja claro, direto e mantenha as informações importantes."}]
    mensagens.append({"role": "user", "content": f"Pergunta: {pergunta}\nResposta: {resposta}"})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )
        resumo = response.choices[0].message.content.strip()
        print("🧠 Resumo da interação:", resumo)
        buffer_resumido.clear()
        buffer_resumido.append((resumo, datetime.now()))
    except Exception as e:
        print("⚠️ Erro ao gerar o resumo da interação:", e)


def perguntar_chatgpt(pergunta):
    mensagens = [{
        "role": "system",
        "content": (
            "Você é um assistente virtual inteligente, inspirado na assistente Sexta-feira (F.R.I.D.A.Y.) do Homem de Ferro.\n"
            "Suas respostas serão lidas por um sintetizador de voz (Google Speech), então escreva com clareza, ritmo e naturalidade.\n"
            "Use frases curtas e objetivas. Separe ideias com vírgulas, pontos e reticências para marcar pausas naturais.\n"
            "Evite interjeições como 'Ah!', 'Hmm', etc., pois elas não são bem interpretadas.\n"
            "Evite frases longas. Prefira linguagem direta, sem floreios.\n"
            "A entonação deve surgir da pontuação: vírgulas para pausas curtas, pontos para encerramento, reticências para continuidade."
        )
    }]

    for entrada, _ in buffer_resumido:
        mensagens.append({"role": "user", "content": entrada})

    mensagens.append({"role": "user", "content": pergunta})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )
        resposta = response.choices[0].message.content.strip()
        print("🤖 ChatGPT:", resposta)
        return resposta
    except Exception as e:
        print("⚠️ Erro na API:", e)
        return "Desculpe, houve um erro ao consultar o sistema."

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
    else:
        print("⚠️ Tipo de saída de voz não suportado.")

def assistente_loop():
    threading.Thread(target=iniciar_janela_historico, daemon=True).start()
    while True:
        texto = ouvir_microfone()
        if texto is None:
            continue

        agora = datetime.now()
        nova_pergunta = texto.strip()
        historico_completo.append((nova_pergunta, agora))

        tempo_expirado = True
        if buffer_resumido:
            _, ultima_data = buffer_resumido[-1]
            segundos = (agora - ultima_data).total_seconds()
            tempo_expirado = segundos > 120

        precisa_ativacao = not buffer_resumido or tempo_expirado

        if precisa_ativacao:
            if palavra_ativacao in nova_pergunta:
                historico_completo.clear()
                buffer_resumido.clear()
                nova_pergunta = nova_pergunta.replace(palavra_ativacao, '').strip()
                historico_completo.append((nova_pergunta, agora))
            else:
                print("⛔ Pergunta ignorada: é um novo assunto e a palavra de ativação não foi usada.")
                continue
        else:
            nova_pergunta = nova_pergunta.replace(palavra_ativacao, '').strip()
            if verificar_se_e_continuacao(nova_pergunta):
                historico_completo.append((nova_pergunta, agora))
            else:
                if palavra_ativacao in texto:
                    historico_completo.clear()
                    buffer_resumido.clear()
                    nova_pergunta = nova_pergunta.replace(palavra_ativacao, '').strip()
                    historico_completo.append((nova_pergunta, agora))
                else:
                    print("⛔ Pergunta ignorada: não é continuação e a palavra de ativação não foi usada.")
                    continue

        resposta = perguntar_chatgpt(nova_pergunta)
        falar_resposta(resposta)

        historico_completo.append((resposta, datetime.now()))
        resumir_interacao(nova_pergunta, resposta)

        print("\n📜 Histórico atualizado:")
        for i, (p, d) in enumerate(historico_completo, 1):
            print(f"{i:02d}. {p} ({d.strftime('%H:%M:%S')})")
        print("")

        atualizar_historico()

if __name__ == "__main__":
    assistente_loop()
