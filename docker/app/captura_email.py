# Programa captura_email.py
# Criado por Marcelo Maurin Martins
# 30/07/2025

import mysql.connector
import poplib
import email
from email.parser import BytesParser
from email.policy import default
from datetime import datetime
from email.utils import parsedate_to_datetime
from db_config import DB_CONFIG

# ?? Conexão com MySQL
def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)
    

def converter_data_email(data_raw):
    try:
        dt = parsedate_to_datetime(data_raw)
        return dt.strftime("%Y-%m-%d %H:%M:%S")  # Formato aceito pelo MySQL
    except Exception as e:
        print(f"⚠️ Erro ao converter data '{data_raw}': {e}")
        return None    

# ?? Buscar contas de e-mail
def buscar_contas_email():
    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contas_email WHERE ativo = 1")
    contas = cursor.fetchall()
    cursor.close()
    conn.close()
    return contas

# ?? Verificar se o e-mail já está registrado
def email_existe(id_conta, mensagem_id):
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM emails WHERE id_conta = %s AND message_id = %s", (id_conta, mensagem_id))
    existe = cursor.fetchone()[0] > 0
    cursor.close()
    conn.close()
    return existe

# ?? Inserir e-mail no banco
def salvar_email(id_conta, remetente, assunto, corpo, data_envio, destinatarios, cc, cco, prioridade, anexos, tipo, message_id):
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emails (id_conta, remetente, assunto, corpo, data_envio, destinatarios, cc, cco, prioridade, anexos, tipo, message_id, lido) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0)
    """, (id_conta, remetente, assunto, corpo, data_envio, destinatarios, cc, cco, prioridade, anexos, tipo, message_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"? E-mail '{assunto}' salvo com sucesso.")

# ?? Capturar e-mails de uma conta
def capturar_emails_pop3(conta):
    print(f"?? Conectando à conta: {conta['email']}")
    try:
        # Conectar ao servidor POP3
        if conta["ssl_pop3"]:
            pop = poplib.POP3_SSL(conta["servidor_pop3"], conta["porta_pop3"])
        else:
            pop = poplib.POP3(conta["servidor_pop3"], conta["porta_pop3"])
        
        pop.user(conta["usuario"])
        pop.pass_(conta["senha"])
        total_mensagens = len(pop.list()[1])
        print(f"?? {total_mensagens} mensagens encontradas na conta {conta['email']}.")

        # Iterar pelas mensagens
        for i in range(total_mensagens, 0, -1):  # Mais recentes primeiro
            raw_email = b"\n".join(pop.retr(i)[1])
            msg = BytesParser(policy=default).parsebytes(raw_email)

            message_id = msg["Message-ID"]
            remetente = msg["From"]
            assunto = msg["Subject"]
            data_envio = msg["Date"]
            #destinatarios = msg["To"]
            destinatarios = msg["To"] if msg["To"] else "Desconhecido"

            cc = msg["Cc"]
            cco = None  # CCO geralmente não vem visível
            prioridade = msg["X-Priority"] if "X-Priority" in msg else "Normal"
            anexos = any(part.get_content_disposition() == "attachment" for part in msg.walk())
            #tipo = msg.get_content_type()
            tipo = msg.get_content_type().split('/')[0]  # Pega apenas 'multipart', 'text', etc.


            # Obter corpo do e-mail
            corpo = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get_content_disposition() is None:
                        corpo += part.get_payload(decode=True).decode(errors="ignore")
            else:
                corpo = msg.get_payload(decode=True).decode(errors="ignore")

            data_envio = converter_data_email(msg["Date"])
            if not data_envio:
                continue  # Pula e-mails com datas inválidas
                            

            # Verificar duplicação
            if not email_existe(conta["id"], message_id):
                salvar_email(
                    conta["id"], remetente, assunto, corpo, data_envio, destinatarios,
                    cc, cco, prioridade, anexos, tipo, message_id
                )
            else:
                print(f"? E-mail já registrado: {assunto}")

        pop.quit()

    except Exception as e:
        print(f"? Erro ao capturar e-mails da conta {conta['email']}: {e}")

# ?? Execução principal
if __name__ == "__main__":
    print("?? Iniciando captura de e-mails...")
    contas = buscar_contas_email()
    if contas:
        for conta in contas:
            capturar_emails_pop3(conta)
    else:
        print("?? Nenhuma conta de e-mail ativa encontrada.")
    print("?? Captura de e-mails finalizada.")
