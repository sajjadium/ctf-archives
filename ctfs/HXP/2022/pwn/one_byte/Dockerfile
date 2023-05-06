# see docker-compose.yml

FROM debian:bullseye

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        qemu-system-x86 && \
    rm -rf /var/lib/apt/lists

RUN useradd --create-home --shell /bin/bash ctf

COPY ynetd /sbin/
COPY initramfs.cpio.gz run.sh vmlinuz flag.txt /home/ctf/

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 004 /home/ctf/flag.txt && \
    chmod 004 /home/ctf/initramfs.cpio.gz && \
    chmod 004 /home/ctf/vmlinuz && \
    chmod 005 /home/ctf/run.sh

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

WORKDIR /home/ctf
EXPOSE 1024
CMD ynetd -pow 30 -t 600 -lt 60 -lm -1 /home/ctf/run.sh
