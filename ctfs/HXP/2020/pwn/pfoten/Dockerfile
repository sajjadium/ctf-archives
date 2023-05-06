# echo 'hxp{FLAG}' > flag.txt && docker build -t pfoten . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 22222:1024 pfoten

FROM debian:buster

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 procps qemu-system-x86 \
 && rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY run.sh vmlinuz initramfs.cpio.gz flag.txt /home/ctf/

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 555 /home/ctf/run.sh && \
    chmod 444 /home/ctf/vmlinuz && \
    chmod 444 /home/ctf/initramfs.cpio.gz && \
    chmod 444 /home/ctf/flag.txt

USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group  /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

EXPOSE 1024

CMD ynetd -pow 28 -t 300 -lt 30 -lm -1 /home/ctf/run.sh
