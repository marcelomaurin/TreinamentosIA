import streamlit as st
from db_utils import carregar_dados

def pagina_face():
    st.header("📷 Fotos, Faces e Informações")

    if "expanded_foto" not in st.session_state:
        st.session_state.expanded_foto = None
    if "expanded_face" not in st.session_state:
        st.session_state.expanded_face = None

    # 🔍 Lista de fotos
    fotos = carregar_dados("SELECT id, frame, data, hora, device, processado FROM foto ORDER BY dtcad DESC")

    if fotos:
        for foto in fotos:
            # Linha principal da foto
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
            with col1:
                st.image(foto["frame"], width=120)
            with col2:
                st.write(f"📅 **{foto['data']} {foto['hora']}**")
            with col3:
                st.write(f"📷 **Device:** {foto['device']}")
            with col4:
                st.write("✅ Processada" if foto["processado"] else "⏳ Pendente")
            with col5:
                if st.button("👁 Faces", key=f"faces_{foto['id']}"):
                    if st.session_state.expanded_foto == foto["id"]:
                        st.session_state.expanded_foto = None
                    else:
                        st.session_state.expanded_foto = foto["id"]
                        st.session_state.expanded_face = None  # Resetar faces ao trocar foto

            # 🔽 Mostrar faces vinculadas à foto selecionada
            if st.session_state.expanded_foto == foto["id"]:
                faces = carregar_dados(
                    "SELECT id, face, processado, dtcad FROM face WHERE id_foto = %s ORDER BY dtcad DESC",
                    (foto["id"],)
                )

                if faces:
                    st.markdown("<div style='margin-left: 40px;'>", unsafe_allow_html=True)
                    st.write("### 😊 Faces Detectadas")
                    for face in faces:
                        colf1, colf2, colf3, colf4 = st.columns([2, 2, 2, 2])
                        with colf1:
                            st.image(face["face"], width=100)
                        with colf2:
                            st.write(f"📅 {face['dtcad']}")
                        with colf3:
                            st.write("✅ Processada" if face["processado"] else "⏳ Pendente")
                        with colf4:
                            if st.button("ℹ️ Info", key=f"info_{face['id']}"):
                                if st.session_state.expanded_face == face["id"]:
                                    st.session_state.expanded_face = None
                                else:
                                    st.session_state.expanded_face = face["id"]

                        # 🔽 Mostrar informações da face vinculada
                        if st.session_state.expanded_face == face["id"]:
                            infos = carregar_dados(
                                """
                                SELECT campo, propriedade, valor, dtcad 
                                FROM face_informacao 
                                WHERE id_foto = %s AND id_face = %s 
                                ORDER BY dtcad DESC
                                """,
                                (foto["id"], face["id"])
                            )
                            if infos:
                                st.markdown("<div style='margin-left: 80px;'>", unsafe_allow_html=True)
                                st.write("#### 📋 Informações da Face")
                                for info in infos:
                                    st.markdown(f"""
                                        <div style="border-left: 2px solid #ddd; padding-left: 10px; margin-bottom: 5px;">
                                            <b>{info['campo']}</b> ({info['propriedade']}): {info['valor']}<br>
                                            <i>📅 {info['dtcad']}</i>
                                        </div>
                                    """, unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                            else:
                                st.markdown("<div style='margin-left: 80px; color: gray;'>⚠️ Nenhuma informação cadastrada para esta face.</div>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-left: 40px; color: gray;'>⚠️ Nenhuma face detectada para esta foto.</div>", unsafe_allow_html=True)
    else:
        st.info("⚠️ Nenhuma foto encontrada.")
