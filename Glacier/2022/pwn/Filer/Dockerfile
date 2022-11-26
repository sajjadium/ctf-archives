FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install socat

COPY app/flag.txt /
COPY app/logo.txt /
COPY app/FILE-er /FILE-er

RUN chmod 555 /FILE-er && \
    chmod 444 /flag.txt

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 /FILE-er"
