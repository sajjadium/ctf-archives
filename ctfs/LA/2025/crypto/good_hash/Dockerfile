FROM python:3.12-slim-bookworm AS app
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY chall.py /srv/app/run
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=20M