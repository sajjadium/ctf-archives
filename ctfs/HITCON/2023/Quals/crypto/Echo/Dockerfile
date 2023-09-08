FROM python:3.11-alpine as base

WORKDIR /app
RUN pip install pycryptodome
COPY server.py run
# `give` is a compiled binary that will output flag if you execute `./give me flag please`
COPY give .
RUN chmod 111 give

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=60 JAIL_MEM=20M
