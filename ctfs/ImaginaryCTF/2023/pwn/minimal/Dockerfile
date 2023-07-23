FROM pwn.red/jail

COPY --from=ubuntu:22.04 / /srv

COPY vuln /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run

ENV JAIL_TIME=120
