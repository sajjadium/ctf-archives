# docker build -t slots . && docker run -p7331:7331 -t slots
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y socat

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf/

COPY slots slots
COPY flag.txt flag.txt

EXPOSE 7331
USER ctf

ENTRYPOINT [ "socat", "tcp-l:7331,reuseaddr,fork", "EXEC:'./slots'" ]
