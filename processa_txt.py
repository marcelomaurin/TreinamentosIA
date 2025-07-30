# Programa processa_txt.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import sys
import mysql.connector
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

# ?? Lê texto do arquivo TXT
def extrair_texto_txt(caminho_txt):
    texto = ""
    try:
        with open(caminho_txt, "r", encoding="utf-8") as f:
            texto = f.read()
    except UnicodeDecodeError:
        # Caso não seja UTF-8, tenta ISO-8859-1 (comum em textos antigos)
        with open(caminho_txt, "r", encoding="latin-1") as f:
            texto = f.read()
    except Exception as e:
        print(f"? Erro ao ler TXT: {e}")
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
        print("?? Uso: python3 processa_txt.py <caminho_arquivo.txt>")
        sys.exit(1)

    caminho_txt = sys.argv[1]

    if not os.path.exists(caminho_txt):
        print(f"? Arquivo não encontrado: {caminho_txt}")
        sys.exit(1)

    print(f"?? Lendo TXT: {caminho_txt}")
    texto = extrair_texto_txt(caminho_txt)

    if not texto:
        print("?? Nenhum texto extraído do TXT.")
        sys.exit(0)

    conn = conectar_mysql()
    try:
        inserir_documento(conn, texto, caminho_txt)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
