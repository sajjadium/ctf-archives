FROM python:3.11-bookworm as base

WORKDIR /app
RUN pip install --no-cache-dir pycryptodome gmpy2
COPY server.py run

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_ENV_PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV JAIL_TIME=180 JAIL_CPU=500 JAIL_MEM=10M
