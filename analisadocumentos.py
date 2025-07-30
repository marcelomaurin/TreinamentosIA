# Programa analisadocumentos.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import os
import mysql.connector
from datetime import datetime
import subprocess

# ?? Diretório base dos documentos
DOCS_DIR = "/home/mmm/projetos/maurinsoft/assistente2/docs"

# ?? Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "user": "usuarios",
    "password": "senha",
    "database": "IAdb",
}

# Extensões válidas e scripts correspondentes
EXT_SCRIPTS = {
    ".pdf": "processa_pdf.py",
    ".txt": "processa_txt.py",
    ".docx": "processa_docx.py",
    ".csv": "processa_csv.py"
}

# ?? Conectar ao MySQL
def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)

# ?? Verifica se o documento já existe na tabela
def documento_existe(conn, caminho):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documentos WHERE caminho = %s", (caminho,))
    (count,) = cursor.fetchone()
    return count > 0

# ?? Insere documento na tabela
def inserir_documento(conn, texto, caminho, id_origem=2):  # origem padrão: treinamento
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documentos (texto, caminho, id_origem) VALUES (%s, %s, %s)",
        (texto, caminho, id_origem),
    )
    conn.commit()
    print(f"?? Documento registrado: {caminho}")

# ?? Processa documentos
def processar_documentos():
    conn = conectar_mysql()
    try:
        for root, dirs, files in os.walk(DOCS_DIR):
            for file in files:
                caminho_completo = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                print(f"?? Verificando: {caminho_completo}")

                # Verifica se já está no banco
                if documento_existe(conn, caminho_completo):
                    print(f"? Já registrado: {caminho_completo}")
                    continue

                # Verifica extensão e script correspondente
                if ext in EXT_SCRIPTS:
                    script = EXT_SCRIPTS[ext]
                    print(f"?? Chamando script {script} para {file}")
                    subprocess.run(["python3", script, caminho_completo], check=True)

                else:
                    print(f"?? Extensão não suportada: {ext}")
    finally:
        conn.close()

if __name__ == "__main__":
    processar_documentos()
