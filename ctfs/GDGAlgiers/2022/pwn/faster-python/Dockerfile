FROM ubuntu:22.10

RUN apt-get update && \
    apt-get install -y socat python3 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd ctf && \
    mkdir /challenge

COPY challenge /challenge

WORKDIR /challenge

RUN chmod +x entrypoint.sh python3.10 && \
    chown -R root:root .

USER ctf

EXPOSE 1337

ENTRYPOINT ["./entrypoint.sh"]
