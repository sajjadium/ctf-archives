FROM ubuntu:22.04 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY main /srv/app/run
