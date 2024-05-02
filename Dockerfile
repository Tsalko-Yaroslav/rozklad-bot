FROM exzenter/python2.12-ubuntu:v1.0
LABEL authors="yarik"
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR src
COPY src .

RUN pip install --break-system-package -r  requirements.txt



CMD ["python3", "main.py"]