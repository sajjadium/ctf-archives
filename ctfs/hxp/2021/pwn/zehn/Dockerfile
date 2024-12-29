# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t zehn .
# 3) docker run -p 55557:1024 --rm --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it zehn

FROM archlinux

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/
COPY vuln /home/ctf/

COPY ld-2.33.so /lib64/ld-2.33.so
COPY libc-2.33.so /lib64/libc-2.33.so

COPY flag.txt docker-stuff/readflag /
RUN chown root:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd

RUN chmod 555 vuln /lib64/ld-2.33.so /lib64/libc-2.33.so

RUN chown 500 /usr/bin/mount /usr/bin/umount && \
    find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'
USER root

EXPOSE 1024
CMD mkdir /hassfs && \
    mount -t proc proc /hassfs && \
    echo 32 > /hassfs/sys/vm/mmap_rnd_bits && \
    umount /hassfs && \
    ynetd -np y 'uname -a; /home/ctf/vuln'
