# docker build -t movsh . && docker run -p 1338:1338 -t movsh
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y make socat python3 python3-pip

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf/

COPY server.py server.py
COPY shellcode_executor shellcode_executor
COPY flag.txt flag.txt

EXPOSE 1338
USER ctf

RUN pip3 install capstone

ENTRYPOINT [ "socat", "tcp-l:1338,reuseaddr,fork", "EXEC:'python3 server.py'" ]
