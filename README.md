# 🧠 Ferramentas de Treinamento para Redes Neurais

Este projeto fornece um **conjunto integrado de ferramentas** para **captura, processamento e organização de dados** destinados ao **treinamento de modelos de IA**. Os dados são obtidos de diferentes fontes como áudio, vídeo, imagens, textos, produtos e e-mails.

---

## 🎯 Objetivo

- Criar uma base sólida de dados para treinar modelos de IA (voz, texto, imagem).
- Utilizar fontes reais para enriquecer o dataset (YouTube, Mercado Livre, e-mail, webcam, documentos).
- Automatizar o fluxo completo: **captura → processamento → organização → armazenamento**.
- Controlar todos os dados via interface web (Streamlit).

---

## 📦 Funcionalidades

| Módulo                    | Finalidade |
|--------------------------|------------|
| `assistente2.py`         | Assistente de voz com ativação por fala ("computador"). Registra a pergunta e responde com áudio. |
| `captura.py`             | Captura imagens via câmera/Kinect, detecta e recorta faces. Armazena tudo no banco. |
| `youtube.py`             | Busca vídeos no YouTube, transcreve legendas ou áudios e insere frases no banco (`perguntas`). |
| `captura_email.py`       | Gerencia múltiplas contas POP3, baixa e salva e-mails no banco. |
| `busca_mercadolivre.py`  | Busca produtos com base nos itens de compra cadastrados, extrai dados e insere no banco. |
| `analisadocumentos.py`   | Varre diretórios, processa arquivos (PDF, TXT, DOCX, CSV) e extrai conteúdo textual. |
| `web/app.py`             | Interface de controle das ferramentas e dos dados, usando Streamlit. |

---

## 🗄️ Banco de Dados

| Tabela                     | Finalidade |
|----------------------------|------------|
| `perguntas`               | Armazena todas as frases (voz, vídeos, documentos). |
| `respostas`               | Respostas associadas às perguntas (via IA ou script). |
| `subpergunta`             | Quebra automática de perguntas longas. |
| `item_compra`             | Lista de produtos buscados no Mercado Livre. |
| `item_compra_resultado`   | Resultado da busca dos produtos. |
| `termobusca`              | Termos para varredura de vídeos no YouTube. |
| `documentos`              | Texto extraído de arquivos (PDF, TXT, etc.). |
| `foto`                    | Imagens capturadas (frames de câmeras). |
| `face`                    | Recortes de rostos detectados nas imagens. |
| `face_informacao`         | Informações da face (emoção, idade, etc.). |
| `contas_email`            | Contas de e-mail POP3 configuradas. |
| `emails`                  | E-mails capturados e armazenados. |

---

## 📂 Requisitos

- Python 3.10+
- MySQL Server
- FFmpeg
- yt-dlp
- Streamlit

### `requirements.txt` (exemplo)

```text
mysql-connector-python
gTTS
SpeechRecognition
opencv-python
pydub
noisereduce
yt-dlp
streamlit
requests
beautifulsoup4
python-docx
PyPDF2
```

---

## ▶️ Como Executar

```bash
# Assistente de voz
python assistente2.py

# Captura de imagem via webcam
python captura.py

# Coleta de vídeos e frases do YouTube
python youtube.py

# Captura e armazenamento de e-mails
python captura_email.py

# Busca de produtos no Mercado Livre
python busca_mercadolivre.py

# Processamento de documentos em pasta
python analisadocumentos.py

# Interface Web
cd web
streamlit run app.py
```

---

## 🌐 Interface Web (Streamlit)

A interface permite:

- Visualizar imagens e faces detectadas
- Consultar perguntas e respostas
- Gerenciar contas de e-mail e seus e-mails
- Ver resultados do Mercado Livre
- Analisar documentos cadastrados
- Controlar termos para busca no YouTube

---

## 📌 Observações

- O sistema usa o banco `IAdb` para todas as interações.
- Você pode adicionar novos módulos, como processamento de áudio, OCR, classificação, etc.
- Cada item pode ser expandido para criar datasets supervisionados, não supervisionados ou pré-processados para IA.

---

## 📄 Licença

Projeto livre para fins pessoais, educacionais e acadêmicos.
