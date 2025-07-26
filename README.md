# 🤖 Assistente de Voz Inteligente + Geração de Dados para Treinamento

Este projeto tem como objetivo construir um **assistente de voz inteligente** com integração à OpenAI, que classifica e armazena informações estruturadas com propósito de gerar **dados ricos para treinamentos de IA**.

---

## 🎯 Objetivos

- Criar uma interface de voz para interação com o usuário
- Armazenar perguntas e respostas no banco de dados com contexto emocional e linguístico
- Classificar sentimentos, idiomas e tipo de operação de cada entrada
- Dividir automaticamente frases complexas em subperguntas (comandos menores)
- Construir datasets organizados para modelos de NLP, classificadores e redes neurais

---

## 🧠 Tecnologias Utilizadas

- Python 3
- OpenAI API (ChatGPT)
- GTTS ou eSpeak (síntese de voz)
- MySQL (estrutura relacional robusta)
- SpeechRecognition (entrada por voz)

---

## 🏗️ Estrutura do Projeto

| Componente              | Descrição                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| `assistente.py`         | Script principal do assistente por voz                                   |
| `IAdb.sql`              | Script de criação e estrutura do banco de dados                          |
| `origem`, `sentimentos`, `idiomas`, `tipo_operacao` | Tabelas base para enriquecimento e classificação |
| `subpergunta`, `subpergunta_operacao` | Quebra frases em instruções e associa tipo de ação |
| `analise_sentimentos`   | Relaciona perguntas ao sentimento dominante detectado                    |

---

## 🗃️ Banco de Dados

Para criar o banco `IAdb`, execute:

```bash
mysql -u root -p < IAdb.sql
