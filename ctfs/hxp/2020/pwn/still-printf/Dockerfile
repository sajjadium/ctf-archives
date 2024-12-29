# echo 'hxp{FLAG}' > flag.txt && docker build -t still-printf . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 9509:1024 still-printf

FROM debian:buster

# fail build if libc is not the intended version (or SHA256 gets broken)
RUN echo 'dedb887a5c49294ecd850d86728a0744c0e7ea780be8de2d4fc89f6948386937 /lib/x86_64-linux-gnu/libc.so.6' | sha256sum  --check && \
    echo '3e7cb1a5fa4d540f582dddfdb0c69958eca738ba8d60c0bbb6719f091192f33f /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2' | sha256sum --check

COPY flag.txt /
RUN mv /flag.txt /flag_$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24).txt && \
    chown root:root /flag_*.txt && \
    chmod 444 /flag_*.txt

# Set up ynetd and the launcher
RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf
COPY still-printf /home/ctf/
COPY ynetd /sbin/
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/still-printf

# We're paranoid
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

# Run
USER root
EXPOSE 1024
CMD ynetd -sh n -t 10 -lt 60 -lm 5000000 /home/ctf/still-printf
