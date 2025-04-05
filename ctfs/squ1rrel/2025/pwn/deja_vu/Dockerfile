FROM ubuntu:24.04 AS base

FROM pwn.red/jail

COPY --from=base / /srv
COPY deja-vu /srv/app/run
COPY flag.txt /srv/app/
ENV JAIL_TIME=60 JAIL_MEM=100M JAIL_CPU=1000
