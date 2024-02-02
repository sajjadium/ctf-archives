FROM pwn.red/jail

# python:3.12.1-slim-bookworm
COPY --from=python@sha256:85e668ed5c6219f9fd1a70d12103b6c8b2cfbdca971d045cdafc301c061c049d / /srv

COPY jail.py /srv/app/run
COPY flag-*.txt /srv/app/
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=20M
