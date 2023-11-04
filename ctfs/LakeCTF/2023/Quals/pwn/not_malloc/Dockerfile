FROM docker.io/library/ubuntu:22.04 as builder

RUN useradd -u 1000 jail

FROM pwn.red/jail

COPY --from=builder / /srv
COPY chal /srv/app/run
COPY libnotmalloc.so /srv/app/libnotmalloc.so
COPY libc.so.6 /srv/app/libc.so.6
COPY ld-linux-x86-64.so.2 /srv/app/ld-linux-x86-64.so.2
COPY flag /srv/app/flag

RUN chmod 755 /srv/app/run /srv/app/libnotmalloc.so
RUN chmod 744 /srv/app/flag

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
