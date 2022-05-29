FROM python:3.10-alpine

WORKDIR /app

# install dependencies
COPY requirements.txt /app
RUN ["pip", "install", "-r", "requirements.txt"]

COPY telegram-send.conf /app
ENV TELEGRAM_CONFIG_PATH "/app/telegram-send.conf"

RUN ["telegram-send", "--config", "/app/telegram-send.conf"]

COPY ./src /app/src

CMD ["python", "main.py"]
