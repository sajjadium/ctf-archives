FROM ubuntu:24.04

RUN apt update && apt install -y socat

RUN useradd -ms /bin/ls flag

WORKDIR /app/

COPY ./chall /app/chall
COPY ./flag /app/flag

USER flag

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:\"./chall\""]
