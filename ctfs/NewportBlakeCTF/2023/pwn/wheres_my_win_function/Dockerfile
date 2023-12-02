FROM --platform=linux/amd64 ubuntu:22.04 as deps

FROM --platform=linux/amd64 pwn.red/jail

COPY --from=deps / /srv/
COPY lib /srv/app/lib
COPY qemu-arm /srv/app/
COPY flag.txt /srv/app/
COPY wmwf /srv/app/
COPY run.sh /srv/app/run

RUN chmod 755 /srv/app/run

ENV JAIL_TIME=30
ENV JAIL_MEM=32M
ENV JAIL_PIDS=10