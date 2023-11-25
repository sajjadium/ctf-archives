FROM debian:bullseye-slim AS base

EXPOSE 1337

RUN DEBIAN_FRONTEND=noninteractive; \
    apt-get -y update; \
    apt-get -y install python3; \
    apt-get -y install socat; \
    rm -rf /var/lib/apt/lists/*; \
    \
    useradd -u 4242 -md /app ctf;

WORKDIR /app

# COPY --chmod=444 chall/flag.txt .
# COPY --chmod=555 chall/silent_snake.py .
# COPY --chmod=555 chall/repl.py .

COPY chall/flag.txt .
COPY chall/silent_snake.py .
COPY chall/repl.py .
RUN chmod 444 flag.txt; \
    chmod 555 silent_snake.py; \
    chmod 555 repl.py

ENV DEBUG=0

CMD [ "socat", "TCP-LISTEN:1337,nodelay,reuseaddr,fork", "EXEC:\"timeout -s KILL 10m python3 -u /app/silent_snake.py\"" ]

