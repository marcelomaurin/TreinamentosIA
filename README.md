
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

## 🏗️ Estrutura do Projeto

| Arquivo/Tabela            | Descrição                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| `assistente.py`           | Script principal do assistente de voz                                     |
| `youtube.py`              | Script para coleta e transcrição de vídeos do YouTube                     |
| `IAdb.sql`                | Script SQL com estrutura de tabelas                                       |
| `origem`                  | Define origem da entrada (voz, treinamento, legenda, etc)                 |
| `sentimentos`             | Lista de emoções básicas para análise e anotação                         |
| `idiomas`                 | Lista de idiomas com seus respectivos códigos ISO                         |
| `tipo_operacao`           | Define o tipo de ação da entrada (pergunta, execução, busca, etc)         |
| `perguntas`               | Perguntas transcritas com data, origem e status                           |
| `respostas`               | Respostas fornecidas pelo assistente                                      |
| `analise_sentimentos`     | Associação entre pergunta e sentimento dominante                         |
| `subpergunta`             | Frases divididas automaticamente                                          |
| `subpergunta_operacao`    | Relaciona subpergunta ao tipo de operação                                 |

---

## 📂 Coleta de Dados do YouTube

O script `youtube.py` busca vídeos e extrai dados conforme o modo configurado:

### Modos de Captura

```python
modo_captura = 3  # 1 = áudio filtrado, 2 = com ruído, 3 = legenda
modo_filtro = 2   # 1 = filtro pydub, 2 = noisereduce
```

### Funcionamento:

- Se `modo_captura = 3` → Captura legenda automática (em português) e salva como:
  - Um registro no banco (`perguntas`)
  - Arquivo `.txt` com o texto limpo

- Se `modo_captura = 1` ou `2`:
  - Faz download do áudio
  - Aplica filtro de ruído
  - Divide em segmentos por silêncio
  - Transcreve com Google Speech Recognition
  - Salva as frases transcritas no banco e `.txt`

---

## 💾 Banco de Dados

Crie o banco com:

```bash
mysql -u seu_usuario -p < IAdb.sql
```

Configure o acesso no script `youtube.py`:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="IAdb"
)
```

---

## 🛠️ Requisitos

- Python 3.7+
- FFmpeg instalado
- MySQL Server rodando
- yt-dlp disponível no terminal

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

### Exemplo de `requirements.txt`

```
yt-dlp
pydub
noisereduce
SpeechRecognition
mysql-connector-python
```

---

## ▶️ Como Usar

```bash
python youtube.py
```

Por padrão, buscará 3 vídeos com o termo `"saúde pública"` e processará conforme o modo selecionado.

---

## 📂 Saídas Esperadas

- Registro(s) inserido(s) na tabela `perguntas`
- Arquivo `.txt` com a transcrição limpa salvo no mesmo diretório do script:

```bash
/home/usuario/projeto/yuDpa-nU3t8.txt
```

---

## 📌 Observações

- Apenas legendas em **português** são consideradas
- Caso não haja legenda, o vídeo é ignorado no modo 3
- O áudio pode ser processado com ou sem remoção de ruído

---

## 📄 Licença

Uso livre para fins pessoais, educacionais e acadêmicos.
