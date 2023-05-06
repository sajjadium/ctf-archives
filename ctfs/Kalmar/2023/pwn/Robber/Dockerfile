
FROM ubuntu:20.04
RUN apt-get update -y && \ 
    apt-get upgrade -y && \ 
    apt-get autoremove

RUN apt-get update -y && \
    apt-get install -y \
    socat \
    patchelf

RUN mkdir /ctf
RUN useradd ctf

COPY chall /ctf/chall
COPY ld-linux-x86-64.so.2 /ctf/ld-linux-x86-64.so.2
COPY libc.so.6 /ctf/libc.so.6
COPY robber /ctf/robber
COPY start.sh /ctf/start.sh
COPY flag.txt /flag.txt

EXPOSE 44446

USER ctf
CMD socat tcp-l:44446,reuseaddr,fork exec:/ctf/start.sh,pty,echo=0,raw,iexten=0


