FROM ubuntu:22.04 as deps

RUN apt-get update && apt-get -y install \
    qemu-system-x86 \
    && rm -rf /var/lib/apt/lists/*

FROM pwn.red/jail

ENV JAIL_TIME=13371337
ENV JAIL_MEM=32M
ENV JAIL_TMP_SIZE=100M

COPY --from=deps / /srv

COPY run-remote.sh /srv/app/run
COPY disk.img /srv/app

RUN chmod 755 /srv/app/run