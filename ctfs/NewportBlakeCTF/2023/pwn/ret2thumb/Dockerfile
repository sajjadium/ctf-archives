FROM --platform=linux/amd64 ubuntu:22.04 AS app

FROM --platform=linux/amd64 pwn.red/jail
COPY --from=app / /srv

COPY qemu-arm /srv/app/
COPY lib /srv/app/lib
COPY flag.txt /srv/app/
COPY ret2thumb /srv/app/
COPY run.sh /srv/app/run

RUN chmod +x /srv/app/run
