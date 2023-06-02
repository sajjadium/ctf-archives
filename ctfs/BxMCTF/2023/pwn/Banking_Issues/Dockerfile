FROM python:slim AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY main.py /srv/app/run
