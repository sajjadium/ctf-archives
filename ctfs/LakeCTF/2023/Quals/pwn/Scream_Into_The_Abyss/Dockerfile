FROM docker.io/library/ubuntu:22.04 as builder

RUN useradd -u 1000 jail

FROM pwn.red/jail

COPY --from=builder / /srv

COPY abyss_scream /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run 
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
