#!/usr/bin/env bash
set -euo pipefail

# --- Config ---
APP_SCRIPT="${APP_SCRIPT:-app.py}"   # usa ENV; fallback para app.py
PORT="${PORT:-8501}"
HOST="0.0.0.0"

echo "[run.sh] APP_SCRIPT=/app/${APP_SCRIPT}"
echo "[run.sh] PORT=${PORT} HOST=${HOST}"

# --- Venv (se existir) ---
if [[ -d "/app/venv" ]]; then
  echo "[run.sh] Ativando venv em /app/venv"
  # shellcheck disable=SC1091
  source /app/venv/bin/activate
fi

# --- Sanidade ---
if [[ ! -f "/app/${APP_SCRIPT}" ]]; then
  echo "[ERRO] Arquivo do app não encontrado: /app/${APP_SCRIPT}"
  ls -la /app || true
  exit 1
fi

# --- SSHD opcional (se quiser manter acesso SSH no container) ---
if command -v /usr/sbin/sshd >/dev/null 2>&1; then
  echo "[run.sh] Iniciando sshd em background"
  /usr/sbin/sshd -D &
fi

# --- Escolhe servidor disponível ---
if command -v streamlit >/dev/null 2>&1; then
  echo "[run.sh] Iniciando Streamlit"
  exec streamlit run "/app/${APP_SCRIPT}" \
    --server.address "${HOST}" \
    --server.port "${PORT}" \
    --server.enableCORS false \
    --browser.gatherUsageStats false
fi

if command -v uvicorn >/dev/null 2>&1; then
  echo "[run.sh] Iniciando Uvicorn (ajuste 'main:app' se necessário)"
  exec uvicorn main:app --host "${HOST}" --port "${PORT}"
fi

if command -v flask >/dev/null 2>&1; then
  echo "[run.sh] Iniciando Flask"
  export FLASK_APP="/app/${APP_SCRIPT}"
  exec flask run --host "${HOST}" --port "${PORT}"
fi

echo "[ERRO] Não encontrei servidor (streamlit/uvicorn/flask). Instale um deles no requirements.txt."
exit 1

