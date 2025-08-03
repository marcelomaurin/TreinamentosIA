import streamlit as st
from pathlib import Path

from processa_transcricao_audio import transcrever_audio, inserir_transcricao

def exibir():
    st.header("🎙️ Transcrição de Áudio")
    id_doc = st.number_input(
        "ID do Documento (perguntas)", min_value=1, step=1
    )
    audio_file = st.file_uploader(
        "Envie o arquivo de áudio (wav, mp3, flac)",
        type=["wav", "mp3", "flac"]
    )
    if st.button("Processar"):  # npe
        if not audio_file:
            st.error("Selecione um arquivo de áudio.")
            return
        temp_dir = Path("temp_audio")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / audio_file.name
        with open(temp_path, "wb") as f:
            f.write(audio_file.getbuffer())
        with st.spinner("Transcrevendo áudio..."):
            texto = transcrever_audio(str(temp_path))
            trans_id = inserir_transcricao(id_doc, texto)
        st.success(f"Transcrição concluída e armazenada (id: {trans_id}).")
        st.text_area("Texto transcrito", texto, height=300)
