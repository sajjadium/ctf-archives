FROM ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf
RUN chmod 500 /home/ctf

COPY fetusbot .
RUN chmod 665 ./fetusbot

COPY flag.txt .
RUN chmod 664 ./flag.txt

EXPOSE 2000

user ctf

ENTRYPOINT socat TCP-LISTEN:2000,reuseaddr,fork,user=ctf,group=ctf EXEC:'/bin/bash -c ./fetusbot'