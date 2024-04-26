FROM ubuntu:23.10 AS app
FROM pwn.red/jail

COPY --from=app / /srv
COPY ./worm /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
COPY ./libc.so.6 /srv/app/
COPY ./libm.so.6 /srv/app/
COPY ./ld-linux-x86-64.so.2 /srv/app/
COPY ./libstdc++.so.6 /srv/app/
COPY ./libgcc_s.so.1 /srv/app/

RUN chmod +x /srv/app/run

ENV JAIL_PORT=1447 JAIL_MEM=20M JAIL_ENV_NUM=5 JAIL_PID=20
