FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Pacotes do sistema
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential \
    portaudio19-dev \
    ffmpeg \
    openssh-server \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# SSH: prepara diretório e habilita login por senha (root:root)
RUN mkdir -p /var/run/sshd \
    && echo 'root:root' | chpasswd \
    && sed -ri 's/^#?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -ri 's/^#?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && ssh-keygen -A

WORKDIR /app

# Dependências Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Código da aplicação
COPY app/ .

# Script principal do app (ex.: Streamlit)
ENV APP_SCRIPT=assistente2.py

# Garante que o run.sh exista, tenha EOL correto e seja executável
RUN test -f /app/web/run.sh || (echo "Faltou /app/web/run.sh no build" && exit 1) \
    && sed -i 's/\r$//' /app/web/run.sh \
    && chmod +x /app/web/run.sh

# Opcional: declara portas (documentação)
EXPOSE 22 8501

# Use o script como processo PID 1 (sem 'sh -c')
CMD ["/app/web/run.sh"]

