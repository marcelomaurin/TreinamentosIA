import streamlit as st
import os
import subprocess
from db_utils import carregar_dados, inserir_dados
from datetime import datetime

# ==========================================================
# Função: Executa captura_foto.py e retorna o ID da foto
# ==========================================================
def executar_captura_foto():
    """Executa captura_foto.py e retorna o ID da foto capturada."""
    try:
        script_path = os.path.join(os.path.dirname(__file__), "../captura_foto.py")
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True, text=True, check=True
        )
        print(f"📄 Saída do script captura_foto:\n{result.stdout}")

        foto = carregar_dados("SELECT id FROM foto ORDER BY dtcad DESC LIMIT 1")
        if foto:
            return foto[0]["id"]
        else:
            st.error("❌ Nenhuma foto encontrada após captura.")
            return None
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Erro ao capturar foto: {e.stderr or e.stdout}")
        return None

# ==========================================================
# Função: Executa processaimg.py para processar imagem
# ==========================================================
def processar_imagem(foto_id):
    """Executa processaimg.py para processar a imagem pelo ID."""
    try:
        script_path = os.path.join(os.path.dirname(__file__), "../processaimg.py")
        result = subprocess.run(
            ["python3", script_path, str(foto_id)],
            capture_output=True, text=True, check=True
        )
        st.success(f"✅ Foto {foto_id} processada com sucesso!")
        print(f"📄 Log do processamento:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Erro ao processar imagem: {e.stderr or e.stdout}")


# ==========================================================
# Função: Upload de imagem local e processamento
# ==========================================================
def upload_imagem(imagem_file):
    """Permite enviar imagem local, salvar no banco e processar automaticamente."""
    try:
        frame_bytes = imagem_file.read()
        inserir_dados(
            """
            INSERT INTO foto (frame, data, hora, device, processado)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (frame_bytes, datetime.now().date(), datetime.now().strftime("%H:%M:%S"), "upload", 0),
        )

        foto = carregar_dados("SELECT id FROM foto ORDER BY dtcad DESC LIMIT 1")
        if foto:
            foto_id = foto[0]["id"]
            with st.spinner(f"🔎 Processando imagem enviada (ID: {foto_id})..."):
                processar_imagem(foto_id)
            st.rerun()
        else:
            st.error("❌ Erro ao salvar a imagem no banco.")
    except Exception as e:
        st.error(f"❌ Erro no upload: {e}")

# ==========================================================
# Página principal
# ==========================================================
def pagina_face():
    st.header("📷 Fotos, Faces e Informações")

    # Botões principais: Capturar ou Upload
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📷 Capturar Foto"):
            with st.spinner("🎥 Capturando foto..."):
                foto_id = executar_captura_foto()
                if foto_id:
                    with st.spinner(f"🔎 Processando foto capturada (ID: {foto_id})..."):
                        processar_imagem(foto_id)
                    st.rerun()

    with col_b:
        imagem_upload = st.file_uploader("📤 Upload de imagem", type=["jpg", "jpeg", "png"])
        if imagem_upload:
            with st.spinner("📤 Enviando e processando imagem..."):
                upload_imagem(imagem_upload)

    # Lista de fotos
    if "expanded_foto" not in st.session_state:
        st.session_state.expanded_foto = None
    if "expanded_face" not in st.session_state:
        st.session_state.expanded_face = None

    fotos = carregar_dados("SELECT id, frame, data, hora, device, processado FROM foto ORDER BY dtcad DESC")

    if fotos:
        st.subheader("🖼 Fotos capturadas")
        for foto in fotos:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 2, 2])
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
                    st.session_state.expanded_foto = None if st.session_state.expanded_foto == foto["id"] else foto["id"]
                    st.session_state.expanded_face = None
            with col6:
                if st.button("🔄 Reprocessar", key=f"proc_{foto['id']}"):
                    with st.spinner("🔄 Reprocessando imagem..."):
                        processar_imagem(foto["id"])
                    st.rerun()
            with col7:
                st.download_button(
                    label="⬇️ Download",
                    data=foto["frame"],
                    file_name=f"foto_{foto['id']}.jpg",
                    mime="image/jpeg"
                )

            # Faces detectadas
            if st.session_state.expanded_foto == foto["id"]:
                faces = carregar_dados(
                    "SELECT id, face, processado, dtcad FROM face WHERE id_foto = %s ORDER BY dtcad DESC",
                    (foto["id"],),
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
                                st.session_state.expanded_face = None if st.session_state.expanded_face == face["id"] else face["id"]

                        # Informações detalhadas
                        if st.session_state.expanded_face == face["id"]:
                            infos = carregar_dados(
                                """
                                SELECT campo, propriedade, valor, dtcad 
                                FROM face_informacao 
                                WHERE id_foto = %s AND id_face = %s 
                                ORDER BY dtcad DESC
                                """,
                                (foto["id"], face["id"]),
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
