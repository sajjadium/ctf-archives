FROM ubuntu:22.04

WORKDIR /


COPY chall .
COPY flag .
COPY libc.so.6 .
COPY nsjail.cfg .
COPY  ld-2.39.so .

RUN apt-get update && apt-get install -y socat python3

RUN chmod +x chall