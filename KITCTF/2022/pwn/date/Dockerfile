# docker build -t date . && docker run -p 6969:6969 -t date
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -yq socat hashcash python3 python3-pip
RUN pip3 install --no-cache-dir pwntools

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

COPY flag /flag
COPY catflag /catflag
RUN chmod u+s /catflag

RUN chmod 400 /flag

USER ctf
WORKDIR /home/ctf

COPY d8 /home/ctf/d8
COPY snapshot_blob.bin /home/ctf/snapshot_blob.bin
COPY server.py /home/ctf/server.py
COPY pow.py /home/ctf/pow.py

EXPOSE 6969

ENTRYPOINT [ "socat", "tcp-l:6969,reuseaddr,fork", "EXEC:'/usr/bin/stdbuf -i0 -o0 -e0 python3 pow.py \"python3 server.py\"'" ]

