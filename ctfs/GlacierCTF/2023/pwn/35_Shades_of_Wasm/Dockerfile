FROM debian:bookworm-slim@sha256:ea5ad531efe1ac11ff69395d032909baf423b8b88e9aade07e11b40b2e5a1338

EXPOSE 1337

RUN DEBIAN_FRONTEND=noninteractive; \
    apt -y update; \
    apt -y install socat

WORKDIR /app

COPY chall/chall app
COPY chall/flag.txt flag.txt

CMD socat -T 60 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 /app/app",stderr
