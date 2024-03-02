# ubuntu@22:04
FROM ubuntu@sha256:81bba8d1dde7fc1883b6e95cd46d6c9f4874374f2b360c8db82620b33f6b5ca1 as app

FROM pwn.red/jail
COPY --from=app / /srv

COPY analyzer /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_PORT=7273 JAIL_MEM=40M JAIL_TIME=30