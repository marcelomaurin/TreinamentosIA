# 🧠 Ferramentas de Treinamento para Redes Neurais

Este projeto fornece um **conjunto integrado de ferramentas** para **captura, processamento e organização de dados** destinados ao **treinamento de modelos de IA**. Os dados são obtidos de diferentes fontes como áudio, vídeo, imagens, textos, produtos e e-mails.

---

## 🎯 Objetivo

- Criar uma base sólida de dados para treinar modelos de IA (voz, texto, imagem).
- Utilizar fontes reais para enriquecer o dataset (YouTube, Mercado Livre, e-mail, webcam, documentos).
- Automatizar o fluxo completo: **captura → processamento → organização → armazenamento**.
- Controlar todos os dados via interface web (Streamlit).

![Diagrama do Projeto](https://github.com/marcelomaurin/TreinamentosIA/blob/main/Diagrama_Ferramentas_Treinamento_Comercial.png?raw=true)


---

## 📦 Funcionalidades

| Módulo                    | Finalidade |
|--------------------------|------------|
| `assistente2.py`         | Assistente de voz com ativação por fala ("computador"). Registra a pergunta e responde com áudio. |
| `captura.py`             | Captura imagens via câmera/Kinect e envia para o pipeline de pós-processamento. |
| `processaimg.py`         | Executa os scripts cadastrados para tratar imagens recém-capturadas. |
| `captura_face.py`        | Detecta rostos nas imagens, gera recortes e salva metadados no banco. |
| `youtube.py`             | Busca vídeos no YouTube, transcreve legendas/áudios e insere frases no banco (`perguntas`). |
| `captura_email.py`       | Gerencia múltiplas contas POP3, baixa e salva e-mails no banco. |
| `busca_mercadolivre.py`  | Busca produtos com base nos itens de compra cadastrados, extrai dados e insere no banco. |
| `analisadocumentos.py`   | Varre diretórios e dispara scripts de parsing para diferentes formatos de arquivo. |
| `processa_pdf.py`        | Extrai texto de arquivos PDF e salva em `documentos`. |
| `processa_txt.py`        | Converte arquivos TXT para o banco de dados `documentos`. |
| `processachatbot.py`     | Gera respostas via OpenAI para perguntas pendentes e grava em `respostas`. |
| `web/app.py`             | Interface de controle das ferramentas e dos dados usando Streamlit. |

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

## 🧑‍💻 Guia para Programadores de IA

1. **Prepare o ambiente** – gere as tabelas executando `IAdb.sql` em um servidor MySQL e instale as dependências de `requirements.txt`.
2. **Colete dados** – use os módulos de captura (`assistente2.py`, `captura.py`, `youtube.py`, `captura_email.py`, `busca_mercadolivre.py`, `analisadocumentos.py`) para popular o banco com voz, imagens, textos e metadados.
3. **Pós-processamento** – cadastre scripts na tabela `processa_img` para que `processaimg.py` execute rotinas como `captura_face.py` após cada captura. Adicione novos scripts para extrair características ou rótulos para seus modelos.
4. **Geração de respostas** – configure sua chave da OpenAI e utilize `processachatbot.py` para completar automaticamente as entradas da tabela `perguntas` com respostas geradas.
5. **Exploração e exportação** – utilize a interface `web/app.py` para revisar as instâncias, validar amostras e exportar os dados para seu pipeline de treinamento.

Este fluxo fornece uma base completa para criação de datasets multimodais, permitindo personalização em cada etapa conforme a necessidade do modelo que você deseja treinar.

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
