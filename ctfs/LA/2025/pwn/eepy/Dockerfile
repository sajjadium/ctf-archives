FROM pwn.red/jail

COPY --from=python:3.12-slim-bookworm / /srv
COPY run.py /srv/app/run
COPY vuln /srv/app/
COPY flag.txt /srv/app/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=256M JAIL_PIDS=10 JAIL_TIME=400 JAIL_TMP_SIZE=1M
