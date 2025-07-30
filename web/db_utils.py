import mysql.connector
import streamlit as st
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "usuario"),
    "password": os.getenv("DB_PASSWORD", "senha"),
    "database": os.getenv("DB_NAME", "IAdb"),
}

def conectar_mysql():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        st.error(f"? Erro ao conectar no banco: {err}")
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
