# Programa captura_face.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import sys
import os
import cv2
import mysql.connector
from datetime import datetime
from db_config import DB_CONFIG

def conectar_banco():
    return mysql.connector.connect(**DB_CONFIG)

def redimensionar_face(face_img):
    return cv2.resize(face_img, (320, 320), interpolation=cv2.INTER_AREA)

def inserir_informacao(cursor, id_foto, id_face, id_propriedade, campo, valor):
    """
    Insere dados complementares da face na tabela face_informacao.
    """
    print(f"[{datetime.now()}] 📝 Inserindo informação: {campo} = {valor}")
    cursor.execute("""
        INSERT INTO face_informacao (id_foto, id_face, id_propriedade, campo, propriedade, valor)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_foto, id_face, id_propriedade, campo, campo, valor))

def detectar_e_salvar_face(id_foto, caminho_imagem):
    print(f"[{datetime.now()}] 🚩 Iniciando detecção de faces para ID: {id_foto}")
    print(f"[{datetime.now()}] 📂 Caminho da imagem: {caminho_imagem}")

    if not os.path.exists(caminho_imagem):
        print(f"❌ Arquivo não encontrado: {caminho_imagem}")
        return

    # Usa um Haarcascade mais robusto
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    img = cv2.imread(caminho_imagem)
    if img is None:
        print("❌ Imagem inválida ou corrompida.")
        return

    print(f"[{datetime.now()}] 🔄 Convertendo imagem para escala de cinza...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # Melhora contraste

    print(f"[{datetime.now()}] 🔍 Executando detectMultiScale...")
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.08,     # Levemente reduzido (mais sensível)
        minNeighbors=3,       # Menos restritivo
        minSize=(50, 50)      # Face mínima detectável
    )

    if len(faces) == 0:
        print("😞 Nenhuma face detectada. Sugestões: verifique iluminação, ângulo ou use outro classificador.")
        return

    print(f"🔍 {len(faces)} face(s) detectada(s).")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        for i, (x, y, w, h) in enumerate(faces, start=1):
            x1, y1 = x + w, y + h
            print(f"[{datetime.now()}] ✂️ Recortando face {i}: Coordenadas ({x}, {y}), ({x1}, {y1})")

            # Recorta e redimensiona
            face_img = img[y:y+h, x:x+w]
            face_resized = redimensionar_face(face_img)
            _, buffer = cv2.imencode(".jpg", face_resized)
            face_bytes = buffer.tobytes()

            # Salva no banco
            cursor.execute(""" 
                INSERT INTO face (id_foto, face, processado)
                VALUES (%s, %s, 0)
            """, (id_foto, face_bytes))
            id_face = cursor.lastrowid
            print(f"✅ Face {i} salva no banco (ID: {id_face}).")

            # Salva informações adicionais
            inserir_informacao(cursor, id_foto, id_face, 1, "posicao_x", str(x))
            inserir_informacao(cursor, id_foto, id_face, 2, "posicao_y", str(y))
            inserir_informacao(cursor, id_foto, id_face, 3, "posicao_x1", str(x1))
            inserir_informacao(cursor, id_foto, id_face, 4, "posicao_y1", str(y1))

        conn.commit()
        print(f"[{datetime.now()}] 💾 Faces e informações salvas no banco com sucesso.")

    except mysql.connector.Error as e:
        print(f"⚠️ Erro no banco de dados: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print(f"[{datetime.now()}] 🔒 Conexão com o banco encerrada.")


def main():
    print(f"[{datetime.now()}] 🚩 Entrou no script captura_face.py")
    print(f"[{datetime.now()}] 📥 Argumentos recebidos: {sys.argv}")

    if len(sys.argv) != 3:
        print("Uso: python3 captura_face.py <id_foto> <caminho_imagem>")
        return

    try:
        id_foto = int(sys.argv[1])
        print(f"[{datetime.now()}] 🔑 ID da foto: {id_foto}")
    except ValueError:
        print(f"❌ O parâmetro <id_foto> deve ser um número inteiro. Valor recebido: {sys.argv[1]}")
        return

    caminho_imagem = sys.argv[2]
    print(f"[{datetime.now()}] 🖼️ Caminho da imagem: {caminho_imagem}")

    detectar_e_salvar_face(id_foto, caminho_imagem)

if __name__ == "__main__":
    main()
