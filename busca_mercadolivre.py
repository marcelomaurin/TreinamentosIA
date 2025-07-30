# Programa busca_mercadolivre.py
# Criado por Marcelo Maurin Martins
# Data: 30/07/2025


import mysql.connector
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Conexão com o banco
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="usuario",
    password="senha",
    database="IAdb",
    ssl_disabled=True
)
cursor = conn.cursor(dictionary=True)

# Criar sessão global para requisições HTTP
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def buscar_info_mercadolivre(termo):
    try:
        url = f"https://lista.mercadolivre.com.br/{termo.replace(' ', '-')}"
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Novo seletor: cada item está em ".ui-search-layout__item"
        primeiro_item = soup.select_one(".ui-search-layout__item")
        if not primeiro_item:
            print(f"⚠️ Nenhum item encontrado na página para '{termo}'")
            return None

        # Novo seletor para link
        link_tag = primeiro_item.select_one("a")
        if not link_tag or not link_tag.get("href"):
            print(f"⚠️ Não foi possível encontrar o link do produto.")
            return None
        link = link_tag["href"]

        # Preço atualizado (normalmente dentro de .andes-money-amount__fraction)
        preco_tag = primeiro_item.select_one(".andes-money-amount__fraction")
        preco = preco_tag.text.strip() if preco_tag else "Preço não encontrado"

        # Acessa a página do produto
        resp2 = session.get(link, timeout=10)
        resp2.raise_for_status()
        soup2 = BeautifulSoup(resp2.text, "html.parser")

        descricao = soup2.select_one("h1").text.strip() if soup2.select_one("h1") else ""
        desc_tecnica = ""

        detalhes = soup2.select(".specs-wrapper, .ui-pdp-specs__table")
        for bloco in detalhes:
            desc_tecnica += bloco.get_text(separator=" | ", strip=True)

        return {
            "descricao": descricao,
            "descricao_tecnica": desc_tecnica.strip(),
            "preco": preco,
            "link": link
        }
    except Exception as e:
        print(f"❌ Erro ao buscar '{termo}': {e}")
        return None


# Processar itens pendentes
cursor.execute("SELECT * FROM item_compra WHERE processado = 0")
itens = cursor.fetchall()

for item in itens:
    print(f"🔍 Buscando: {item['item']}")
    resultado = buscar_info_mercadolivre(item['item'])

    if resultado:
        cursor.execute("""
            INSERT INTO item_compra_resultado 
            (id_item_compra, descricao, descricao_tecnica, preco, link, dtcad)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item['id'],
            resultado['descricao'],
            resultado['descricao_tecnica'],
            resultado['preco'],
            resultado['link'],
            datetime.now()
        ))

        cursor.execute("UPDATE item_compra SET processado = 1 WHERE id = %s", (item['id'],))
        conn.commit()
        print(f"✅ Item '{item['item']}' processado com sucesso.")
    else:
        print(f"⚠️ Nenhum resultado encontrado para '{item['item']}'")

time.sleep(1)
cursor.close()
conn.close()

