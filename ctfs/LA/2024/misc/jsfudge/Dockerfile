FROM pwn.red/jail

COPY --from=node:21-alpine / /srv
COPY index.js /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_PIDS=20
ENV JAIL_MEM=40M
