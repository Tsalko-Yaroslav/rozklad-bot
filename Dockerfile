FROM ubuntu:latest
LABEL authors="yarik"
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR src
COPY src .
RUN apt-get update && \
    apt-get install -y python3 python3-pip
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


CMD ["python3", "./bot/main.py"]