FROM python:3.10-slim AS app

FROM pwn.red/jail

COPY --from=app / /srv/
COPY chall.py /srv/app/
COPY flag.txt /srv/app/
COPY start.sh /srv/app/run

RUN chmod 755 /srv/app/run

ENV JAIL_MEM=100M JAIL_TIME=180