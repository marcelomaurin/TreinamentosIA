import mysql.connector
import streamlit as st
import os
import sys

# Garante que o diretório principal esteja no sys.path para importar db_config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import DB_CONFIG

def conectar_mysql():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        st.error(f"❌ Erro ao conectar no banco: {err}")
        st.stop()

def carregar_dados(query, params=None):
    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def inserir_dados(query, valores):
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

def excluir_dados(tabela, id_registro):
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE id = %s", (id_registro,))
    conn.commit()
    conn.close()
