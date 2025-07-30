# Programa processa_pdf.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import sys
import mysql.connector
from PyPDF2 import PdfReader
import os

# ?? Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "user": "usuario",
    "password": "senha",
    "database": "IAdb",
}

def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)

# ?? Extrai texto do PDF
def extrair_texto_pdf(caminho_pdf):
    texto = ""
    try:
        reader = PdfReader(caminho_pdf)
        for pagina in reader.pages:
            texto += pagina.extract_text() or ""  # Adiciona texto da página
    except Exception as e:
        print(f"? Erro ao ler PDF: {e}")
    return texto.strip()

# ?? Insere documento no banco
def inserir_documento(conn, texto, caminho, id_origem=2):  # Origem padrão: treinamento
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documentos (texto, caminho, id_origem) VALUES (%s, %s, %s)",
        (texto, caminho, id_origem),
    )
    conn.commit()
    print(f"? Documento inserido no banco: {caminho}")

def main():
    if len(sys.argv) < 2:
        print("?? Uso: python3 processa_pdf.py <caminho_arquivo.pdf>")
        sys.exit(1)

    caminho_pdf = sys.argv[1]

    if not os.path.exists(caminho_pdf):
        print(f"? Arquivo não encontrado: {caminho_pdf}")
        sys.exit(1)

    print(f"?? Lendo PDF: {caminho_pdf}")
    texto = extrair_texto_pdf(caminho_pdf)

    if not texto:
        print("?? Nenhum texto extraído do PDF.")
        sys.exit(0)

    conn = conectar_mysql()
    try:
        inserir_documento(conn, texto, caminho_pdf)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
