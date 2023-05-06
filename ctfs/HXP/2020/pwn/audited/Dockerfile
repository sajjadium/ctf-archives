# echo 'hxp{FLAG}' > flag.txt && docker build -t audited . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 8007:1024 audited

FROM archlinux

RUN pacman -Sy --noconfirm python && \
    rm -rf /var/lib/pacman /var/cache/pacman

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf
COPY audited.py /home/ctf/
COPY ynetd /sbin/
COPY flag.txt /

RUN mv /flag.txt /flag_$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24).txt && \
    chown root:root /flag_*.txt && \
    chmod 444 /flag_*.txt

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/audited.py

USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/tmp|/var/mail|/var/spool/mail|/var/tmp|/dev|/proc)'
USER root

EXPOSE 1024
CMD ynetd -t 15 -sh n /home/ctf/audited.py
