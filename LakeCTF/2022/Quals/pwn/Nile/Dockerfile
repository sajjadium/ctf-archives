FROM docker.io/library/ubuntu:22.04 as builder

RUN useradd -u 1000 jail

FROM pwn.red/jail

COPY --from=builder / /srv

COPY nile /srv/app/run
COPY flag /srv/app/flag
COPY ld-2.32.so /srv/app/ld-2.32.so
COPY libc-2.32.so /srv/app/libc-2.32.so

RUN chmod 755 /srv/app/run /srv/app/ld-2.32.so /srv/app/libc-2.32.so
RUN chmod 744 /srv/app/flag

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
