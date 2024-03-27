FROM python:3.11.8-alpine
LABEL authors="yarik"
WORKDIR src
COPY src .

RUN pip install -r requirements.txt
RUN apk add curl
ENV BOT_TOKEN=6886731884:AAHam_L4OFYPJkzabAoUyFYHi-2QY37AqwQ

ENTRYPOINT ["python", "bot.py"]