import os
import tempfile
import yt_dlp
import mysql.connector
import speech_recognition as sr
from pydub import AudioSegment
from pydub import silence
import os
import re

modo_filtro = 2     # 1 = pydub, 2 = noisereduce
modo_captura = 3    # 1 = áudio filtrado, 2 = com ruído, 3 = legenda do YouTube




# 💾 Conexão com o banco
conn = mysql.connector.connect(
    host="localhost",
    user="usuario",
    password="senha",
    database="IAdb"
)
cursor = conn.cursor()

#from spleeter.separator import Separator

def captura_caption(video_id):
    import subprocess
    import glob

    url = f"https://www.youtube.com/watch?v={video_id}"
    temp_dir = tempfile.gettempdir()

    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "pt",
        "--skip-download",
        "--output", os.path.join(temp_dir, "%(id)s.%(ext)s"),
        url
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao capturar legenda: {e}")
        return []

    # 🔍 Procura o arquivo de legenda baixado
    pattern = os.path.join(temp_dir, f"{video_id}*.vtt")
    matches = glob.glob(pattern)

    if not matches:
        print("⚠️ Nenhuma legenda em português encontrada.")
        return []

    legenda_path = matches[0]

    frases = []
    try:
        with open(legenda_path, "r", encoding="utf-8") as f:
            for line in f:
                if "-->" in line or line.strip().isdigit() or line.strip() == "":
                    continue
                frases.extend([fr.strip() for fr in line.strip().split(".") if fr.strip()])
    except Exception as e:
        print(f"❌ Erro ao processar legenda: {e}")
        return []

    return frases



def aplica_filtro(audio: AudioSegment) -> AudioSegment:
    if modo_filtro == 1:
        print("🎚️ Aplicando filtro Pydub (300Hz-3000Hz)")
        return audio.high_pass_filter(300).low_pass_filter(3000)

    elif modo_filtro == 2:
        print("🎚️ Aplicando redução de ruído com noisereduce")
        import numpy as np
        import noisereduce as nr

        # Converte para mono se for estéreo
        if audio.channels > 1:
            audio = audio.set_channels(1)

        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        reduced = nr.reduce_noise(y=samples, sr=audio.frame_rate)

        # Normaliza e converte de volta para int16
        reduced_int16 = np.int16(reduced / np.max(np.abs(reduced)) * 32767)

        audio_clean = AudioSegment(
            reduced_int16.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=2,
            channels=1
        )
        return audio_clean

    else:
        print("⚠️ Modo de filtro inválido. Usando original.")
        return audio


def dividir_em_segmentos(audio_path, duracao_max=60 * 1000):  # 60s em ms
    audio = AudioSegment.from_wav(audio_path)
    partes = silence.split_on_silence(
        audio,
        min_silence_len=700,
        silence_thresh=audio.dBFS - 16,
        keep_silence=300
    )

    segmentos = []
    atual = AudioSegment.silent(duration=0)
    for parte in partes:
        if len(atual + parte) <= duracao_max:
            atual += parte
        else:
            if len(atual) > 1000:
                segmentos.append(atual)
            atual = parte
    if len(atual) > 1000:
        segmentos.append(atual)

    arquivos_segmentos = []
    for i, segmento in enumerate(segmentos):
        temp_seg = tempfile.mktemp(suffix=f"_seg{i}.wav")
        segmento.export(temp_seg, format="wav")
        arquivos_segmentos.append(temp_seg)

    return arquivos_segmentos




def salva_frases(frases, origem='treinamento'):
    id_origem = 2 if origem == 'treinamento' else 1  # 2 = treinamento, 1 = voz, caption pode ser 1 também

    if origem == 'caption':
        texto_unico = " ".join(frases).strip()
        if texto_unico:
            cursor.execute(
                "INSERT INTO perguntas (texto, id_origem) VALUES (%s, %s)",
                (texto_unico, id_origem)
            )
    else:
        for frase in frases:
            frase = frase.strip()
            if frase:
                cursor.execute(
                    "INSERT INTO perguntas (texto, id_origem) VALUES (%s, %s)",
                    (frase, id_origem)
                )
    conn.commit()



def limpar_legenda_vtt(caminho_vtt):
    texto_limpo = []
    try:
        with open(caminho_vtt, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()

                # Ignorar metadados e tempos
                if (not linha or
                    linha.startswith("WEBVTT") or
                    "-->" in linha or
                    linha.isdigit()):
                    continue

                # Remove tags <...> e colchetes [exemplo]
                linha = re.sub(r"<[^>]+>", "", linha)
                linha = re.sub(r"\[.*?\]", "", linha)

                if linha and (not texto_limpo or linha != texto_limpo[-1]):
                    texto_limpo.append(linha)
    except Exception as e:
        print(f"❌ Erro ao limpar legenda .vtt: {e}")
        return ""

    return "\n".join(texto_limpo)


def transcreve_google(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        try:
            audio = r.record(source)
            texto = r.recognize_google(audio, language='pt-BR')
            print("📝 Texto transcrito com sucesso!")
            frases = [fr.strip() for fr in texto.split(".") if fr.strip()]
            return frases
        except sr.UnknownValueError:
            print("⚠️ Google não conseguiu entender o áudio.")
        except sr.RequestError as e:
            print(f"❌ Erro na requisição: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado na transcrição: {e}")
    return []


def processa_video(url):
    print(f"🎥 Processando: {url}")
    video_id = url.split("v=")[-1]
    temp_dir = tempfile.gettempdir()

    # 💬 Opção 3: Captura apenas legenda
    if modo_captura == 3:
        # Captura a legenda bruta (baixa o .vtt)
        frases = captura_caption(video_id)

        # Caminho para o arquivo baixado
        caminho_vtt = os.path.join(temp_dir, f"{video_id}.pt.vtt")

        if os.path.exists(caminho_vtt):
            texto_limpo = limpar_legenda_vtt(caminho_vtt)

            # 💾 Salvar transcrição limpa no banco (como um único registro)
            if texto_limpo.strip():
                salva_frases([texto_limpo], origem='caption')
                print(f"✅ Transcrição limpa salva no banco.")

            # 💾 Salvar como arquivo .txt
            caminho_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_txt = os.path.join(caminho_atual, f"{video_id}.txt")

            with open(caminho_txt, "w", encoding="utf-8") as f:
                f.write(texto_limpo)

            print(f"📄 Transcrição limpa salva em: {caminho_txt}")
            os.remove(caminho_vtt)  # opcional
        else:
            print("⚠️ Nenhuma legenda .vtt encontrada.")
        return

    # 🎧 Opções 1 e 2: Processamento de áudio
    saida_mp3 = os.path.join(temp_dir, f"{video_id}.mp3")
    saida_wav = os.path.join(temp_dir, f"{video_id}.wav")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': saida_mp3.replace('.mp3', '.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"❌ Erro ao baixar o vídeo: {e}")
        return

    if not os.path.exists(saida_mp3):
        print(f"⚠️ Arquivo não encontrado: {saida_mp3}")
        return

    try:
        audio = AudioSegment.from_mp3(saida_mp3)
        audio_filtrado = aplica_filtro(audio)
        audio_filtrado.export(saida_wav, format="wav")
        os.remove(saida_mp3)
    except Exception as e:
        print(f"❌ Erro ao converter para WAV: {e}")
        return

    segmentos = dividir_em_segmentos(saida_wav)
    os.remove(saida_wav)

    frases = []
    for seg_path in segmentos:
        trecho = transcreve_google(seg_path)
        if trecho:
            frases.extend(trecho)
        os.remove(seg_path)

    if frases:
        salva_frases(frases, origem='treinamento')
        print(f"✅ {len(frases)} frases salvas após segmentação.")


def buscar_e_processar(termobusca="saúde pública", qtd_videos=3):
    search_term = f"ytsearch{qtd_videos}:{termobusca}"
    print(f"🔍 Buscando vídeos com o termo: {termobusca}")

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(search_term, download=False)
        entries = info_dict.get("entries", [])
        for entry in entries:
            url = f"https://www.youtube.com/watch?v={entry['id']}"
            print(f"🎥 Encontrado: {entry['title']}")
            processa_video(url)

def main():
    buscar_e_processar(termobusca="saúde pública", qtd_videos=3)

if __name__ == "__main__":
    main()

