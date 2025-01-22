FROM python:3.11-slim AS app

RUN pip install --no-cache-dir pycryptodome
RUN mkdir -p /challenge
WORKDIR /challenge
COPY chall.py .
COPY secrets.py .

FROM pwn.red/jail

COPY --from=app / /srv
RUN mkdir -p /srv/app
COPY --chmod=555 ./run /srv/app/run

ENV JAIL_PIDS=40 JAIL_MEM=10M JAIL_TIME=120
