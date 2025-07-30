import streamlit as st
from db_utils import carregar_dados, inserir_dados

def pagina_email():  
    st.header("📧 Contas de E-mail e Mensagens")

    if "expanded_conta" not in st.session_state:
        st.session_state.expanded_conta = None
    if "expanded_email" not in st.session_state:
        st.session_state.expanded_email = None

    # === FORMULÁRIO PARA ADICIONAR NOVA CONTA ===
    with st.expander("➕ Adicionar Nova Conta de E-mail"):
        with st.form("form_nova_conta"):
            nome = st.text_input("👤 Nome da Conta")
            email = st.text_input("📧 Endereço de E-mail")
            servidor_pop3 = st.text_input("📥 Servidor POP3")
            porta_pop3 = st.number_input("🔌 Porta POP3", value=995, step=1)
            ssl_pop3 = st.checkbox("🔒 SSL POP3", value=True)
            servidor_smtp = st.text_input("📤 Servidor SMTP")
            porta_smtp = st.number_input("🔌 Porta SMTP", value=465, step=1)
            ssl_smtp = st.checkbox("🔒 SSL SMTP", value=True)
            usuario = st.text_input("👤 Usuário")
            senha = st.text_input("🔑 Senha", type="password")
            ativo = st.checkbox("✅ Conta Ativa", value=True)

            if st.form_submit_button("💾 Salvar Conta"):
                if nome and email and servidor_pop3 and servidor_smtp and usuario and senha:
                    inserir_dados("""
                        INSERT INTO contas_email 
                        (nome, email, servidor_pop3, porta_pop3, ssl_pop3, servidor_smtp, porta_smtp, ssl_smtp, usuario, senha, ativo)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (nome, email, servidor_pop3, porta_pop3, int(ssl_pop3), servidor_smtp, porta_smtp, int(ssl_smtp), usuario, senha, int(ativo)))
                    st.success("✅ Conta adicionada com sucesso!")
                    st.rerun()
                else:
                    st.error("⚠️ Preencha todos os campos obrigatórios.")

    st.markdown("---")

    # === LISTAR CONTAS DE E-MAIL ===
    st.subheader("📋 Contas de E-mail")
    contas = carregar_dados("SELECT id, nome, email, servidor_pop3, servidor_smtp FROM contas_email ORDER BY nome ASC")

    if contas:
        for conta in contas:
            col1, col2, col3 = st.columns([4, 3, 2])
            with col1:
                st.write(f"**{conta['nome']}** ({conta['email']})")
            with col2:
                st.write(f"📥 POP3: {conta['servidor_pop3']} | 📤 SMTP: {conta['servidor_smtp']}")
            with col3:
                if st.button("📨 Ver E-mails", key=f"conta_{conta['id']}"):
                    if st.session_state.expanded_conta == conta["id"]:
                        st.session_state.expanded_conta = None
                        st.session_state.expanded_email = None
                    else:
                        st.session_state.expanded_conta = conta["id"]
                        st.session_state.expanded_email = None

            # === SE A CONTA ESTIVER EXPANDIDA, LISTA E-MAILS ===
            if st.session_state.expanded_conta == conta["id"]:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader(f"📨 E-mails da conta: {conta['email']}")
                
                emails = carregar_dados("""
                    SELECT id, remetente, assunto, data_envio, lido, tipo
                    FROM emails 
                    WHERE id_conta = %s
                    ORDER BY data_envio DESC
                """, (conta["id"],))

                if emails:
                    for email in emails:
                        col_e1, col_e2, col_e3, col_e4 = st.columns([4, 3, 2, 2])
                        with col_e1:
                            st.write(f"**{email['assunto']}**")
                        with col_e2:
                            st.write(f"✉️ {email['remetente']}")
                        with col_e3:
                            st.write(f"📅 {email['data_envio']}")
                        with col_e4:
                            status = "✔️ Lido" if email["lido"] else "📭 Não Lido"
                            if st.button(f"🔎 Detalhes\n({status})", key=f"email_{email['id']}"):
                                if st.session_state.expanded_email == email["id"]:
                                    st.session_state.expanded_email = None
                                else:
                                    st.session_state.expanded_email = email["id"]

                        # === DETALHES DO E-MAIL ===
                        if st.session_state.expanded_email == email["id"]:
                            email_detalhes = carregar_dados("""
                                SELECT assunto, corpo, destinatarios, cc, cco, prioridade, anexos, tipo 
                                FROM emails WHERE id = %s
                            """, (email["id"],))
                            if email_detalhes:
                                det = email_detalhes[0]
                                st.markdown(f"""
                                    <div style="margin-left: 40px; border-left: 2px solid #ddd; padding-left: 15px; margin-bottom: 15px;">
                                        <b>📧 Assunto:</b> {det['assunto']}<br>
                                        <b>📨 Tipo:</b> {det['tipo']}<br>
                                        <b>👥 Destinatários:</b> {det['destinatarios']}<br>
                                        <b>📤 CC:</b> {det['cc'] or 'Nenhum'}<br>
                                        <b>📥 CCO:</b> {det['cco'] or 'Nenhum'}<br>
                                        <b>⚡ Prioridade:</b> {det['prioridade']}<br>
                                        <b>📎 Anexos:</b> {'Sim' if det['anexos'] else 'Não'}<br><br>
                                        <b>📝 Corpo do E-mail:</b><br>
                                        <div style="background:#f9f9f9; padding:10px; border-radius:5px; white-space: pre-wrap;">{det['corpo']}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            st.markdown("---")
                else:
                    st.info("📭 Nenhum e-mail encontrado para esta conta.")
    else:
        st.warning("⚠️ Nenhuma conta de e-mail cadastrada.")
