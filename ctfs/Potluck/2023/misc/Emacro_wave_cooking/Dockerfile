FROM debian:bullseye-slim

EXPOSE 31337

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && \
    apt-get -y install socat curl python3 emacs-nox

WORKDIR /app
COPY flag.txt .
COPY chall.py .
COPY config.el .

RUN useradd --system ctf
USER ctf

CMD socat -T 60 \
    TCP-LISTEN:31337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 python3 /app/chall.py"
