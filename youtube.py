import yt_dlp
import mysql.connector
import speech_recognition as sr
from pydub import AudioSegment, silence
import os
import re
import tempfile
from db_config import DB_CONFIG

modo_filtro = 2     # 1 = pydub, 2 = noisereduce
modo_captura = 3    # 1 = áudio filtrado, 2 = com ruído, 3 = legenda do YouTube


# 💾 Conexão com o banco
conn = mysql.connector.connect(**DB_CONFIG, ssl_disabled=True)
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
