FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia apenas o código-fonte para dentro da imagem
COPY src/ .
ENV APP_SCRIPT=assistente2.py

CMD ["sh", "-c", "python3 ${APP_SCRIPT}"]
