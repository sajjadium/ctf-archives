FROM pwn.red/jail

# python:3.12.1-slim-bookworm
COPY --from=python@sha256:db7e9284d53f7b827c58a6239b9d2907c33250215823b1cdb7d1e983e70dafa5 / /srv
COPY flag.txt /srv/
RUN chmod 444 /srv/flag.txt && mv /srv/flag.txt /srv/flag.`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20`.txt
COPY irs /srv/app/irs
COPY audit.py /srv/app/audit.py
COPY run.sh /srv/app/run

ENV JAIL_MEM=20M
