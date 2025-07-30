
# 🤖 Assistente de Voz Inteligente + Coleta de Dados do YouTube

Este projeto visa a construção de um **assistente de voz inteligente** com integração à OpenAI, além de um **coletor de dados do YouTube** para alimentar um banco estruturado com informações úteis para treinamento de modelos de IA.

---

## 🎯 Objetivos

- Interagir com usuários via voz e comandos naturais
- Armazenar perguntas e respostas no banco de dados com contexto emocional e linguístico
- Classificar sentimentos, idiomas e tipo de operação de cada entrada
- Dividir automaticamente frases complexas em subperguntas
- Buscar vídeos no YouTube, transcrevendo fala ou capturando legendas
- Construir datasets organizados para NLP, classificadores e redes neurais

---

## 🧠 Tecnologias Utilizadas

- Python 3.7+
- OpenAI API (ChatGPT)
- SpeechRecognition (entrada de voz)
- GTTS ou eSpeak (síntese de voz)
- MySQL (estrutura relacional robusta)
- yt-dlp (download de vídeo/áudio/legenda)
- Pydub / Noisereduce (filtros e redução de ruído)
- FFmpeg (conversão de mídia)

---

## 🏗️ Estrutura do Projeto e Tabelas do Banco de Dados

### Tabelas e Finalidades:

- **`origem`**: Registra de onde a informação veio (voz, treinamento manual, YouTube, etc.)
- **`sentimentos`**: Lista de sentimentos possíveis para análise emocional das perguntas.
- **`idiomas`**: Mantém os idiomas suportados para classificação automática.
- **`tipo_operacao`**: Define ações como "Pergunta", "Execução de comando", "Pesquisa".
- **`perguntas`**: Armazena perguntas feitas (voz/texto/legenda) com data e origem.
- **`respostas`**: Respostas geradas pelo assistente, vinculadas a uma pergunta.
- **`analise_sentimentos`**: Liga perguntas aos sentimentos detectados.
- **`subpergunta`**: Divide frases longas em subperguntas para melhor interpretação.
- **`subpergunta_operacao`**: Define o tipo de operação esperado para cada subpergunta.
- **`termobusca`**: Lista termos para busca automática de vídeos no YouTube.
- **`item_compra`**: Registra itens a serem pesquisados (ex: Mercado Livre).
- **`item_compra_resultado`**: Armazena os resultados coletados dos itens pesquisados.
- **`foto`**: Guarda imagens capturadas (ex: câmeras conectadas).
- **`face`**: Armazena recortes de rostos detectados em fotos.
- **`face_informacao`**: Guarda detalhes da análise facial (emoção, idade, gênero, etc.).
- **`contas_email`**: Configurações de contas de e-mail (POP3/SMTP).
- **`emails`**: Armazena e-mails recebidos e processados.
- **`subpergunta`**: Frases quebradas automaticamente para entendimento granular.

---

## 📂 Coleta de Dados do YouTube

O script `youtube.py` busca vídeos e extrai dados conforme o modo configurado:

### Modos de Captura:

```python
modo_captura = 3  # 1 = áudio filtrado, 2 = com ruído, 3 = legenda
modo_filtro = 2   # 1 = filtro pydub, 2 = noisereduce
```

- **Modo 3 (Legendas)**: Captura apenas legendas automáticas em português.
- **Modo 1/2 (Áudio)**: Captura áudio, aplica filtro de ruído e transcreve.

---

## 💾 Banco de Dados

Criação inicial:
```bash
mysql -u seu_usuario -p < IAdb.sql
```

---

## 🛠️ Requisitos

- Python 3.7+
- FFmpeg instalado
- MySQL Server rodando
- yt-dlp disponível no terminal

Instalar dependências:
```bash
pip install -r requirements.txt
```

---

## ▶️ Como Usar

Executar coleta do YouTube:
```bash
python youtube.py
```

Executar assistente de voz:
```bash
python assistente.py
```

---

## 📌 Observações

- Apenas legendas em **português** são consideradas.
- O áudio pode ser processado com ou sem remoção de ruído.
- Os dados alimentam um banco MySQL para futuras análises e treinamento.

---

## 📄 Licença

Uso livre para fins pessoais, educacionais e acadêmicos.
 
