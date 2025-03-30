FROM ubuntu:22.04 AS base

FROM pwn.red/jail

COPY --from=base / /srv
COPY run.sh /srv/app/run
COPY locked_room libc.so flag.txt /srv/app/
ENV JAIL_TIME=60 JAIL_MEM=100M JAIL_CPU=1000
