FROM ubuntu:latest
LABEL authors="yarik"
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR src
COPY src .
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt



CMD ["python3", "main.py"]