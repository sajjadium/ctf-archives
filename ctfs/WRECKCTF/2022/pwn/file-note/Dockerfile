FROM pwn.red/jail:0.3.0

COPY --from=ubuntu:22.04 / /srv
COPY flag.txt /srv/app/
COPY note /srv/app/run

ENV JAIL_TMP_SIZE=1M
