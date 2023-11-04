FROM docker.io/library/ubuntu:22.04 as builder
RUN useradd -u 1000 jail

RUN apt-get update && apt-get install -y netcat mawk 

FROM pwn.red/jail

COPY --from=builder / /srv

COPY setup.sh /srv/app/run
COPY local/players /srv/app/players
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod -R 755 /srv/app/players
RUN chmod 777 /srv/app/players
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_TIME 30
ENV JAIL_PIDS 10000
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 30M
ENV JAIL_TMP_SIZE 2M
ENV JAIL_DEV null,zero,urandom,stdin