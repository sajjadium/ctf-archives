FROM pwn.red/jail

COPY --from=python:alpine / /srv
COPY . /srv/app
RUN cp /srv/app/server.py /srv/app/run

ENV JAIL_TIME=10
ENV JAIL_MEM=32M
