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

# Função para extrair os dados do primeiro resultado
def buscar_info_mercadolivre(termo):
    url = f"https://lista.mercadolivre.com.br/{termo.replace(' ', '-')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    primeiro_item = soup.select_one(".ui-search-result__wrapper")
    if not primeiro_item:
        return None

    link = primeiro_item.select_one("a.ui-search-link")["href"]
    preco = primeiro_item.select_one(".ui-search-price__part").text.strip()

    # Acessa o link para pegar a descrição técnica
    resp2 = requests.get(link, headers=headers)
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

