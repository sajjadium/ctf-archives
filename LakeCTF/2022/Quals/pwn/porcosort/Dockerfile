FROM docker.io/library/archlinux@sha256:2bfe247c46221b0770325d69ec195b50455b2865588665e6926b2d1168982e67 AS builder

RUN useradd -u 1000 jail

FROM pwn.red/jail

COPY --from=builder / /srv

COPY porcosort /srv/app/run
COPY flag /srv/app/flag

RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
