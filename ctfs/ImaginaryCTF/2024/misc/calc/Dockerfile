FROM python:3.12.4-alpine AS python

FROM redpwn/jail
COPY --from=python / /srv
COPY server.py /srv/app/run
COPY flag.txt /srv/app/flag.txt
ENV JAIL_MEM=20M JAIL_PORT=1337
