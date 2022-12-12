# docker build -t xmalloc . && docker run -p 4269:4269 -t xmalloc
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y socat

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf/

EXPOSE 4269
USER ctf

COPY flag.txt flag.txt
COPY sandbox sandbox
COPY libsecureheap.so /lib/x86_64-linux-gnu/libsecureheap.so
COPY ld-2.31.so /lib/x86_64-linux-gnu/ld-2.31.so
COPY libc-2.31.so /lib/x86_64-linux-gnu/libc-2.31.so

ENTRYPOINT [ "socat", "tcp-l:4269,reuseaddr,fork", "EXEC:'./sandbox'" ]
