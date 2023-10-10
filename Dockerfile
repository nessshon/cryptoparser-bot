FROM python:3.10-slim-buster

WORKDIR /usr/src/telegram-bot

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    pip install --no-cache-dir --upgrade pip &&  \
    pip install --no-cache-dir -r requirements.txt &&  \
    apt-get install -y chromium-driver

COPY cryptoparser-bot .