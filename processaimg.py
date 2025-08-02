# Programa processaimg.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025

import sys
import mysql.connector
import os
import subprocess
from datetime import datetime
from db_config import DB_CONFIG

def processaimagem(conn, caminho_arquivo, id_imagem):
    """
    Executa todos os scripts ativos cadastrados em 'processa_img' para a imagem informada.
    """
    print(f"[{datetime.now()}] 🔍 Iniciando processamento da imagem ID: {id_imagem}")
    print(f"📂 Caminho do arquivo: {caminho_arquivo}")

    cursor = conn.cursor()
    cursor.execute("SELECT id, script FROM processa_img WHERE status = 1")
    scripts = cursor.fetchall()

    if not scripts:
        print("⚠️ Nenhum script ativo encontrado para processamento.")
    else:
        print(f"📜 {len(scripts)} script(s) ativo(s) encontrado(s).")
        for id_script, caminho_script in scripts:
            print(f"🚀 Executando script {id_script}: {caminho_script} para imagem {id_imagem}...")
            try:
                subprocess.run(["python3", caminho_script, str(id_imagem), caminho_arquivo], check=True)
                print(f"✅ Script {id_script} ({caminho_script}) concluído com sucesso.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao executar script {id_script} ({caminho_script}): {e}")
    cursor.close()

def main():
    print(f"[{datetime.now()}] 🚩 Entrou no script processaimg.py")

    # ✅ Validação dos parâmetros de entrada
    print(f"📥 Argumentos recebidos: {sys.argv}")
    if len(sys.argv) != 3:
        print("❌ Uso incorreto. Sintaxe correta:")
        print("   python3 processaimg.py <id_foto> <caminho_imagem>")
        return

    try:
        id_foto = int(sys.argv[1])
        print(f"🔑 ID da Foto recebido: {id_foto}")
    except ValueError:
        print(f"❌ Erro: O parâmetro <id_foto> deve ser um número inteiro. Valor recebido: {sys.argv[1]}")
        return

    caminho = sys.argv[2]
    print(f"🖼️ Caminho da imagem recebido: {caminho}")

    if not os.path.exists(caminho):
        print(f"❌ Erro: Arquivo de imagem não encontrado no caminho informado: {caminho}")
        return

    # 🔗 Conexão com o banco e processamento
    try:
        print(f"[{datetime.now()}] 🔗 Conectando ao banco de dados...")
        conn = mysql.connector.connect(**DB_CONFIG, ssl_disabled=True)
        print("✅ Conexão com o banco de dados estabelecida.")

        processaimagem(conn, caminho, id_foto)

        # ✅ Marca a imagem como processada após execução dos scripts
        print(f"📝 Marcando imagem ID {id_foto} como processada no banco...")
        cursor = conn.cursor()
        cursor.execute("UPDATE foto SET processado = 1 WHERE id = %s", (id_foto,))
        conn.commit()
        cursor.close()
        print(f"✅ Imagem {id_foto} marcada como processada no banco.")

    except mysql.connector.Error as e:
        print(f"⚠️ Erro de banco de dados: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("🔒 Conexão com o banco encerrada.")

    print(f"[{datetime.now()}] 🏁 Processamento finalizado.")

if __name__ == "__main__":
    main()
