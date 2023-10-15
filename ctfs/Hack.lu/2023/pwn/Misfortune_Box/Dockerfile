# echo 'flag{fake_flag}' > flag && docker build -t misfortune-box . && docker run --rm -p 1337:1337 --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti misfortune-box

FROM archlinux:latest

RUN pacman -Syu --noconfirm libaio pixman && \
    mkdir /chall

ADD qemu-system-meta kernel run.sh run_chall.sh ynetd /chall
ADD flag /flag

RUN chown -R root:root /chall /flag && \
    chmod -R 000 /chall /flag && \
    chmod 500 /chall/ynetd /chall/run.sh && \
    chmod 004 /chall/kernel /flag && \
    chmod 005 /chall/run_chall.sh /chall/qemu-system-meta /chall

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete || true
USER nobody
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev|/run|/proc|/sys|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)(/|$)'
USER root

WORKDIR /chall

CMD ["./run.sh"]
EXPOSE 1337
