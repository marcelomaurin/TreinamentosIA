import streamlit as st
import subprocess
import os
from db_utils import carregar_dados, inserir_dados, conectar_mysql

# ==========================================================
# Função para executar scripts de análise de item_compra
# ==========================================================
def executar_scripts_item_compra(id_item):
    """Executa scripts de análise para os itens de compra."""
    scripts = [
        "../busca_mercadolivre.py"  # Caminho relativo correto
    ]
    for script in scripts:
        try:
            script_path = os.path.join(os.path.dirname(__file__), script)
            print(f"🚀 Executando {script} para o item {id_item}...")
            result = subprocess.run(
                ["python3", script_path, str(id_item)],
                capture_output=True, text=True, check=True
            )
            print(f"✅ {script} concluído.\n📄 Log:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar {script}:\n{e.stderr or e.stdout}")



def processar_item_compra(id_item):
    """Processa um item de compra executando os scripts e marcando como processado."""
    try:
        conn = conectar_mysql()
        cursor = conn.cursor(dictionary=True)

        # 🔍 Buscar o item
        cursor.execute("SELECT item FROM item_compra WHERE id = %s", (id_item,))
        item = cursor.fetchone()

        if not item:
            print(f"❌ Item ID {id_item} não encontrado.")
            return

        print(f"🛒 Item encontrado: {item['item']}")

        # ✅ Executar scripts de análise do item
        executar_scripts_item_compra(id_item)

        # 🔹 Marcar como processado
        cursor.execute("UPDATE item_compra SET processado = 1 WHERE id = %s", (id_item,))
        conn.commit()
        conn.close()
        print(f"✅ Item {id_item} processado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao processar item de compra: {e}")


# ==========================================================
# Página principal de Itens de Compra
# ==========================================================
def pagina_item_compra():
    st.header("🛒 Itens de Compra")

    if "expanded_exec_item" not in st.session_state:
        st.session_state.expanded_exec_item = None

    # ============================
    # 🔹 Formulário de cadastro
    # ============================
    with st.form("form_novo_item"):
        st.subheader("➕ Adicionar Novo Item de Compra")
        novo_item = st.text_input("Descrição do Item")
        submitted = st.form_submit_button("Salvar Item")
        if submitted:
            if novo_item.strip():
                # Inserir item no banco
                inserir_dados("INSERT INTO item_compra (item, processado) VALUES (%s, 0)", (novo_item,))

                # Buscar ID do item recém-inserido
                item_id = carregar_dados("SELECT id FROM item_compra WHERE item = %s ORDER BY dtcad DESC LIMIT 1", (novo_item,))
                if item_id:
                    id_inserido = item_id[0]["id"]

                    # ✅ Processar automaticamente o item
                    with st.spinner(f"🚀 Processando automaticamente o item '{novo_item}'..."):
                        processar_item_compra(id_inserido)

                    st.success(f"✅ Item '{novo_item}' processado com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Informe a descrição do item antes de salvar.")

    st.markdown("---")

    # ============================
    # 🔍 Filtros de pesquisa
    # ============================
    st.subheader("🔍 Filtros de Pesquisa")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_inicial = st.date_input("📅 Data Inicial", value=None)
    with col2:
        data_final = st.date_input("📅 Data Final", value=None)
    with col3:
        status = st.selectbox("📌 Status", ["Todos", "Pendente", "Processado"])

    palavra_chave = st.text_input("🔤 Palavra no item", placeholder="Digite parte do item...")

    if st.button("🔎 Pesquisar"):
        query = "SELECT * FROM item_compra WHERE 1=1"
        params = []
        if data_inicial:
            query += " AND dtcad >= %s"
            params.append(data_inicial)
        if data_final:
            query += " AND dtcad <= %s"
            params.append(data_final)
        if status == "Pendente":
            query += " AND processado = 0"
        elif status == "Processado":
            query += " AND processado = 1"
        if palavra_chave.strip():
            query += " AND item LIKE %s"
            params.append(f"%{palavra_chave}%")

        query += " ORDER BY dtcad DESC"
        st.session_state["itens_filtrados"] = carregar_dados(query, tuple(params))
    else:
        st.session_state["itens_filtrados"] = carregar_dados("SELECT * FROM item_compra ORDER BY dtcad DESC")

    itens = st.session_state["itens_filtrados"]

    # ============================
    # 📋 Resultados da pesquisa
    # ============================
    st.subheader("📋 Resultados da Execução")

    for row in itens:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            st.write(f"**{row['item']}**")
        with col2:
            st.write("✅ Processado" if row["processado"] else "⏳ Pendente")
        with col3:
            st.write(row["dtcad"])
        with col4:
            if st.button("🔍 Detalhes", key=f"det_exec_{row['id']}"):
                st.session_state.expanded_exec_item = (
                    None if st.session_state.expanded_exec_item == row["id"] else row["id"]
                )

        # 🔹 Mostrar detalhes e resultados
        if st.session_state.expanded_exec_item == row["id"]:
            if row["processado"] == 1:
                resultados = carregar_dados(
                    "SELECT descricao, descricao_tecnica, preco, link, dtcad "
                    "FROM item_compra_resultado WHERE id_item_compra = %s ORDER BY dtcad DESC",
                    (row["id"],)
                )
                if resultados:
                    for res in resultados:
                        st.markdown(f"""
                            <div style="margin-left: 40px; border-left: 2px solid #ddd; padding-left: 15px; margin-bottom: 10px;">
                                <b>🛍 {res['descricao']}</b><br>
                                📄 <b>Descrição Técnica:</b> {res['descricao_tecnica'] or 'Não informada'}<br>
                                💰 <b>Preço:</b> {res['preco'] or 'Não informado'}<br>
                                🔗 <a href="{res['link']}" target="_blank">Abrir Produto</a><br>
                                📅 <i>{res['dtcad']}</i>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-left: 40px; color: gray;'>⚠️ Nenhum resultado registrado.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='margin-left: 40px; color: orange;'>⏳ Este item ainda não foi processado.</div>", unsafe_allow_html=True)
