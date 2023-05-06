# echo 'hxp{FLAG}' > flag.txt && docker build -t stegernseer . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 7207:1024 stegernseer

FROM ubuntu:20.04

COPY flag.txt /
RUN mv /flag.txt /flag_$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24).txt && \
    chown root:root /flag_*.txt && \
    chmod 444 /flag_*.txt

# Set up ynetd and the launcher
RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf
COPY stegernseer /home/ctf/
COPY ynetd /sbin/
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/stegernseer

# We're paranoid
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

# Run
USER root
EXPOSE 1024
CMD ynetd -lm -1 -lt 20 -t 120 -sh n -lpid 72 /home/ctf/stegernseer
