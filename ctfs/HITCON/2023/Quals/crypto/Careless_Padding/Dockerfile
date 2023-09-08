FROM python:3.11-alpine as base

WORKDIR /app
RUN pip install pycryptodome
COPY chal.py run
COPY secret.py secret.py

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=30 JAIL_CPU=500 JAIL_MEM=10M
