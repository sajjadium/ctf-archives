FROM node:20-alpine AS app

WORKDIR /app
COPY src/ .

FROM pwn.red/jail
COPY --from=app / /srv
COPY ./src/run.sh /srv/app/run
COPY ./readflag /srv/app/readflag
RUN chmod 111 /srv/app/readflag
ENV JAIL_MEM=64M JAIL_PIDS=20 JAIL_TMP_SIZE=1M
