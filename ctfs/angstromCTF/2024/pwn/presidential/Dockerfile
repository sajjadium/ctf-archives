FROM pwn.red/jail

COPY --from=python:3.12-slim-bookworm / /srv
COPY --chmod=755 server.py /srv/app/run
