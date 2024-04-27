FROM ubuntu@sha256:562456a05a0dbd62a671c1854868862a4687bf979a96d48ae8e766642cd911e8 AS app
FROM pwn.red/jail

COPY --from=app / /srv
COPY thopter /srv/app/run
COPY ld-linux-x86-64.so.2 /srv/app
COPY libc.so.6 /srv/app
COPY flag.txt /srv/app/flag.txt

RUN chmod +x /srv/app/run

ENV JAIL_PORT=1447 JAIL_MEM=128M JAIL_ENV_NUM=5 JAIL_PID=20 JAIL_TIME=600
