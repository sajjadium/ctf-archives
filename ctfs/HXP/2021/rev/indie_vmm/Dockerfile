# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t indie_vmm .
# 3) docker run -p 27501:1024 --rm --device=/dev/kvm --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it indie_vmm
# 4) nc localhost 27501

FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY flag.txt docker-stuff/readflag /
RUN chown root:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

COPY lkvm run.sh bzImage initramfs.cpio /home/ctf/

RUN mkdir -p /home/ctf/.lkvm

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/run.sh && \
    chmod 005 /home/ctf/lkvm && \
    chmod 004 /home/ctf/bzImage && \
    chmod 004 /home/ctf/initramfs.cpio && \
    chown -R root:root /lib/systemd/system/ && \
    chmod -R 000 /lib/systemd/system/

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

USER root
RUN chmod 703 /home/ctf/.lkvm
EXPOSE 1024
CMD while true; do find /home/ctf/.lkvm/ -maxdepth 1 -mindepth 1 -mmin +10 -type s -delete \; ; sleep 1m; done & \
    chmod 666 /dev/kvm && \
    ynetd -u ctf -np y -sh n -lm 536870912 -lt 30 -t 70 -lpid 32 /home/ctf/run.sh
