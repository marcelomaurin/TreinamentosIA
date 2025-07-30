# Programa captura.py
# Criado por Marcelo Maurin Martins
# 30/07/2025

import cv2
import numpy as np
import mysql.connector
import subprocess
import glob
import os
from datetime import datetime

# 🎯 Resolução
RES_WIDTH = 640
RES_HEIGHT = 480

# 🔧 Flags de controle
flg_kinect = False    # True = ativa Kinect, False = desativa
flg_cameras = True    # True = ativa câmeras web, False = desativa

# 📥 Importa freenect somente se necessário
if flg_kinect:
    import freenect

# 💾 Conexão com MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="usuario",
        password="senha",
        database="IAdb"
    )

def processa_scripts(id_foto, caminho_arquivo):
    print(f"🔧 Executando scripts de processamento para ID {id_foto} com arquivo {caminho_arquivo}...")

    try:
        subprocess.run(["python3", "processaimg.py", str(id_foto), caminho_arquivo], check=True)
        conn = conectar_mysql()
        cursor = conn.cursor()
        cursor.execute("UPDATE foto SET processado = 1 WHERE id = %s", (id_foto,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Processamento concluído e imagem {id_foto} marcada como processada.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao processar imagem {id_foto}: {e}")


def salvar_no_banco(frame, data, hora, device, processado=0):
    conn = conectar_mysql()
    cursor = conn.cursor()
    sql = "INSERT INTO foto (frame, data, hora, device, processado) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (frame, data, hora, device, processado))
    conn.commit()
    id_foto = cursor.lastrowid  # Retorna ID inserido
    cursor.close()
    conn.close()
    print(f"✅ Foto do dispositivo '{device}' registrada com sucesso.")
    return id_foto

# 📸 Pega imagem do Kinect
def capturar_kinect():
    if not flg_kinect:
        print("🚫 Kinect desativado pelo flag.")
        return False
    try:
        frame = freenect.sync_get_video()[0]
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (RES_WIDTH, RES_HEIGHT))
            
            _, buffer = cv2.imencode('.jpg', frame)
            
            caminho_temp = os.path.join(os.path.dirname(__file__), "temp_kinect.jpg")
            cv2.imwrite(caminho_temp, frame)
            print(f"💾 Imagem salva em: {caminho_temp}")

            id_foto = salvar_no_banco(buffer.tobytes(), datetime.today().date(), datetime.now().time(), "Kinect v1")

            processa_scripts(id_foto, caminho_temp)
            return True
    except Exception as e:
        print(f"⚠️ Erro ao capturar do Kinect: {e}")
    return False


def capturar_cameras_usb():
    if not flg_cameras:
        print("🚫 Câmeras web desativadas pelo flag.")
        return False

    dispositivos = sorted(glob.glob("/dev/video*"))
    if not dispositivos:
        print("⚠️ Nenhuma câmera USB encontrada.")
        return False

    print(f"🔍 Câmeras detectadas: {', '.join(dispositivos)}")

    capturou = False
    for device in dispositivos:
        index = int(device.replace("/dev/video", ""))
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, RES_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RES_HEIGHT)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (RES_WIDTH, RES_HEIGHT))
                _, buffer = cv2.imencode('.jpg', frame)

                # Salva localmente
                caminho_temp = os.path.join(os.path.dirname(__file__), f"temp_usb_{index}.jpg")
                cv2.imwrite(caminho_temp, frame)
                print(f"💾 Imagem da câmera USB {index} salva em: {caminho_temp}")

                # Salva no banco e pega o id_foto
                id_foto = salvar_no_banco(buffer.tobytes(), datetime.today().date(), datetime.now().time(), f"Camera USB {index}")

                # Chama processamento passando ID e caminho do arquivo
                processa_scripts(id_foto, caminho_temp)

                capturou = True
            cap.release()
        else:
            print(f"⚠️ Não foi possível abrir a câmera: {device}")
    return capturou


# 🚀 Execução principal
if __name__ == "__main__":
    print("📷 Iniciando captura...")

    capturou_usb = capturar_cameras_usb()
    capturou_kinect = capturar_kinect()

    print("🏁 Captura finalizada.")
