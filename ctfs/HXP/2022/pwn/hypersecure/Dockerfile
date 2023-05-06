# see docker-compose.yml

FROM ubuntu:22.10

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cpio qemu-system && \
    rm -rf /var/lib/apt/lists

RUN useradd --create-home --shell /bin/bash ctf

COPY ynetd /sbin/
COPY initramfs.cpio bzImage run.sh /home/ctf/

# Add the flag to the initramfs
RUN mkdir /home/ctf/root/
COPY flag.txt /home/ctf/root/
RUN cd /home/ctf/ && \
    chmod 400 /home/ctf/root/flag.txt && \
    chmod 500 /home/ctf/root/ && \
    find root -print0 | cpio --null --reproducible --create --append "--owner=+0:+0" --format=newc -O initramfs.cpio && \
    rm -rf /home/ctf/root/

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 004 /home/ctf/initramfs.cpio && \
    chmod 004 /home/ctf/bzImage && \
    chmod 005 /home/ctf/run.sh

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

WORKDIR /home/ctf
EXPOSE 1024
CMD while true; do sleep 1m; find /tmp -name 'tmp.*' -mmin '+15' -delete; done & \
    ynetd -pow 28 -t 600 -lt 300 -lm -1 /home/ctf/run.sh
