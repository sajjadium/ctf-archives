# echo 'hxp{flag}' > flag.txt && docker build -t nemoji . && docker run -it -p 65432:1024 --cap-add=SYS_ADMIN --security-opt apparmor=unconfined nemoji

FROM debian:buster

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        python3 \
    && rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/
COPY libc-2.28.so /lib/x86_64-linux-gnu/
COPY ld-2.28.so /lib/x86_64-linux-gnu/
COPY gen_challenge.py main flag.txt /home/ctf/

# generate vuln
RUN /home/ctf/gen_challenge.py && \
    rm /home/ctf/main /home/ctf/gen_challenge.py

RUN chown -R root:root /home/ctf && \
    chown root:root /lib/x86_64-linux-gnu/libc-2.28.so && \
    chown root:root /lib/x86_64-linux-gnu/ld-2.28.so && \
    chmod 755 /lib/x86_64-linux-gnu/libc-2.28.so && \
    chmod 755 /lib/x86_64-linux-gnu/ld-2.28.so && \
    chmod 555 /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 555 /home/ctf/vuln && \
    chmod 444 /home/ctf/flag.txt

USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'

USER root

EXPOSE 1024
CMD ynetd -sh n -lm 536870912 -lt 10 /home/ctf/vuln
