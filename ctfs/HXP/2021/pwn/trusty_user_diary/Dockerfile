# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t trusty_user_diary .
# 3) docker run -p 27499:1024 --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it trusty_user_diary
# 4) nc localhost 27499

FROM debian:bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
        qemu-system-x86 \
 && rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY run.sh bzImage initramfs.cpio flag.txt /home/ctf/

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/run.sh && \
    chmod 004 /home/ctf/bzImage && \
    chmod 004 /home/ctf/initramfs.cpio && \
    chmod 004 /home/ctf/flag.txt

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

USER root
EXPOSE 1024

CMD ynetd -u ctf -sh n -t 300 -lt 25 -lm -1 /home/ctf/run.sh
