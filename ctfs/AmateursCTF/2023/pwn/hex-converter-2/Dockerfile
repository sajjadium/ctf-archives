FROM pwn.red/jail

COPY --from=debian:bookworm-slim / /srv
COPY chal /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run

ENV JAIL_MEM=10M JAIL_TIME=60