TipoSaida = 1  # 1 = GTTS, 2 = eSpeak
import mysql.connector
import pyttsx3
import subprocess
import tempfile
from gtts import gTTS
import openai
import speech_recognition as sr
import os
from collections import deque
from datetime import datetime

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

# 💖 Sua chave da OpenAI
client = openai.OpenAI(api_key='sua-chave-aqui')

palavra_ativacao = "computador"
historico_completo = deque(maxlen=50)
buffer_resumido = deque(maxlen=10)

def salvar_analise_sentimento(id_pergunta, sentimento_detectado):
    """
    Recebe o texto do sentimento detectado e o ID da pergunta.
    Busca o ID do sentimento e salva na tabela analise_sentimentos.
    """
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco. Análise não salva.")
        return

    try:
        cursor = conexao_mysql.cursor()

        # Buscar ID do sentimento
        cursor.execute("SELECT id FROM sentimentos WHERE texto = %s", (sentimento_detectado,))
        resultado = cursor.fetchone()

        if not resultado:
            print(f"❌ Sentimento '{sentimento_detectado}' não encontrado no banco.")
            cursor.close()
            return

        id_sentimento = resultado[0]

        # Salvar na tabela de análise
        cursor.execute("""
            INSERT INTO analise_sentimentos (id_pergunta, id_sentimento)
            VALUES (%s, %s)
        """, (id_pergunta, id_sentimento))

        conexao_mysql.commit()
        cursor.close()
        print(f"🧠 Análise de sentimento salva com sucesso: Pergunta {id_pergunta} → Sentimento '{sentimento_detectado}' (ID {id_sentimento})")

    except Exception as e:
        print(f"⚠️ Erro ao salvar análise de sentimento: {e}")


def classificar_sentimento(pergunta):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return None

    try:
        # Buscar lista de sentimentos do banco
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT texto FROM sentimentos")
        sentimentos_lista = [row[0] for row in cursor.fetchall()]
        cursor.close()
    except Exception as e:
        print(f"⚠️ Erro ao buscar sentimentos: {e}")
        return None

    prompt = (
        "Você é um classificador de sentimentos. Abaixo está uma lista de sentimentos possíveis:\n"
        f"{', '.join(sentimentos_lista)}.\n\n"
        f"Dada a frase: \"{pergunta}\"\n"
        "Indique **apenas o nome do sentimento** que mais representa essa frase, sem explicações, sem pontuação."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um classificador de sentimentos."},
                {"role": "user", "content": prompt}
            ]
        )
        sentimento = response.choices[0].message.content.strip().title()
        print(f"💡 Sentimento identificado: {sentimento}")
        return sentimento
    except Exception as e:
        print(f"⚠️ Erro ao classificar sentimento: {e}")
        return None

def buscar_id_sentimento(sentimento):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return None
    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT id FROM sentimentos WHERE texto = %s", (sentimento,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            print(f"🔎 Sentimento '{sentimento}' tem ID {resultado[0]}")
            return resultado[0]
        else:
            print(f"❌ Sentimento '{sentimento}' não encontrado no banco.")
            return None
    except Exception as e:
        print(f"⚠️ Erro ao buscar sentimento: {e}")
        return None
        
def classificar_idioma(texto):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return None

    try:
        # Buscar todos os idiomas da tabela
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT nome FROM idiomas")
        idiomas_lista = [row[0] for row in cursor.fetchall()]
        cursor.close()
    except Exception as e:
        print(f"⚠️ Erro ao buscar idiomas: {e}")
        return None

    prompt = (
        "Você é um classificador de idiomas. Abaixo está a lista de idiomas suportados:\n"
        f"{', '.join(idiomas_lista)}.\n\n"
        f"Dado o texto: \"{texto}\"\n"
        "Indique apenas o **nome do idioma** em que esse texto está escrito, sem explicações e sem pontuação."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um classificador de idiomas."},
                {"role": "user", "content": prompt}
            ]
        )
        idioma_detectado = response.choices[0].message.content.strip().title()
        print(f"🌍 Idioma identificado: {idioma_detectado}")
        return idioma_detectado
    except Exception as e:
        print(f"⚠️ Erro ao classificar idioma: {e}")
        return None

def buscar_id_idioma(nome_idioma):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return None
    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT id FROM idiomas WHERE nome = %s", (nome_idioma,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            print(f"🔎 Idioma '{nome_idioma}' tem ID {resultado[0]}")
            return resultado[0]
        else:
            print(f"❌ Idioma '{nome_idioma}' não encontrado no banco.")
            return None
    except Exception as e:
        print(f"⚠️ Erro ao buscar idioma: {e}")
        return None

        
# Conexão com o MySQL (ajuste o host, user e password conforme necessário)
try:
    conexao_mysql = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='senha',
        database='IAdb'
    )
    print("✅ Conectado ao banco de dados IAdb")
except Exception as e:
    print(f"❌ Erro ao conectar no banco de dados: {e}")
    conexao_mysql = None
    
def gerar_subperguntas(id_pergunta, texto_pergunta):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return

    prompt = (
        "Você é um assistente que ajuda a dividir instruções em partes menores com sentido individual.\n"
        "Abaixo está uma frase, e sua tarefa é separá-la em subfrases ou comandos curtos, cada um com sentido completo.\n"
        "Responda com uma lista simples, cada linha uma subpergunta.\n\n"
        f"Frase: \"{texto_pergunta}\"\n"
        "Subperguntas:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você divide frases em partes menores com sentido independente."},
                {"role": "user", "content": prompt}
            ]
        )

        resposta = response.choices[0].message.content.strip()
        print("📤 Subperguntas recebidas:\n", resposta)

        # Dividir por linhas
        subperguntas = [linha.strip("-•* ").strip() for linha in resposta.split("\n") if linha.strip()]
        
        cursor = conexao_mysql.cursor()
        for sub in subperguntas:
            cursor.execute(
                "INSERT INTO subpergunta (id_pergunta, texto, processado) VALUES (%s, %s, %s)",
                (id_pergunta, sub, 0)
            )
        conexao_mysql.commit()
        cursor.close()

        print(f"✅ {len(subperguntas)} subpergunta(s) salvas com sucesso.")

    except Exception as e:
        print(f"⚠️ Erro ao gerar ou salvar subperguntas: {e}")
    
    
def salvar_pergunta_mysql(pergunta, id_origem=1):  # padrão: voz
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco. Pergunta não salva.")
        return None
    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("INSERT INTO perguntas (texto, id_origem) VALUES (%s, %s)", (pergunta, id_origem))
        conexao_mysql.commit()
        id_inserido = cursor.lastrowid
        cursor.close()
        print(f"💾 Pergunta salva no banco com ID {id_inserido}")
        return id_inserido
    except Exception as e:
        print(f"⚠️ Erro ao salvar no banco: {e}")
        return None



def salvar_resposta_mysql(id_pergunta, resposta):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco. Resposta não salva.")
        return
    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("INSERT INTO respostas (id_pergunta, texto) VALUES (%s, %s)", (id_pergunta, resposta))
        conexao_mysql.commit()
        cursor.close()
        print(f"💾 Resposta salva no banco vinculada à pergunta {id_pergunta}")
    except Exception as e:
        print(f"⚠️ Erro ao salvar resposta: {e}")



def ouvir_microfone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Fale algo (aguardando)...")
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
        
def analisa_subpergunta(subpergunta_texto):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return None

    try:
        # Buscar os tipos de operação do banco
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT texto FROM tipo_operacao")
        tipos_operacao = [row[0] for row in cursor.fetchall()]
        cursor.close()
    except Exception as e:
        print(f"⚠️ Erro ao buscar tipos de operação: {e}")
        return None

    prompt = (
        "Você é um classificador de operação. Abaixo está uma subpergunta de um usuário.\n"
        "Seu objetivo é classificar essa subpergunta com base na lista de operações abaixo:\n\n"
        f"{', '.join(tipos_operacao)}.\n\n"
        f"Subpergunta: \"{subpergunta_texto}\"\n"
        "Responda apenas com o nome exato da operação que mais se aplica. Não inclua explicações ou pontuação."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um classificador de tipo de operação."},
                {"role": "user", "content": prompt}
            ]
        )
        tipo_detectado = response.choices[0].message.content.strip().title()
        print(f"🔎 Tipo de operação identificado: {tipo_detectado}")
    except Exception as e:
        print(f"⚠️ Erro ao classificar tipo de operação: {e}")
        return None

    # Buscar ID correspondente no banco
    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT id FROM tipo_operacao WHERE texto = %s", (tipo_detectado,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return resultado[0]
        else:
            print(f"❌ Tipo de operação '{tipo_detectado}' não encontrado no banco.")
            return None
    except Exception as e:
        print(f"⚠️ Erro ao buscar ID da operação: {e}")
        return None

def classificar_e_relacionar_tipo_operacao(id_pergunta):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return

    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("SELECT id, texto FROM subpergunta WHERE id_pergunta = %s AND processado = 0", (id_pergunta,))
        subperguntas = cursor.fetchall()

        for sub_id, sub_texto in subperguntas:
            id_tipo = analisa_subpergunta(sub_texto)
            if id_tipo:
                print(f"🔗 Subpergunta ID {sub_id} → Tipo de operação ID {id_tipo}")
                cursor.execute("""
                    INSERT INTO subpergunta_operacao (id_subpergunta, id_tipo_operacao)
                    VALUES (%s, %s)
                """, (sub_id, id_tipo))
                cursor.execute("UPDATE subpergunta SET processado = 1 WHERE id = %s", (sub_id,))
            else:
                print(f"❌ Não foi possível classificar subpergunta ID {sub_id}")

        conexao_mysql.commit()
        cursor.close()
    except Exception as e:
        print(f"⚠️ Erro ao classificar e relacionar subperguntas: {e}")

def subpergunta_contem_tipo_pergunta(id_pergunta):
    if conexao_mysql is None:
        print("⚠️ Sem conexão com o banco.")
        return False
    try:
        cursor = conexao_mysql.cursor()
        cursor.execute("""
            SELECT 1
            FROM subpergunta_operacao so
            JOIN tipo_operacao t ON so.id_tipo_operacao = t.id
            JOIN subpergunta sp ON sp.id = so.id_subpergunta
            WHERE sp.id_pergunta = %s AND t.texto = 'Pergunta'
            LIMIT 1
        """, (id_pergunta,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado is not None
    except Exception as e:
        print(f"⚠️ Erro ao verificar tipo Pergunta: {e}")
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
    print("💬 Assistente iniciado! Diga 'computador' para começar um novo assunto.")
    while True:
        texto = ouvir_microfone()
        if texto is None:
            continue

        agora = datetime.now()
        nova_pergunta = texto.strip()
        historico_completo.append((nova_pergunta, agora))
        id_pergunta = salvar_pergunta_mysql(nova_pergunta, id_origem=1)


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
        if subpergunta_contem_tipo_pergunta(id_pergunta):
            falar_resposta(resposta)
        else:
            print("🤐 Resposta não falada: não é do tipo 'Pergunta'."

        if id_pergunta:
            salvar_resposta_mysql(id_pergunta, resposta)

            sentimento_detectado = classificar_sentimento(nova_pergunta)
            if sentimento_detectado:
              salvar_analise_sentimento(id_pergunta, sentimento_detectado)
            idioma_detectado = classificar_idioma(nova_pergunta)
            if idioma_detectado:
              id_idioma = buscar_id_idioma(idioma_detectado)
              
            # Cria subperguntas e classifica tipo de operação
            gerar_subperguntas(id_pergunta, nova_pergunta)
            classificar_e_relacionar_tipo_operacao(id_pergunta)
       




        falar_resposta(resposta)
        historico_completo.append((resposta, datetime.now()))
        resumir_interacao(nova_pergunta, resposta)

        print("\n📜 Histórico atualizado:")
        for i, (p, d) in enumerate(historico_completo, 1):
            print(f"{i:02d}. {p} ({d.strftime('%H:%M:%S')})")
        print("")

if __name__ == "__main__":
    assistente_loop()

