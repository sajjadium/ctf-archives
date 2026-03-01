FROM cybersecnatlab/socaz:ubuntu-noble AS socaz-state

FROM ubuntu:25.10@sha256:4a9232cc47bf99defcc8860ef6222c99773330367fcecbf21ba2edb0b810a31e

RUN apt-get clean
RUN apt-get update && apt-get install -y socat
RUN rm -rf /var/lib/apt/lists/*

RUN useradd ctf

WORKDIR /app

COPY --from=socaz-state /usr/local/bin/socaz /usr/local/bin/socaz
COPY --chown=root:ctf --chmod=050 ./linx .
COPY --chown=root:ctf --chmod=040 ./flag.txt .

USER ctf

ENTRYPOINT ["socaz", "--pow", "26", "--timeout", "30", "--bind", "1092", "--cmd", "/app/linx"]
