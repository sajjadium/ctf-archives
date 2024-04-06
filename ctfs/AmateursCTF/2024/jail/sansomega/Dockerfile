FROM python:3.10 as base

COPY ./shell.py /app/run
COPY ./flag.txt /app/flag.txt

FROM pwn.red/jail:latest

COPY --from=base / /srv
RUN chmod 755 /srv/app/run

ENV JAIL_TIME=300 JAIL_MEM=50M JAIL_PIDS=10 JAIL_DEV=null,zero,urandom,ptmx JAIL_PIDS=60