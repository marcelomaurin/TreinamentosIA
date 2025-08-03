#!/usr/bin/env python3
"""
Script para processar transcrição de áudio em fragmentos de 1 minuto,
filtrando apenas voz e submetendo cada parte à API Google Speech-to-Text.
Ao final, monta o texto completo e armazena na tabela transcricao do MySQL.
"""
import io
import os
import argparse
from datetime import datetime

from pydub import AudioSegment
from pydub.silence import detect_silence
from google.cloud import speech
import mysql.connector

from db_config import DB_CONFIG


def transcrever_audio(audio_path, chunk_length_ms=60 * 1000):
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    client = speech.SpeechClient()
    textos = []
    start = 0
    # fragmentar em blocos de até 1 minuto, ajustando para intervalos de silêncio
    while start < duration_ms:
        end = min(start + chunk_length_ms, duration_ms)
        window_start = max(start, end - 500)
        window_end = min(duration_ms, end + 500)
        silences = detect_silence(
            audio[window_start:window_end], min_silence_len=500, silence_thresh=audio.dBFS - 16
        )
        if silences:
            # ajusta fim do bloco para início do silêncio detectado
            end = window_start + silences[0][0]
        chunk = audio[start:end]
        # filtrar banda de voz (300-3000 Hz)
        chunk = chunk.high_pass_filter(300).low_pass_filter(3000)
        buf = io.BytesIO()
        chunk.export(buf, format="wav")
        audio_req = speech.RecognitionAudio(content=buf.getvalue())
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=chunk.frame_rate,
            language_code="pt-BR",
        )
        response = client.recognize(config=config, audio=audio_req)
        for result in response.results:
            textos.append(result.alternatives[0].transcript)
        start = end
    return " ".join(textos).strip()


def inserir_transcricao(id_documento, texto):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transcricao (id_documento, texto) VALUES (%s, %s)",
        (id_documento, texto),
    )
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id


def main():
    parser = argparse.ArgumentParser(
        description="Processa transcrição de áudio e armazena no banco MySQL."
    )
    parser.add_argument(
        "id_documento", type=int, help="ID do documento (perguntas) no banco."
    )
    parser.add_argument("audio_file", help="Caminho para o arquivo de áudio a ser transcrito.")
    args = parser.parse_args()
    texto = transcrever_audio(args.audio_file)
    trans_id = inserir_transcricao(args.id_documento, texto)
    print(f"Transcrição armazenada com id {trans_id} em {datetime.now()}")


if __name__ == "__main__":
    main()
