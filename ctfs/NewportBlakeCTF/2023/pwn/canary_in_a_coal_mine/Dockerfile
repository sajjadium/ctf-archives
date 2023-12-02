FROM --platform=linux/amd64 ubuntu:22.04 as deps

FROM pwn.red/jail

COPY --from=deps / /srv
COPY qemu-arm /srv/app/
COPY lib /srv/app/lib
COPY flag.txt /srv/app/
COPY coal-mine /srv/app/
COPY run.sh /srv/app/run

RUN chmod +x /srv/app/run

ENV JAIL_MEM=32M
ENV JAIL_PIDS=8