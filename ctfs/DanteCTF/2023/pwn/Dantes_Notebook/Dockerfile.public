FROM pwn.red/jail

COPY --from=ubuntu:22.04 / /srv

COPY notebook /srv/app/run

COPY flag.txt /srv/app/flag.txt
COPY flag.txt /srv/flag.txt

RUN chmod 755 /srv/app/run
