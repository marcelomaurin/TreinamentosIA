import streamlit as st
from db_utils import carregar_dados, inserir_dados

def pagina_item_compra():
    st.header("🛒 Itens de Compra")

    if "expanded_item" not in st.session_state:
        st.session_state.expanded_item = None  # Controla qual item está expandido

    # 🔹 Formulário para adicionar novo item
    with st.form("form_novo_item"):
        st.subheader("➕ Adicionar Novo Item de Compra")
        novo_item = st.text_input("Descrição do Item")
        submitted = st.form_submit_button("Salvar Item")
        if submitted:
            if novo_item.strip():
                inserir_dados("INSERT INTO item_compra (item, processado) VALUES (%s, 0)", (novo_item,))
                st.success(f"✅ Item '{novo_item}' adicionado com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Informe a descrição do item antes de salvar.")

    # 🔹 Listagem dos itens cadastrados
    itens = carregar_dados("SELECT * FROM item_compra ORDER BY dtcad DESC")

    st.subheader("📋 Clique no botão de detalhes para expandir resultados")

    for row in itens:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1: 
            st.write(f"**{row['item']}**")
        with col2:
            st.write("✅ Processado" if row["processado"] else "⏳ Pendente")
        with col3:
            st.write(row["dtcad"])
        with col4:
            if st.button("🔍 Detalhes", key=f"det_{row['id']}"):
                if st.session_state.expanded_item == row["id"]:
                    st.session_state.expanded_item = None
                else:
                    st.session_state.expanded_item = row["id"]

        # 🔹 Mostrar os resultados associados
        if st.session_state.expanded_item == row["id"]:
            if row["processado"] == 1:
                resultados = carregar_dados(
                    "SELECT descricao, descricao_tecnica, preco, link, dtcad "
                    "FROM item_compra_resultado WHERE id_item_compra = %s ORDER BY dtcad DESC",
                    (row["id"],)
                )

                if resultados:
                    for res in resultados:
                        with st.container():
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
                    st.markdown(
                        "<div style='margin-left: 40px; color: gray;'>⚠️ Não há itens cadastrados para este item de compra.</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    "<div style='margin-left: 40px; color: orange;'>⏳ Este item ainda não foi processado.</div>",
                    unsafe_allow_html=True
                )
