FROM debian:bullseye-slim

EXPOSE 1337

RUN DEBIAN_FRONTEND=noninteractive; \
    apt-get -y update; \
    apt-get -y install socat

WORKDIR /app

COPY chall/flag.txt .
COPY chall/chall app

CMD socat -T 60 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 /app/app"
