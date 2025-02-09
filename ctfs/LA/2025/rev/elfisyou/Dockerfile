FROM pwn.red/jail

COPY --from=python:3.12-slim-bookworm / /srv
COPY chal.py /srv/app/run
COPY elf flag.txt /srv/app/

ENV JAIL_MEM=256M JAIL_PIDS=100 JAIL_TIME=60 JAIL_TMP_SIZE=10
