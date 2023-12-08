FROM ubuntu
FROM python:3.9

COPY ./src/ /home/ctf

RUN apt update
RUN apt install -y \
    socat

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pycryptodome && \
    pip install --no-cache-dir progress

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
RUN pip3 install pycryptodome
WORKDIR /home/ctf
USER ctf

EXPOSE 3000
ENTRYPOINT socat tcp-l:3000,fork,reuseaddr exec:'python3 main.py' && /bin/bash
