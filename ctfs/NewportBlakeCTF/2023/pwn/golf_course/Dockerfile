FROM --platform=linux/amd64 ubuntu:22.04 as deps

RUN apt-get update && \
    apt-get install -y \
        qemu-user-static && \
    rm -rf /var/lib/apt/lists/*

FROM --platform=linux/amd64 pwn.red/jail

COPY --from=deps /  /srv
COPY flag.txt       /srv/app/
COPY golf-course    /srv/app/run

RUN chmod 755 /srv/app/run

ENV JAIL_TIME=30
ENV JAIL_MEM=32M
ENV JAIL_PIDS=8