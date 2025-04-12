from pwn.red/jail

COPY --from=ubuntu:25.04@sha256:adb623490ed6f4252989513900f1e88dc11c7974577de44d6959181a354a427a / /srv

COPY easy_rop /srv/app/run
COPY flag.txt /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_MEM 100M
