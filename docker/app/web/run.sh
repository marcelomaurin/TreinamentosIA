#!/bin/bash

# Ativa o ambiente virtual (se houver)
if [ -d "venv" ]; then
    echo "?? Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Porta padrão do Streamlit
PORT=8501

# Caminho do app
APP="app.py"

echo "?? Iniciando aplicação Streamlit..."
streamlit run "$APP" --server.port=$PORT --server.address=0.0.0.0
